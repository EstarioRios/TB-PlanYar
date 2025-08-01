from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup
from InfoManager import test_proxies_and_get_client

app = test_proxies_and_get_client()
if (not app) or (app == None):
    print("No proxies found")

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
        "👨‍💻 ربات PlanYar با هدف مدیریت پلن‌ها در گروه‌های تلگرامی توسط *Abolfazl Khezri* توسعه داده شده است.\n\n"
        "📩 جهت ارتباط مستقیم یا پیشنهاد همکاری:\n"
        "✉️ ایمیل: estariorios@gmail.com\n\n"
        "🤝 این ربات آماده جذب اسپانسر یا شریک فنی/مالی می‌باشد.\n"
        "💸 در صورت حمایت مالی (مانند تأمین هزینه‌های سرور)، قابلیت‌های پیشرفته‌تری فعال خواهند شد:\n"
        "✅ ارسال پیام‌های تبلیغاتی هدفمند در گروه‌ها\n"
        "✅ فعال‌سازی نسخه حرفه‌ای ربات\n"
        "✅ توسعه امکانات بیشتر بر اساس نیاز اسپانسر\n\n"
        "📢 فرصت تبلیغات ویژه برای برندها و کسب‌وکارها از طریق ربات فراهم است.\n"
        "اگر تمایل به همکاری یا حمایت دارید، خوشحال می‌شوم از شما بشنوم!"
    )

    message.reply_text(about_text)


@app.on_message(filters.command("menu") & filters.private)
def menu_handler(client, message):
    welcome_text = "این هم از منوی اصلی:"
    message.reply_text(welcome_text, reply_markup=MAIN_KEYBOARD)


if __name__ == "__main__":
    app.run()
