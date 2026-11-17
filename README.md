# ⚡ ElektroLearn — Avtomatlashtirilgan Aqlli Agent va Bilimlar Bazasi Tizimi

**ElektroLearn** platformasi (`https://elektrolearn-mobile.uzbekistonmet.uz`) uchun to'liq tahlil qilingan API mijozi, normativ hujjatlarga asoslangan semantik qidiruv, Telegram orqali real-vaqtda boshqaruv va xavfsiz avtomatlashtirilgan test yechish tizimi.

---

## 📋 Mundarija
- [Loyiha haqida](#-loyiha-haqida)
- [Arxitektura va Fayllar Strukturasi](#-arxitektura-va-fayllar-strukturasi)
- [Asosiy Imkoniyatlar](#-asosiy-imkoniyatlar)
- [Xavfsizlik va Maxfiylik](#-xavfsizlik-va-maxfiylik)
- [O'rnatish va Sozlash](#-ornatish-va-sozlash)
- [Ishga Tushirish va Foydalanish](#-ishga-tushirish-va-foydalanish)
- [Telegram Bot Integratsiyasi](#-telegram-bot-integratsiyasi)
- [Kengaytirilgan Skriptlar](#-kengaytirilgan-skriptlar)

---

## 🔍 Loyiha haqida

Ushbu tizim O'zbekiston Milliy Elektr Tarmoqlari xodimlari uchun mo'ljallangan ElektroLearn tizimida:
- O'quv darajalaridagi testlar va nazariy materiallarni avtomatlashtirilgan tahlil qilish;
- 100% ishonchli va tekshirilgan to'g'ri javoblarni o'zida saqlovchi **Bilimlar Bazasi (Knowledge Base)** shakllantirish;
- Normativ-huquqiy hujjatlar (TEQQ, XTQ, PUE, VMQ-711, VMQ-608, 374, 1193) bo'yicha to'g'ri javobni avtomatik topish;
- Jon (Energy) zaxirasini ehtiyot qilib, xato variantlarni tavakkal tanlamasdan, insoniy kechikishlar bilan ishlashni ta'minlaydi.

---

## 📁 Arxitektura va Fayllar Strukturasi

Loyiha qat'iy modulyar, toza va kengaytiriluvchan Clean Architecture tamoyillari asosida tuzilgan:

```
ElektroLearn/
├── config.py                 # Markaziy konfiguratsiya (.env va tizim sozlamalari)
├── auth_manager.py           # Token muddatini tekshirish va avto-login menejeri
├── main.py                   # Asosiy konsol (CLI) boshqaruv paneli
├── autopilot.py              # Avtonom test yechish agenti (jon himoyasi bilan)
├── daily_solver.py           # Kunlik rejalarni avtomatik bajarish moduli
├── telegram_bot.py           # Telegram Q&A va monitoring boti
├── library_searcher.py       # Normativ hujjatlardan semantik qidiruvchi
├── requirements.txt          # Python kutubxonalari
├── .env.example              # Muhit o'zgaruvchilari andozasi
├── .gitignore                # Maxfiy ma'lumotlar va kesh filtri
├── START_AUTOPILOT.bat       # Windows avtopilot tezkor ishga tushirgich
├── STOP_AUTOPILOT.bat        # Windows avtopilot to'xtatgich
│
├── api/                      # Backend API mijoz qatlami (REST Client)
│   ├── __init__.py           # ElektroLearnClient yagona nuqtasi
│   ├── base.py               # Asosiy BaseAPI va Session menejeri
│   ├── client.py             # HTTP so'rovlar, headerlar va xatoliklar filtri
│   ├── auth.py               # Autentifikatsiya va foydalanuvchi profili
│   ├── progress.py           # Darajalar, testlar va mavzular API (/progress/*)
│   ├── daily_plan.py         # Kunlik vazifalar API (/mobile/daily-plan/*)
│   ├── exam.py               # Jonli imtihonlar API (/exams/live/*)
│   └── leaderboard.py        # Foydalanuvchilar reytingi (/leaderboard/*)
│
├── models/                   # Typed ma'lumotlar modellari (Dataclasses)
│   ├── __init__.py
│   ├── question.py           # Question, Option, AnswerResult modellari
│   ├── theory.py             # Theory, Level, Module modellari
│   └── user.py               # UserProfile, UserStats modellari
│
├── agent/                    # Aqlli Agent va Qaror Qabul Qilish Qatlami
│   ├── __init__.py
│   ├── knowledge_base.py     # O'rganilgan to'g'ri javoblar bazasi menejeri
│   ├── telegram_qa.py        # Bot orqali noaniq savollarni adminga yo'llash
│   ├── solver.py             # Semantik va kontekstual tahlil qiluvchi
│   └── runner.py             # Test yechish navbati va strategiyalari
│
├── data/                     # Ma'lumotlar va bilimlar bazasi
│   ├── knowledge_base.json   # 100% tasdiqlangan to'g'ri javoblar bazasi
│   ├── full_theory_database.json # Barcha nazariy qoidalar arxivi
│   ├── all_500_questions.json    # 500 talik savollar bazasi
│   ├── library/              # Normativ qonun va nizomlarning asl PDF hujjatlari
│   └── library_extracted/    # PDF lardan ajratib olingan toza matnlar
│
├── scripts/                  # Yordamchi va diagnostik vositalar
│   ├── probes/               # API, kutubxona va progress tekshiruv skriptlari
│   └── solvers/              # Alohida daraja va modullarni sinovchi skriptlar
│
└── docs/                     # Loyiha hujjatlari va spetsifikatsiyalar
    └── API_SPECIFICATION.md  # Barcha aniqlangan endpointlar tavsifi
```

---

## ⚡ Asosiy Imkoniyatlar

1. **Aqlli Bilimlar Bazasi (Knowledge Base):**
   - Har bir to'g'ri yechilgan savol savol matni, variant matni va uning `correctOptionId`si bilan avtomatik saqlanadi.
   - Baza hash va fuzzy-matching orqali savoldagi kichik farqlarni (probel, katta-kichik harf) e'tiborga oladi.
2. **Jon (Heart / Energy) Himoyasi:**
   - Serverda foydalanuvchining 5 ta joni mavjud. Noto'g'ri javob 1 ta jonni yo'qotadi.
   - Agent javobdan 100% amin bo'lmasa, **aslo tavakkal qilmaydi**. Savolni Telegram bot orqali adminga yo'llaydi yoki jon 0 bo'lib qolmasligi uchun jarayonni xavfsiz to'xtatadi.
3. **Inson kabi tabiiy harakat (Human-like Delays):**
   - Savollar oralig'ida 3-7 soniyalik tasodifiy kechikishlar bilan javob beriladi, bu server tomonidan bot sifatida bloklanish xavfini bartaraf etadi.
4. **Kutubxona va Normativ Hujjatlar bilan Integratsiya:**
   - O'zbekiston energetika qoidalariga oid barcha rasmiy PDF hujjatlar matnga aylantirilgan bo'lib, noma'lum savollarning kalit so'zlari bo'yicha qonun moddalaridan to'g'ridan-to'g'ri javob topiladi.

---

## 🔐 Xavfsizlik va Maxfiylik

- Loyiha kod bazasida **hech qanday ochiq token yoki parol saqlanmaydi**.
- Barcha hisob ma'lumotlari faqat maxalliy `.env` faylida saqlanadi.
- `.gitignore` barcha maxfiy kalitlar (`.env`), shaxsiy loglar (`*.log`) va vaqtinchalik ma'lumotlarni Git repozitoriysiga tushishidan to'liq himoya qiladi.

---

## 🛠 O'rnatish va Sozlash

### 1. Repozitoriyni klonlash
```bash
git clone https://github.com/<username>/ElektroLearn.git
cd ElektroLearn
```

### 2. Virtual muhitni yaratish va faollashtirish
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 3. Bog'liqliklarni o'rnatish
```bash
pip install -r requirements.txt
```

### 4. Konfiguratsiya faylini sozlash
`.env.example` faylidan nusxa olib, `.env` faylini yarating:
```bash
cp .env.example .env
```
`.env` faylini ochib, kerakli parametrlarni kiriting:
```ini
ELEKTROLEARN_BASE_URL=https://elektrolearn-mobile.uzbekistonmet.uz/api
ELEKTROLEARN_USERNAME=your_username
ELEKTROLEARN_PASSWORD=your_password
ELEKTROLEARN_TOKEN=your_jwt_token_here

TELEGRAM_BOT_TOKEN=your_telegram_bot_token
ADMIN_CHAT_ID=your_telegram_chat_id
```

---

## 🚀 Ishga Tushirish va Foydalanish

### 1. Umumiy Holatni Ko'rish (CLI)
Foydalanuvchi profili, tajriba ballari (XP), darajalar va jonlar miqdorini ko'rish:
```bash
python main.py --status
```

### 2. Kunlik Rejani Bajarish
Bugungi kunga berilgan kunlik topshiriqlar va darslarni avtomatik bajarish:
```bash
python main.py --plan
```

### 3. Muayyan Daraja yoki Modulni Yechish
```bash
python main.py --level <LEVEL_ID>
```

### 4. Avtopilot Rejimi
Jonlarni monitoring qilib, tinimsiz avtomatik test yechish va darajalarni ochish:
```bash
python autopilot.py
```
*(Windows foydalanuvchilari `START_AUTOPILOT.bat` faylini ikki marta bosib ishga tushirishlari mumkin).*

---

## 🤖 Telegram Bot Integratsiyasi

Tizim Telegram bot orqali to'liq masofadan boshqariladi:
```bash
python telegram_bot.py
```

**Bot imkoniyatlari:**
- `/status` — Jonlar holati, joriy ball va ochiq darajalar haqida tezkor hisobot;
- `/solve` — Avtopilotni bot orqali boshlash;
- `/stop` — Jarayonni to'xtatish;
- **Jonli Savol-Javob:** Baza topa olmagan noaniq savol paydo bo'lganda, bot variantlarni tugma ko'rinishida adminga yuboradi. Admin to'g'ri variantni tanlashi bilan tizim javob beradi va ushbu savolni o'zining Bilimlar Bazasiga saqlab oladi.

---

## 📊 Kengaytirilgan Skriptlar

- `scripts/probes/check_progress.py` — Foydalanuvchining barcha darajalar bo'yicha foizlarini tekshirish;
- `scripts/probes/analyze_energy.py` — Jonlarning tiklanish vaqtini sekundigacha hisoblash;
- `scripts/solvers/sync_knowledge_base.py` — Barcha savollar bazasi bilan bilimlar bazasini solishtirish va to'ldirish.

---

## 📄 Litsenziya va Ogohlantirish
Ushbu loyiha o'quv va ta'lim jarayonlarini tadqiq qilish, bilim darajasini avtomatlashtirilgan tahlil qilish maqsadida yaratilgan. Tizimdan mas'uliyat bilan va xizmat ko'rsatish qoidalariga rioya qilgan holda foydalaning.
