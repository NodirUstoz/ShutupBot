"""
Bot configuration settings
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Bot settings
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Moderation settings
FORBIDDEN_WORDS = ["so'kinish1", "so'kinish2", "yomonso'z"]

# Progressive punishment durations (in seconds)
PUNISHMENT_DURATIONS = {
    1: 300,      # First offense: 5 minutes
    2: 900,      # Second offense: 15 minutes  
    3: 3600,     # Third offense: 1 hour
    4: 86400     # Fourth offense: 1 day
}

# Time window for counting violations (24 hours)
VIOLATION_WINDOW = 86400  # 24 hours in seconds

# Message templates
BLOCKED_MESSAGE_TEMPLATE = """❌ Siz taqiqlangan so'z ishlatdingiz!

🚫 Sabab: "{word}" so'zi taqiqlangan
⏱ Blok muddati: {duration}
📊 Bugungi kunlik buzishlar soni: {count}/4

Iltimos, guruh qoidalariga rioya qiling."""

# Group notification template with clickable profile and blue ID
GROUP_NOTIFICATION_TEMPLATE = """🚫 **Foydalanuvchi bloklandi**

👤 Foydalanuvchi: [{user_name}](tg://user?id={user_id}) `#{user_id}`
🚫 Sabab: "{word}" so'zi ishlatildi
⏱ Blok muddati: {duration}
📊 Bu foydalanuvchining {count}-chi buzishi

_Bu xabar foydalanuvchi blokdan chiqgach o'chadi._"""

def format_duration(seconds):
    """Format duration in human readable format"""
    if seconds < 60:
        return f"{seconds} soniya"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes} daqiqa"
    elif seconds < 86400:
        hours = seconds // 3600
        return f"{hours} soat"
    else:
        days = seconds // 86400
        return f"{days} kun"