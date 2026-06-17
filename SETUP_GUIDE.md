# 🚀 Tez O'rnatish Qo'llanmasi

Bu qo'llanma botni 5 daqiqada ishga tushirish uchun mo'ljallangan.

## ✅ 1-Qadam: Python o'rnatish

Python 3.9 yoki yuqori versiyasi kerak:

```bash
python3 --version
# yoki
python --version
```

Agar Python o'rnatilmagan bo'lsa: [python.org](https://www.python.org/downloads/) dan yuklab oling.

## ✅ 2-Qadam: Loyihani yuklab olish

```bash
git clone https://github.com/Naruto-shippuden00/davomat.git
cd davomat
```

## ✅ 3-Qadam: Virtual environment yaratish (tavsiya etiladi)

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

## ✅ 4-Qadam: Kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

## ✅ 5-Qadam: Bot Token olish

### 5.1. @BotFather ga murojaat qiling

1. Telegram'da [@BotFather](https://t.me/BotFather) botini oching
2. `/newbot` buyrug'ini yuboring
3. Bot nomini kiriting (masalan: "Maktab Davomat")
4. Bot username ni kiriting (masalan: "maktab_davomat_bot")
5. Olingan tokenni nusxalang

**Misol token:**
```
7123456789:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw
```

### 5.2. O'z Telegram ID ni aniqlash

1. Telegram'da [@userinfobot](https://t.me/userinfobot) botini oching
2. `/start` yuboring
3. `Id:` qatoridagi raqamni nusxalang

**Misol:**
```
Id: 123456789
```

## ✅ 6-Qadam: .env faylini sozlash

```bash
# .env faylini yaratish
cp .env.example .env
```

`.env` faylini tahrirlang:

```env
BOT_TOKEN=7123456789:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw
DATABASE_URL=sqlite+aiosqlite:///./data/davomat.db
ADMIN_TELEGRAM_ID=123456789
```

⚠️ **MUHIM**: `BOT_TOKEN` va `ADMIN_TELEGRAM_ID` ni o'z qiymatlaringizga almashtiring!

## ✅ 7-Qadam: Test ma'lumotlarini yaratish

### 7.1. init_data.py faylini tahrirlash

`init_data.py` faylini oching va quyidagi telegram ID larni o'zingiznikiga o'zgartiring:

```python
# Admin foydalanuvchi
admin = User(
    telegram_id=123456789,  # BU YERGA O'Z ID INGIZNI KIRITING!
    ...
)

# Sinf rahbari
class_teacher = User(
    telegram_id=987654321,  # Agar sinf rahbarisi bo'lsangiz
    ...
)

# O'qituvchi
teacher = User(
    telegram_id=111222333,  # Agar o'qituvchi bo'lsangiz
    ...
)

# Ota-onalar
parent1 = User(
    telegram_id=444555666,  # Agar ota-ona bo'lsangiz
    ...
)
```

### 7.2. Ma'lumotlar bazasini yaratish

```bash
python init_data.py
```

**Natija:**
```
Ma'lumotlar bazasini tozalash va qayta yaratish...
Test ma'lumotlarini qo'shish...
✅ Test ma'lumotlari muvaffaqiyatli yaratildi!

📝 Test foydalanuvchilar:
Admin: telegram_id=123456789
Sinf rahbari: telegram_id=987654321
...
```

## ✅ 8-Qadam: Botni ishga tushirish

```bash
python main.py
```

**To'g'ri ishlab turgan bot:**
```
2024-01-15 10:30:45,123 - __main__ - INFO - Ma'lumotlar bazasini ishga tushirish...
2024-01-15 10:30:45,456 - __main__ - INFO - Ma'lumotlar bazasi tayyor!
2024-01-15 10:30:45,789 - __main__ - INFO - Bot ishga tushmoqda...
```

## ✅ 9-Qadam: Botni test qilish

1. Telegram'da botni oching (username orqali)
2. `/start` buyrug'ini yuboring
3. Sizning rolga qarab menyular ochiladi:
   - Admin: Barcha funksiyalar
   - O'qituvchi: Davomat va hisobotlar
   - Ota-ona: Farzand davomati

## 🎯 Tez Test

### O'qituvchi sifatida test:

```
1. "📅 Davomat boshlash" tugmasini bosing
2. Sinf tanlang (masalan: 9-A)
3. Fan tanlang (masalan: Matematika)
4. O'quvchilarni tanlang va holatni belgilang
5. "💾 Saqlash" tugmasini bosing
```

### Ota-ona sifatida test:

```
1. "📊 Farzandim davomati" tugmasini bosing
2. Statistikani ko'ring
```

## 🐛 Xatolarni tuzatish

### Bot ishlamayapti?

**1. Token xatosi:**
```
telegram.error.InvalidToken: Invalid token
```
✅ `.env` faylidagi `BOT_TOKEN` ni tekshiring

**2. Python versiya xatosi:**
```
SyntaxError: ...
```
✅ Python versiyani tekshiring: `python3 --version` (3.9+ kerak)

**3. Kutubxona xatosi:**
```
ModuleNotFoundError: No module named 'telegram'
```
✅ Kutubxonalarni qayta o'rnating: `pip install -r requirements.txt`

**4. Ma'lumotlar bazasi xatosi:**
```
sqlalchemy.exc.OperationalError: ...
```
✅ `data/` papkasini o'chirib, `python init_data.py` ni qayta ishga tushiring

### Bot javob bermayapti?

1. ✅ Bot @BotFather da faolmi? (`/mybots` -> botingiz -> `API Token`)
2. ✅ `init_data.py` da telegram ID to'g'ri kiritilganmi?
3. ✅ Bot dan `/start` bosganmisiz?

### Ma'lumotlar bazasini qayta yaratish:

```bash
rm -rf data/
python init_data.py
```

## 🎓 Keyingi Qadamlar

- [ ] `init_data.py` ga ko'proq o'quvchilar qo'shing
- [ ] Ko'proq fanlar va sinflar yarating
- [ ] Ota-onalarni qo'shing va ularga test xabarlar yuboring
- [ ] Haftalik hisobotlarni tekshiring

## 📞 Yordam

Muammo yechilmasa:
- GitHub Issues: [github.com/Naruto-shippuden00/davomat/issues](https://github.com/Naruto-shippuden00/davomat/issues)
- README.md: To'liq qo'llanma uchun

---

**✨ Muvaffaqiyatlar! Botingiz tayyor!** 🎉
