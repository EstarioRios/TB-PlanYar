# 🤖 PlanYar - A Telegram Bot Backed by Django

**PlanYar** is a modular and clear Telegram bot backend, built entirely with Django.  
Designed for simplicity, speed, and internal-only logic — there's no need for frontend clients, no authentication complexity, and no external API consumers. Everything works internally and efficiently.

---

## 🧠 About the Project

PlanYar is a backend system for a Telegram bot that interacts directly with Django through internal logic.  
The bot itself (written in `telegrambot.py`) acts as the only client, communicating via local requests. This architecture removes the need for serializers, authentication systems for APIs, or user-facing security layers — everything stays in your control.

This structure is perfect when:

- Your bot and server logic are hosted together
- No external frontend/mobile apps are involved
- You want clean separation between logic layers (e.g., authentication, bot engine)
- You prefer Django’s ecosystem over microframeworks

---

## 📂 Project Structure
```
project_root/
├── AuthenticationSystem/ # Handles user models, login logic, internal user processing
├── BotCore/ # (Or TeleOps / TeloCore) — main logic of the bot's commands and actions
├── telegrambot.py # Telegram bot file interacting directly with Django endpoints
├── manage.py
└── requirements.txt
```
```yaml
Copy
Edit
```

---

## ⚙️ Technologies Used

- 🐍 Python 3.x
- 🧱 Django (no DRF needed)
- 📡 python-telegram-bot (or Telethon / Aiogram — depending on your preference)
- 🐧 Localhost / Linux-first development

---

## 🔒 No Authentication? Why?

Yes! This bot runs locally and acts as its **own client**.  
There's no need for JWT, OAuth, or REST API consumers. This keeps the logic simple, fast, and Pythonic — with no overhead from typical frontend/backend separation.

---

## 🛠 Setup & Run

```bash
git clone https://github.com/YourUsername/PlanYar.git
cd PlanYar

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Django server
python manage.py runserver
```

# In a separate terminal, run the bot
python telegrambot.py
📌 Notes
This bot is not designed for public API exposure — it's fast, local, and focused.

You can modularize your Django apps further by purpose (e.g., AnalyticsModule, ContentManager, etc.)

Ideal for devs who love Django but don’t need DRF or microservice complexity

💡 Name Meaning
PlanYar
A combination of the word "Plan" (as in scheduling, action, or strategy)
and "Yar" (یار), the Persian word for helper/assistant.
It’s your assistant in running structured logic through Telegram.

📄 License
This project is open-source and available under the MIT License.


---

## A Gift For You From Abolfazl 😉 
