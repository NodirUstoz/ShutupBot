"""
Telegram Moderation Bot using Aiogram 3
Blocks users for using forbidden words in groups
"""
import asyncio
import logging
import time
from datetime import datetime, timedelta
from typing import List, Dict, Set
from collections import defaultdict

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ChatPermissions
from aiogram.types import User
from aiogram.enums import ChatType

from config import (
    BOT_TOKEN, FORBIDDEN_WORDS, PUNISHMENT_DURATIONS, 
    VIOLATION_WINDOW, BLOCKED_MESSAGE_TEMPLATE, GROUP_NOTIFICATION_TEMPLATE, format_duration
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is required")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class ModerationBot:
    """Main moderation bot class"""
    
    def __init__(self):
        self.forbidden_words = [word.lower() for word in FORBIDDEN_WORDS]
        # Store user violations: user_id -> list of timestamps
        self.user_violations = defaultdict(list)
        # Store admin notification messages for delayed deletion: user_id -> (message_id, chat_id, duration)
        self.admin_notifications = {}
    
    def clean_old_violations(self, user_id: int) -> None:
        """Remove violations older than 24 hours"""
        current_time = time.time()
        self.user_violations[user_id] = [
            timestamp for timestamp in self.user_violations[user_id]
            if current_time - timestamp < VIOLATION_WINDOW
        ]
    
    def get_violation_count(self, user_id: int) -> int:
        """Get current violation count for user in last 24 hours"""
        self.clean_old_violations(user_id)
        return len(self.user_violations[user_id])
    
    def add_violation(self, user_id: int) -> int:
        """Add new violation and return total count"""
        current_time = time.time()
        self.user_violations[user_id].append(current_time)
        return self.get_violation_count(user_id)
    
    def get_punishment_duration(self, violation_count: int) -> int:
        """Get punishment duration based on violation count"""
        if violation_count <= 4:
            return PUNISHMENT_DURATIONS[violation_count]
        else:
            # After 4 violations, always 1 day
            return PUNISHMENT_DURATIONS[4]
    
    def contains_forbidden_word(self, text: str) -> tuple:
        """Check if text contains any forbidden words. Returns (is_forbidden, word)"""
        if not text:
            return False, None
        
        text_lower = text.lower()
        for word in self.forbidden_words:
            if word in text_lower:
                return True, word
        return False, None
    
    async def restrict_user(self, chat_id: int, user_id: int, duration: int) -> bool:
        """Restrict user from sending messages for specified duration"""
        try:
            # Set permissions to block user from sending messages
            permissions = ChatPermissions(
                can_send_messages=False,
                can_send_media_messages=False,
                can_send_polls=False,
                can_send_other_messages=False,
                can_add_web_page_previews=False,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False
            )
            
            # Calculate until when to restrict
            until_date = datetime.now() + timedelta(seconds=duration)
            
            await bot.restrict_chat_member(
                chat_id=chat_id,
                user_id=user_id,
                permissions=permissions,
                until_date=until_date
            )
            
            logger.info(f"User {user_id} restricted in chat {chat_id} for {duration} seconds")
            return True
            
        except Exception as e:
            logger.error(f"Failed to restrict user {user_id} in chat {chat_id}: {e}")
            return False
    
    async def send_private_warning(self, user_id: int, word: str, duration: int, violation_count: int) -> bool:
        """Send private warning message to user"""
        try:
            message = BLOCKED_MESSAGE_TEMPLATE.format(
                word=word,
                duration=format_duration(duration),
                count=violation_count
            )
            
            await bot.send_message(
                chat_id=user_id,
                text=message
            )
            logger.info(f"Warning sent to user {user_id} for word '{word}', violation #{violation_count}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send warning to user {user_id}: {e}")
            return False
    
    async def send_group_notification(self, chat_id: int, user_id: int, user_name: str, word: str, duration: int, violation_count: int) -> None:
        """Send notification to group about user restriction"""
        try:
            message = GROUP_NOTIFICATION_TEMPLATE.format(
                user_name=user_name,
                user_id=user_id,
                word=word,
                duration=format_duration(duration),
                count=violation_count
            )
            
            # Send notification to group
            notification_msg = await bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode="Markdown"
            )
            
            logger.info(f"Group notification sent for user {user_name} (#{user_id}) - word: '{word}', violation #{violation_count}")
            
            # Store message info for delayed deletion when user is unblocked
            self.admin_notifications[user_id] = {
                'message_id': notification_msg.message_id,
                'chat_id': chat_id,
                'duration': duration,
                'start_time': time.time()
            }
            
            # Schedule deletion after restriction ends
            asyncio.create_task(self.delete_group_notification_after_unblock(user_id, duration))
                
        except Exception as e:
            logger.error(f"Failed to send group notification: {e}")
    
    async def delete_group_notification_after_unblock(self, user_id: int, duration: int) -> None:
        """Delete group notification message after user is unblocked"""
        try:
            # Wait for the restriction duration
            await asyncio.sleep(duration)
            
            # Check if we have stored notification for this user
            if user_id in self.admin_notifications:
                notification_data = self.admin_notifications[user_id]
                
                # Delete the stored message
                try:
                    await bot.delete_message(
                        chat_id=notification_data['chat_id'], 
                        message_id=notification_data['message_id']
                    )
                    logger.info(f"Deleted group notification message for user {user_id}")
                except Exception as e:
                    logger.error(f"Failed to delete group notification for user {user_id}: {e}")
                
                # Remove from storage
                del self.admin_notifications[user_id]
                logger.info(f"Cleaned up notification for user {user_id}")
                
        except Exception as e:
            logger.error(f"Failed to delete group notification for user {user_id}: {e}")


# Initialize moderation bot
moderation_bot = ModerationBot()


@dp.message(F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def handle_group_message(message: Message):
    """Handle messages in groups and supergroups"""
    
    # Skip if no text content
    if not message.text:
        return
    
    # Check for forbidden words
    is_forbidden, forbidden_word = moderation_bot.contains_forbidden_word(message.text)
    if is_forbidden:
        if not message.from_user:
            return
        
        user_id = message.from_user.id
        chat_id = message.chat.id
        
        # Get user display name
        user_name = message.from_user.full_name or message.from_user.username or f"User {user_id}"
        
        # Add violation and get count
        violation_count = moderation_bot.add_violation(user_id)
        duration = moderation_bot.get_punishment_duration(violation_count)
        
        logger.info(f"Forbidden word '{forbidden_word}' detected from user {user_name} ({user_id}) in chat {chat_id}. Violation #{violation_count}")
        
        # Try to delete the offensive message
        try:
            await message.delete()
            logger.info(f"Deleted message from user {user_name}")
        except Exception as e:
            logger.error(f"Failed to delete message: {e}")
        
        # Restrict the user
        restriction_success = await moderation_bot.restrict_user(chat_id, user_id, duration)
        
        if restriction_success:
            # Send group notification (in background task)
            asyncio.create_task(
                moderation_bot.send_group_notification(chat_id, user_id, user_name, forbidden_word, duration, violation_count)
            )
            
            # Send private warning (in background)
            asyncio.create_task(
                moderation_bot.send_private_warning(user_id, forbidden_word, duration, violation_count)
            )


@dp.message(F.chat.type == ChatType.PRIVATE)
async def handle_private_message(message: Message):
    """Handle private messages - bot doesn't work in private chats"""
    await message.answer("Bu bot faqat guruhlarda ishlaydi. Meni guruhga qo'shing.")


async def main():
    """Main function to start the bot"""
    logger.info("Starting Telegram Moderation Bot...")
    
    try:
        # Start polling
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Bot stopped with error: {e}")
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())