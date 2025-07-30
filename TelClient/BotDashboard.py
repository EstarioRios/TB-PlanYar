from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup

app = Client(
    "PlanYarBot",
    api_id="YOUR_API_ID",
    api_hash="YOUR_API_HASH",
    bot_token="YOUR_BOT_TOKEN",
)

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [["➕ افزودن به گروه", "📖 راهنمای کارکرد ربات"], ["👨‍💻 درباره توسعه دهنده"]],
    resize_keyboard=True,
)

START_GROUP_LINK = "https://t.me/PlanYarBot?startgroup=add"


@app.on_message(filters.command("start") & filters.private)
def start_handler(client, message):
    welcome_text = (
        "👋 سلام!\n" "به ربات PlanYar خوش آمدید.\n" "لطفاً یک گزینه را انتخاب کنید:"
    )
    message.reply_text(welcome_text, reply_markup=MAIN_KEYBOARD)


@app.on_message(filters.private & filters.regex("➕ افزودن به گروه"))
def add_to_group_handler(client, message):
    text = (
        "🤖 برای افزودن ربات به گروه خود، روی لینک زیر کلیک کنید:\n"
        f"{START_GROUP_LINK}"
    )
    message.reply_text(text)


@app.on_message(filters.private & filters.regex("📖 راهنمای کارکرد ربات"))
def help_handler(client, message):
    help_text = (
        "🛠 ربات PlanYar به شما کمک می‌کند پلن‌ها و وظایف را در گروه‌های تلگرام مدیریت کنید.\n"
        "👥 در گروه، مدیر می‌تواند پلن بسازد و کاربران می‌توانند وظایف خود را مدیریت کنند.\n"
        "🚀 برای شروع، ربات را به گروه خود اضافه کنید و از دستورات آن استفاده کنید."
    )
    message.reply_text(help_text)


@app.on_message(filters.private & filters.regex("👨‍💻 درباره توسعه دهنده"))
def about_dev_handler(client, message):
    about_text = (
        "👨‍💻 ربات PlanYar توسط Abolfazl Khezri توسعه یافته است.\n"
        "📬 برای اطلاعات بیشتر می‌توانید با من تماس بگیرید."
    )
    message.reply_text(about_text)


if __name__ == "__main__":
    app.run()
