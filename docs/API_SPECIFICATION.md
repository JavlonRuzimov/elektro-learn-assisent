# ElektroLearn Mobile API To'liq Hujjatlari va Arxitekturasi

Ushbu hujjat `https://elektrolearn-mobile.uzbekistonmet.uz` platformasining barcha backend API endpointlari, autentifikatsiya sxemasi, so'rov va javob modellari bo'yicha to'liq tahlilni o'z ichiga oladi.

---

## 1. Umumiy Ma'lumot va Autentifikatsiya

- **Base URL:** `https://elektrolearn-mobile.uzbekistonmet.uz/api`
- **Frontend URL:** `https://elektrolearn-mobile.uzbekistonmet.uz`
- **Auth turi:** Bearer JWT Token
- **Header:**
  ```http
  Authorization: Bearer <JWT_ACCESS_TOKEN>
  Content-Type: application/json
  Accept: application/json
  ```
- **Token muddati va yangilash:** JWT muddati tugaganda `POST /api/auth/refresh` orqali yangilanadi (`refreshToken`).

---

## 2. Autentifikatsiya va Profil Endpointlari

### `GET /api/auth/me`
Joriy tizimga kirgan foydalanuvchi ma'lumotlarini qaytaradi.
- **Javob:**
  ```json
  {
    "id": "37287c6f-a150-487e-9afc-b787701212a7",
    "email": "s.ruzimov2774",
    "firstName": "Sabirjan",
    "lastName": "Ruzimov",
    "middleName": "Qodamjanovich",
    "role": "USER",
    "avatarUrl": null,
    "organizationIds": ["bc6c7a4f-b739-4142-897e-e4f572d800d5"],
    "organizations": [
      {
        "id": "bc6c7a4f-b739-4142-897e-e4f572d800d5",
        "name": "XORAZM MAGISTRAL ELEKTR TARMOQLARI FILIALI"
      }
    ],
    "mustChangePassword": false,
    "energoId": "35db0681-e448-46de-8785-897f5252cb72"
  }
  ```

### `POST /api/auth/login`
Parol va login orqali kirish.
- **Body:** `{"login": "...", "email": "...", "password": "..."}`

### `POST /api/auth/refresh`
Tokenni yangilash.
- **Body:** `{"refreshToken": "..."}`

### `POST /api/user-activity/heartbeat`
Foydalanuvchi tizimda faol ekanligini bildirish (ping/heartbeat).
- **Body:** `{}`

---

## 3. O'rganish va Darajalar (Progress & Levels)

### `GET /api/progress/me`
Foydalanuvchining umumiy balli (XP), unvoni va barcha mavjud darajalar ro'yxati.
- **Javob namunasi:**
  ```json
  {
    "totalXp": 300,
    "completedLevels": 0,
    "badge": { "label": "Yangi ishchi", "bolts": 1 },
    "levels": [
      {
        "id": "3ad50502-c9bf-462d-ba09-c870e96bd361",
        "title": "Хавфсизлик техникаси коидалари.",
        "orderIndex": 4,
        "isLocked": false,
        "isCompleted": false,
        "completionPercent": 59,
        "correctAnswersCount": 34,
        "attemptsCount": 35
      }
    ]
  }
  ```

### `GET /api/progress/level/{level_id}`
Muayyan daraja ichidagi nazariy mavzular (Theories) ro'yxatini qaytaradi.
- **Javob namunasi:**
  ```json
  {
    "id": "3ad50502-c9bf-462d-ba09-c870e96bd361",
    "title": "Хавфсизлик техникаси коидалари.",
    "theories": [
      {
        "id": "3b49aa4a-1d01-4f2d-838b-1c385953e1fa",
        "title": "Наряд-ижозат ",
        "content": "Ишнинг мазмуни, жойи, уни бошлаш ва тамомлаш вақтларини...",
        "orderIndex": 0,
        "totalQuestions": 9,
        "answeredQuestions": 9
      }
    ]
  }
  ```

### `GET /api/theories/{theory_id}/questions?mode=continue`
Nazariy mavzuga tegishli savollar va ularning variantlarini olish (`mode`: `continue` yoki `retry`).
- **Javob:**
  ```json
  {
    "mode": "continue",
    "totalQuestions": 10,
    "answeredCount": 4,
    "remainingCount": 6,
    "isModuleComplete": false,
    "questions": [
      {
        "id": "f889afef-dffd-47e5-9e9e-51c6867b6b44",
        "prompt": "Himoya vositalarini tayyorlash, sinash va ishlatish nimaga muvofiq amalga oshiriladi?",
        "type": "SINGLE_CHOICE",
        "orderIndex": 23,
        "options": [
          { "id": "37cf52e4-...", "optionText": "Texnik shartlar...", "orderIndex": 0 }
        ]
      }
    ]
  }
  ```

### `POST /api/progress/answer`
Oddiy tanlovli savolga (`SINGLE_CHOICE`) javob jo'natish.
- **Body:**
  ```json
  {
    "questionId": "f889afef-dffd-47e5-9e9e-51c6867b6b44",
    "selectedOptionId": "da7c23c7-96ee-45ec-8f8c-15397e2cb036",
    "source": "LESSON"
  }
  ```
- **Javob:**
  ```json
  {
    "isCorrect": true,
    "correctOptionId": "da7c23c7-96ee-45ec-8f8c-15397e2cb036",
    "xpEarned": 10,
    "xpMessage": "+10 XP",
    "hearts": 5,
    "planCorrectCount": 10
  }
  ```
  *(Eslatma: Noto'g'ri tanlanganda ham server `correctOptionId` maydonida haqiqiy to'g'ri variant IDsini qaytaradi! Agent buni darhol o'z bilimlar bazasiga saqlaydi).*

### `POST /api/progress/matching`
Moslashtirish savollariga (`MATCHING`) javob berish.
- **Body:**
  ```json
  {
    "questionId": "...",
    "pairs": [
      { "leftOptionId": "...", "rightOptionId": "..." }
    ],
    "source": "LESSON"
  }
  ```

---

## 4. Kunlik Reja (Daily Plan)

### `GET /api/mobile/daily-plan/today`
Bugungi 10 talik reja holati.
- **Javob:**
  ```json
  {
    "planDate": "2026-11-13",
    "targetQuestions": 10,
    "dailyGoalCorrect": 10,
    "isPlanDay": true,
    "answeredCount": 10,
    "correctCount": 10,
    "wrongCount": 0,
    "completionPercent": 100,
    "completed": true
  }
  ```

### `GET /api/mobile/daily-plan/next-question`
Kunlik rejadagi navbatdagi savolni olib kelish.

---

## 5. Reyting (Leaderboard)

- `GET /api/leaderboard/global?limit=50`: Global reyting
- `GET /api/leaderboard/organization?limit=50`: Korxona / filial bo'yicha reyting

---

## 6. Imtihonlar (Live Exams & Proctoring)

- `GET /api/exams/live/me/next`: Rejalashtirilgan imtihon
- `POST /api/exams/live/validate-qr`: QR kod orqali kirish
- `GET /api/exams/live/session/{id}/state`: Imtihon vaqti va holati
- `POST /api/exams/live/session/{id}/verify-code`: Kod bilan tasdiqlash
- `POST /api/exams/live/session/{id}/start-section`: Imtihon qismini boshlash
- `POST /api/exams/live/session/{id}/answer`: Imtihon savoliga javob
- `POST /api/exams/live/session/{id}/submit-section`: Qismni yakunlash

