# 🤖 ShutupBot - Telegram Moderatsiya Boti

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![Aiogram](https://img.shields.io/badge/Aiogram-3.22+-green?style=for-the-badge&logo=telegram)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Telegram guruhlarida taqiqlangan so'zlarni avtomatik ravishda nazorat qiluvchi aqlli moderatsiya boti**

[🚀 O'rnatish](#-o'rnatish) • [⚙️ Sozlash](#️-sozlash) • [📖 Foydalanish](#-foydalanish) • [🔧 Xususiyatlar](#-xususiyatlar)

</div>

---

## 📋 Loyiha haqida

**ShutupBot** - bu Telegram guruhlarida taqiqlangan so'zlarni avtomatik ravishda aniqlab, foydalanuvchilarni progressiv jazo tizimi orqali nazorat qiluvchi aqlli moderatsiya boti. Bot foydalanuvchilarning xatti-harakatlarini 24 soat davomida kuzatib, har bir buzish uchun mos darajada jazo beradi.

### 🎯 Asosiy maqsad
- Guruhlarda toza va madaniy muhit yaratish
- Taqiqlangan so'zlardan foydalanishni oldini olish
- Foydalanuvchilarni progressiv jazo tizimi orqali o'qitish
- Adminlarning ishini engillashtirish

---

## ✨ Xususiyatlar

### 🛡️ Aqlli Moderatsiya
- **Avtomatik aniqlash**: Taqiqlangan so'zlarni real vaqtda aniqlaydi
- **Xabar o'chirish**: Buzilgan xabarlarni avtomatik o'chiradi
- **Progressiv jazo**: Har bir buzish uchun ortib boruvchi jazo muddati

### 📊 Progressiv Jazo Tizimi
| Buzish soni | Jazo muddati | Tavsif |
|-------------|--------------|---------|
| 1-chi | 5 daqiqa | Birinchi ogohlantirish |
| 2-chi | 15 daqiqa | Ikkinchi ogohlantirish |
| 3-chi | 1 soat | Uchinchi ogohlantirish |
| 4-chi va undan keyin | 1 kun | Jiddiy jazo |

### 🔄 Avtomatik Tizim
- **24 soatlik kuzatuv**: Har bir foydalanuvchining buzishlarini 24 soat davomida hisoblaydi
- **Avtomatik tozalash**: 24 soatdan keyin buzishlar hisobini tozalaydi
- **Xabar o'chirish**: Blok tugagach, guruhdagi ogohlantirish xabarlarini avtomatik o'chiradi

### 💬 Xabar Tizimi
- **Shaxsiy ogohlantirish**: Har bir foydalanuvchiga shaxsiy xabar yuboradi
- **Guruh bildirishnomasi**: Guruhga buzish haqida ma'lumot beradi
- **O'zbek tilida**: Barcha xabarlar o'zbek tilida

---

## 🚀 O'rnatish

### 📋 Talablar
- Python 3.11 yoki undan yuqori versiya
- Telegram Bot Token (BotFather dan olingan)
- Git

### 🔧 O'rnatish qadamlari

1. **Loyihani klonlash**
```bash
git clone https://github.com/NodirUstoz/ShutupBot.git
cd ShutupBot
```

2. **Virtual muhit yaratish**
```bash
python -m venv venv
# Windows uchun:
venv\Scripts\activate
# Linux/Mac uchun:
source venv/bin/activate
```

3. **Kerakli kutubxonalarni o'rnatish**
```bash
pip install -r requirements.txt
```

4. **Bot Token olish**
   - [@BotFather](https://t.me/BotFather) ga o'ting
   - `/newbot` buyrug'ini yuboring
   - Bot nomini va username ni kiriting
   - Olingan token ni saqlang

5. **Konfiguratsiya faylini yaratish**
```bash
# .env faylini yarating
echo "BOT_TOKEN=your_bot_token_here" > .env
```

6. **Botni ishga tushirish**
```bash
python bot.py
```

---

## ⚙️ Sozlash

### 🔧 config.py faylini sozlash

```python
# Taqiqlangan so'zlar ro'yxati
FORBIDDEN_WORDS = [
    "so'kinish1", 
    "so'kinish2", 
    "yomonso'z",
    # O'zingizning so'zlaringizni qo'shing
]

# Jazo muddatlari (soniyalarda)
PUNISHMENT_DURATIONS = {
    1: 300,      # 5 daqiqa
    2: 900,      # 15 daqiqa  
    3: 3600,     # 1 soat
    4: 86400     # 1 kun
}
```

### 📝 Xabar shablonlarini o'zgartirish

```python
# Shaxsiy ogohlantirish xabari
BLOCKED_MESSAGE_TEMPLATE = """❌ Siz taqiqlangan so'z ishlatdingiz!

🚫 Sabab: "{word}" so'zi taqiqlangan
⏱ Blok muddati: {duration}
📊 Bugungi kunlik buzishlar soni: {count}/4

Iltimos, guruh qoidalariga rioya qiling."""

# Guruh bildirishnomasi
GROUP_NOTIFICATION_TEMPLATE = """🚫 **Foydalanuvchi bloklandi**

👤 Foydalanuvchi: [{user_name}](tg://user?id={user_id}) `#{user_id}`
🚫 Sabab: "{word}" so'zi ishlatildi
⏱ Blok muddati: {duration}
📊 Bu foydalanuvchining {count}-chi buzishi

_Bu xabar foydalanuvchi blokdan chiqgach o'chadi._"""
```

---

## 📖 Foydalanish

### 🤖 Botni guruhga qo'shish

1. Botni guruhga qo'shing
2. Botga admin huquqlarini bering (xabarlarni o'chirish va foydalanuvchilarni cheklash huquqi)
3. Bot avtomatik ravishda ishlay boshlaydi

### 👥 Admin huquqlari

Bot to'g'ri ishlashi uchun quyidagi huquqlarga ega bo'lishi kerak:
- ✅ Xabarlarni o'chirish
- ✅ Foydalanuvchilarni cheklash
- ✅ Guruh ma'lumotlarini o'qish

### 🔍 Qanday ishlaydi

1. **Xabar tekshirish**: Bot har bir xabarni taqiqlangan so'zlar bilan solishtiradi
2. **Buzish aniqlash**: Agar taqiqlangan so'z topilsa, foydalanuvchi buzish qilgan deb hisoblanadi
3. **Jazo berish**: Progressiv jazo tizimi bo'yicha foydalanuvchi cheklanadi
4. **Xabar yuborish**: Foydalanuvchiga shaxsiy ogohlantirish va guruhga bildirishnoma yuboriladi

---

## 🛠️ Texnik tafsilotlar

### 📚 Ishlatilgan texnologiyalar
- **Python 3.11+**: Asosiy dasturlash tili
- **Aiogram 3.22+**: Telegram Bot API kutubxonasi
- **python-dotenv**: Muhit o'zgaruvchilarini boshqarish

### 🏗️ Loyiha tuzilishi
```
ShutupBot/
├── bot.py              # Asosiy bot kodi
├── config.py           # Konfiguratsiya sozlamalari
├── pyproject.toml      # Loyiha konfiguratsiyasi
├── requirements.txt    # Kerakli kutubxonalar
└── README.md          # Loyiha hujjati
```

### 🔄 Asosiy komponentlar

#### ModerationBot klassi
- `contains_forbidden_word()`: Taqiqlangan so'zlarni aniqlash
- `restrict_user()`: Foydalanuvchini cheklash
- `send_private_warning()`: Shaxsiy ogohlantirish yuborish
- `send_group_notification()`: Guruh bildirishnomasi

#### Event Handlerlar
- `handle_group_message()`: Guruh xabarlarini qayta ishlash
- `handle_private_message()`: Shaxsiy xabarlarni qayta ishlash

---

## 🎨 Xususiyatlar

### 🎯 Aqlli Algoritm
- **Case-insensitive**: Katta-kichik harflarga e'tibor bermaydi
- **Substring matching**: So'zning bir qismi ham topilsa, buzish deb hisoblanadi
- **Real-time processing**: Xabarlar real vaqtda tekshiriladi

### 🔒 Xavfsizlik
- **Token himoyasi**: Bot token .env faylida saqlanadi
- **Error handling**: Xatoliklarni boshqarish
- **Logging**: Barcha harakatlar log qilinadi

### 📊 Monitoring
- **Violation tracking**: Har bir foydalanuvchining buzishlarini kuzatish
- **Automatic cleanup**: Eski ma'lumotlarni avtomatik tozalash
- **Message management**: Xabarlarni avtomatik o'chirish

---

## 🤝 Hissa qo'shish

Bu loyihaga hissa qo'shish uchun:

1. **Fork** qiling
2. **Feature branch** yarating (`git checkout -b feature/AmazingFeature`)
3. **Commit** qiling (`git commit -m 'Add some AmazingFeature'`)
4. **Push** qiling (`git push origin feature/AmazingFeature`)
5. **Pull Request** yarating

---

## 👨‍💻 Muallif

**Sizning Ismingiz**
- GitHub: [@NodirUstoz](https://github.com/NodirUstoz)
- Telegram: [@NodirUstozBot](https://t.me/NodirUstozBot)

---

## 🙏 Minnatdorchilik

- [Aiogram](https://github.com/aiogram/aiogram) - Ajoyib Telegram Bot kutubxonasi
- [Python](https://python.org) - Kuchli dasturlash tili
- [Telegram](https://telegram.org) - Eng yaxshi messenjer

---

## 📞 Aloqa

Savollar yoki takliflar uchun:
- 💬 Telegram: [@NodirUstozBot](https://t.me/NodirUstozBot)
- 🐛 Issues: [GitHub Issues](https://github.com/NodirUstoz/ShutupBot/issues)

---

<div align="center">

**⭐ Agar loyiha sizga yoqsa, yulduzcha qoldiring! ⭐**

</div>
