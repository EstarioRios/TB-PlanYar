from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
import requests
import json

API_BASE_URL = "http://localhost:8000/api"

user_states = {}


def setup_group_handlers(app: Client):
    @app.on_message(filters.command("start") & filters.group)
    async def group_start_handler(client: Client, message: Message):
        chat_id = message.chat.id

        response = requests.get(
            f"{API_BASE_URL}/plans/by-group/",
            params={"chat_group_id_code": chat_id},
        )

        if response.status_code == 200:
            await message.reply("✅ یک پلن برای این گروه وجود دارد.")
        else:
            await message.reply(
                "❗️هیچ پلنی برای این گروه ثبت نشده.\nآیا مایل به ایجاد یک پلن جدید هستید؟",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "📝 ایجاد پلن جدید",
                                callback_data=f"create_plan:{chat_id}",
                            )
                        ]
                    ]
                ),
            )

    @app.on_callback_query(filters.regex(r"^create_plan:\-?\d+$"))
    async def create_plan_callback_handler(
        client: Client, callback_query: CallbackQuery
    ):
        chat_id = int(callback_query.data.split(":")[1])
        user_id = callback_query.from_user.id

        user_states[user_id] = {
            "step": "awaiting_title",
            "chat_id": chat_id,
            "data": {},
        }

        await callback_query.message.reply("لطفاً عنوان پلن را وارد کنید:")
        await callback_query.answer()

    @app.on_message(filters.group & filters.text)
    async def collect_plan_data_handler(client: Client, message: Message):
        user_id = message.from_user.id
        if user_id not in user_states:
            return

        state = user_states[user_id]
        step = state["step"]
        chat_id = state["chat_id"]

        if step == "awaiting_title":
            state["data"]["title"] = message.text
            state["step"] = "awaiting_description"
            await message.reply("توضیحات پلن را وارد کنید:")

        elif step == "awaiting_description":
            state["data"]["description"] = message.text
            state["step"] = "awaiting_users"
            await message.reply(
                "لطفاً لیست کاربران و وظایف آن‌ها را به صورت JSON وارد کنید:\n\n"
                '{"1": {"id_code": 12345, "action_title": "وظیفه ۱", "action_description": "توضیح وظیفه"},\n'
                ' "2": {"id_code": 67890, "action_title": "وظیفه ۲", "action_description": "توضیح وظیفه"}}'
            )

        elif step == "awaiting_users":
            try:
                users = json.loads(message.text)
                state["data"]["users"] = users
                state["step"] = "done"

                payload = {
                    "title": state["data"]["title"],
                    "description": state["data"]["description"],
                    "users": users,
                    "creator_id_code": user_id,
                    "chat_group_id_code": chat_id,
                }

                response = requests.post(
                    f"{API_BASE_URL}/plans/create/",
                    json=payload,
                )

                if response.status_code == 201:
                    await message.reply("✅ پلن با موفقیت ایجاد شد!")
                else:
                    await message.reply(
                        f"❌ ایجاد پلن با خطا مواجه شد:\n{response.json().get('error', 'خطای نامشخص')}"
                    )

            except Exception:
                await message.reply("فرمت وارد شده نامعتبر است. لطفاً دوباره تلاش کنید.")

            user_states.pop(user_id, None)

    @app.on_message(filters.command("plan") & filters.group)
    async def show_plan_handler(client: Client, message: Message):
        chat_id = message.chat.id

        response = requests.get(
            f"{API_BASE_URL}/plans/by-group/",
            params={"chat_group_id_code": chat_id},
        )

        if response.status_code != 200:
            await message.reply("❌ هیچ پلنی برای این گروه تعریف نشده است.")
            return

        plan_id = response.json()["plan_id"]

        response = requests.get(
            f"{API_BASE_URL}/plans/details/",
            params={"plan_id": plan_id},
        )

        if response.status_code != 200:
            await message.reply("❌ دریافت اطلاعات پلن با خطا مواجه شد.")
            return

        data = response.json()
        plan_info = (
            f"📋 *عنوان:* {data['plan_title']}\n"
            f"📝 *توضیحات:* {data['plan_description']}\n"
            f"📊 *وضعیت پلن:* {data['plan_status']}\n\n"
            f"👥 *کاربران:*\n"
        )

        user_id = message.from_user.id
        user_buttons = []

        for user in data["users"]:
            status_emoji = "✅" if user["action_status"] == "finished" else "⏳"
            plan_info += (
                f"- `{user['id_code']}` → {user['action_title']} {status_emoji}\n"
            )

            if (
                str(user["id_code"]) == str(user_id)
                and user["action_status"] == "active"
            ):
                user_buttons.append(
                    InlineKeyboardButton(
                        "✅ انجام شد", callback_data=f"finish_action:{plan_id}"
                    )
                )

        markup = InlineKeyboardMarkup([user_buttons]) if user_buttons else None

        await message.reply(plan_info, reply_markup=markup, parse_mode="Markdown")

    @app.on_callback_query(filters.regex(r"^finish_action:\d+$"))
    async def finish_action_handler(client: Client, callback_query: CallbackQuery):
        user_id = callback_query.from_user.id
        plan_id = callback_query.data.split(":")[1]

        response = requests.put(
            f"{API_BASE_URL}/actions/finish/",
            params={"id_code": user_id, "plan_id": plan_id},
        )

        if response.status_code == 200:
            await callback_query.message.edit_text("✅ وظیفه شما با موفقیت ثبت شد.")
        else:
            error = response.json().get("error", "خطای نامشخص")
            await callback_query.message.reply(f"❌ خطا: {error}")

        await callback_query.answer()
