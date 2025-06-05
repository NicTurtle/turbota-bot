# TurbotaBot

**TurbotaBot** is an AI-powered Telegram chatbot designed to provide emotional support to Ukrainians who may not have access to professional psychological care.

### 💡 Project Description

TurbotaBot connects GPT-based intelligence with Telegram to offer 24/7 empathy-driven conversation and basic mental support — not a replacement for therapy, but a warm companion for hard times.

### 🧠 Features

- Asynchronous Telegram bot (aiogram)
- GPT-4o integration for dialogue
- SQLite for message history
- FastAPI as application backend
- Ready for future Stripe integration (donations/payments)

### 🛠️ Tech Stack

- Python 3.11+
- FastAPI
- aiogram
- OpenAI API
- SQLite
- python-dotenv

### 🚀 Getting Started

1. Clone the repo:
    ```bash
    git clone https://github.com/NicTurtle/turbotabot.git
    cd turbotabot
    ```

2. Create virtual environment and install dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. Create `.env` file:
    ```
    TELEGRAM_TOKEN=your_telegram_bot_token
    OPENAI_API_KEY=your_openai_key
    ```

4. Run the bot locally:
    ```bash
    uvicorn turbota_app.main:app --reload
    ```

### 📌 Disclaimer

TurbotaBot is not a licensed therapist. It is an AI-powered assistant aimed at emotional relief and connection.

---

### ⚖️ License & Usage

This project is published **strictly for educational and demonstration purposes**.  
All code, logic, and structure belong to the author.

> ❗️Copying, reproducing, or using this code for commercial products is **not allowed**.

If you want to use parts of this project, please contact the author for permission.


## 🇺🇦 Ukrainian version — `README.uk.md`