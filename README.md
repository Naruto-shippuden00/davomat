# 🎓 Maktab Davomat Bot

Maktab o'quvchilarining davomatini boshqaruvchi aqlli Telegram boti. O'qituvchilar, sinf rahbarlari va ota-onalar uchun qulay va tez davomat yuritish tizimi.

## 📋 Asosiy Funksiyalar

### 👨‍🏫 O'qituvchilar uchun:
- ✅ Dars boshida tez va qulay davomat belgilash
- ⏰ Kechikishlarni sababi bilan qayd etish
- 📊 Kunlik, haftalik va oylik hisobotlar
- 🔔 Ota-onalarga avtomatik xabar yuborish

### 👨‍👩‍👧 Ota-onalar uchun:
- 📱 Farzand davomati haqida real vaqtda xabarnoma
- 📈 Farzand davomat statistikasini ko'rish
- 💬 Kechikish va yo'qlik sabablari haqida ma'lumot

### 🎯 Ma'murlar uchun:
- 👥 Foydalanuvchilarni boshqarish
- 🏫 Sinflar va fanlarni sozlash
- 📊 Umumiy statistika va tahlillar

## 🚀 O'rnatish

### 1. Talablar
- Python 3.9 yoki yuqori versiya
- Telegram Bot Token (@BotFather dan olinadi)

### 2. Kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

### 3. Konfiguratsiya

`.env` faylini yarating va quyidagi ma'lumotlarni kiriting:

```bash
cp .env.example .env
```

`.env` faylini tahrirlang:

```env
BOT_TOKEN=your_telegram_bot_token_here
DATABASE_URL=sqlite+aiosqlite:///./data/davomat.db
ADMIN_TELEGRAM_ID=123456789
```

**Bot Token olish:**
1. Telegram da @BotFather ga yozing
2. `/newbot` buyrug'ini yuboring
3. Bot nomini va username ni kiriting
4. Olingan tokenni `.env` fayliga qo'ying

**Telegram ID aniqlash:**
- @userinfobot ga yozing va o'z ID ingizni oling

### 4. Ma'lumotlar bazasini yaratish

```bash
python init_data.py
```

⚠️ **MUHIM:** `init_data.py` faylida telegram ID larni o'zingiznikiga o'zgartiring!

### 5. Botni ishga tushirish

```bash
python main.py
```

## 📱 Foydalanish

### Birinchi ishga tushirish

1. Telegram da botni qidiring (username orqali)
2. `/start` buyrug'ini yuboring
3. Sizning rolga qarab menyular ochiladi

### O'qituvchilar uchun qo'llanma

#### Davomat belgilash:

1. **"📅 Davomat boshlash"** tugmasini bosing yoki `/davomat` yuboring
2. Sinf va fanni tanlang
3. Har bir o'quvchi uchun holatni belgilang:
   - ✅ Keldi
   - ⏰ Kechikdi
   - ❌ Kelmadi
4. Kechikkanlar uchun sabab va vaqtni kiriting
5. **"💾 Saqlash"** tugmasini bosing
6. Ota-onalarga xabar yuborishni tasdiqlang

#### Hisobotlarni ko'rish:

1. **"📊 Hisobotlar"** tugmasini bosing yoki `/hisobot` yuboring
2. Hisobot turini tanlang:
   - 📅 Bugungi davomat
   - 📊 Haftalik hisobot
   - 📈 Oylik hisobot
   - 👥 Sinf statistikasi

### Ota-onalar uchun qo'llanma

1. **"📊 Farzandim davomati"** tugmasini bosing
2. Oxirgi 7 kunlik davomat va statistikani ko'ring
3. Bot avtomatik ravishda xabarnomalar yuboradi:
   - Farzand kelmasa
   - Farzand kechiksa

## 🏗️ Loyiha Strukturasi

```
davomat/
├── bot/
│   ├── handlers/          # Handler funksiyalar
│   │   ├── start.py      # Start va yordam
│   │   ├── attendance.py # Davomat funksiyalari
│   │   ├── reports.py    # Hisobot funksiyalari
│   │   └── admin.py      # Admin funksiyalari
│   ├── keyboards/         # Keyboard layout'lar
│   │   ├── main_keyboard.py
│   │   ├── attendance_keyboard.py
│   │   └── report_keyboard.py
│   ├── models/            # Ma'lumotlar bazasi modellari
│   │   ├── base.py
│   │   ├── user.py
│   │   ├── student.py
│   │   ├── class_model.py
│   │   ├── subject.py
│   │   ├── attendance.py
│   │   └── notification.py
│   └── utils/             # Yordamchi funksiyalar
│       ├── auth.py
│       ├── notifications.py
│       └── reports.py
├── config/                # Konfiguratsiya
│   └── settings.py
├── data/                  # Ma'lumotlar bazasi
├── main.py               # Asosiy bot fayl
├── init_data.py          # Test ma'lumotlar
├── requirements.txt      # Kutubxonalar
├── .env.example         # Konfiguratsiya namunasi
└── README.md            # Bu fayl
```

## 🎯 Buyruqlar Ro'yxati

| Buyruq | Ta'rif |
|--------|--------|
| `/start` | Botni ishga tushirish |
| `/yordam` | Yordam va qo'llanma |
| `/davomat` | Davomat belgilash |
| `/hisobot` | Hisobotlarni ko'rish |
| `/oquvchilar` | O'quvchilar ro'yxati |
| `/sozlamalar` | Sozlamalar |
| `/admin` | Admin panel (faqat adminlar uchun) |

## 🔐 Xavfsizlik

- Har bir foydalanuvchi faqat o'z ro'li bo'yicha ruxsat etilgan ma'lumotlarni ko'ra oladi
- O'qituvchi faqat o'z sinfi ma'lumotlariga kiradi
- Ota-ona faqat o'z farzandining davomatini ko'radi
- Barcha harakatlar log'lanadi

## 📊 Ma'lumotlar Bazasi

Bot SQLite ma'lumotlar bazasidan foydalanadi. Quyidagi jadvallar mavjud:

- **users** - Foydalanuvchilar (o'qituvchi, ma'mur, ota-ona)
- **classes** - Sinflar
- **students** - O'quvchilar
- **subjects** - Fanlar
- **attendances** - Davomat yozuvlari
- **notifications** - Yuborilgan xabarlar

## 🔧 Sozlash va Maxsuslashtirish

### Xabar Shablonlarini O'zgartirish

`config/settings.py` faylida xabar shablonlarini o'zgartirishingiz mumkin:

```python
PARENT_NOTIFICATION_ABSENT = """
{emoji} Hurmatli {parent_name},
...
"""
```

### Yangi Rol Qo'shish

1. `config/settings.py` ga yangi rol qo'shing
2. `bot/utils/auth.py` da ruxsat tekshiruvlarini yangilang
3. `bot/keyboards/main_keyboard.py` da yangi keyboard yarating

## 🐛 Xatolarni Tuzatish

### Bot ishlamayapti?

1. Bot token to'g'riligini tekshiring
2. Python versiyasini tekshiring: `python --version`
3. Kutubxonalar o'rnatilganligini tekshiring
4. Log'larni ko'ring

### Ma'lumotlar bazasi xatosi?

```bash
# Ma'lumotlar bazasini qayta yaratish
rm -rf data/davomat.db
python init_data.py
```

### Xabarlar yuborilmayapti?

1. Bot @BotFather da faolligini tekshiring
2. Ota-ona telegram ID si to'g'riligini tekshiring
3. Ota-ona bot dan `/start` bosganligini tekshiring

## 📞 Yordam va Qo'llab-quvvatlash

Savollar yoki muammolar bo'lsa:

- Issues: GitHub Issues bo'limida yangi issue oching
- Email: support@example.com

## 📝 License

MIT License

## 🙏 Minnatdorchilik

Bu loyiha quyidagi texnologiyalardan foydalanadi:

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [aiosqlite](https://github.com/omnilib/aiosqlite)

## 🚀 Kelajak Rejalar

- [ ] Excel formatida hisobot export
- [ ] Grafik va diagrammalar qo'shish
- [ ] SMS xabarnomalar
- [ ] Web admin panel
- [ ] Multi-til qo'llab-quvvatlash
- [ ] QR kod orqali davomat
- [ ] Mobil ilova integratsiyasi

## 📸 Screenshot'lar

*Coming soon...*

---

Made with ❤️ for Uzbekistan schools
