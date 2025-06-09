# TurbotaBot

**TurbotaBot** is an AI-powered Telegram chatbot that provides emotional support to Ukrainians affected by war, anxiety, and personal hardships.  
It uses the OpenAI Assistant API with thread-based memory to deliver consistent, empathetic, and helpful conversations directly in Telegram.

---

## 💡 Project Overview

TurbotaBot is **not a licensed therapist**, but a warm and anonymous companion built to offer 24/7 support to those who may not have access to professional help.  
It listens attentively, asks thoughtful questions, and gently guides users with practical psychological advice.

---

## 🧠 Key Features

- Telegram chatbot built with **Aiogram**
- Integration with **OpenAI Assistant API** (`gpt-4o-mini`)
- Persistent assistant + thread memory per user
- SQLite for storing assistant/thread/user data
- FastAPI backend for API and webhook management
- Fully asynchronous architecture
- Ready for **Stripe integration** (donations/freemium)

---

## 🛠️ Tech Stack

- Python 3.11+
- FastAPI
- Aiogram
- OpenAI Assistant API
- SQLite (`aiosqlite`)
- python-dotenv

---

## 📁 Project Structure

```
turbota_bot/
└── turbota_app/
    ├── main.py               # Launches FastAPI and aiogram bot
    ├── routers/
    │   └── base.py           # API routes (e.g., assistant endpoint)
    ├── schemas/
    │   ├── gpt.py            # Pydantic models for GPT assistant
    │   └── users.py          # Pydantic models for user data
    ├── services/
    │   ├── bot.py            # Aiogram logic and handlers
    │   ├── gpt.py            # Assistant API integration
    │   ├── database.py       # SQLite database logic
    │   └── config.py         # Loads environment config
├── psychologist.db           # Local SQLite DB (autocreated)
├── .env                      # API keys and tokens
├── requirements.txt          # Dependencies
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/NicTurtle/turbotabot.git
cd turbotabot
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` File

```env
TELEGRAM_TOKEN=your_telegram_bot_token
OPENAI_API_KEY=your_openai_api_key
```

### 5. Run the Bot

```bash
uvicorn turbota_app.main:app --reload
```

---

## ⚠️ Disclaimer

TurbotaBot is not a licensed therapist or medical service.  
It provides general emotional support only.  
If you’re experiencing a mental health crisis, please contact a qualified professional or local helpline.

---

## 📜 License & Usage

This project is released **for educational and demonstration purposes only**.  
Commercial use or redistribution is prohibited without explicit permission.

> Contact the author directly if you want to adapt or reuse this project.
