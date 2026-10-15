import asyncio
import json
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

BOT_TOKEN = "ТВОЙ_ТОКЕН"
WEBAPP_URL = "https://giwachka.github.io/ipapp/index.html"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    # Reply-клавиатура с Web App (обязательно для работы sendData)
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text="🔍 Узнать IP",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )]
        ],
        resize_keyboard=True
    )
    await message.answer(
        "Привет! Нажми кнопку ниже, чтобы узнать свой IP.",
        reply_markup=kb
    )

@dp.message(F.web_app_data)
async def handle_webapp(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        # Формируем расширенный вывод
        text = (
            f"🌐 *Твой IP:* `{data.get('ip', '—')}`\n"
            f"📍 *Город:* {data.get('city', '—')}\n"
            f"🗺 *Регион:* {data.get('region', '—')}\n"
            f"🏳️ *Страна:* {data.get('country', '—')}\n"
            f"🌍 *Континент:* {data.get('continent', '—')}\n"
            f"📡 *Провайдер:* {data.get('org', '—')}\n"
            f"🕒 *Часовой пояс:* {data.get('timezone', '—')}\n"
            f"📮 *Почтовый индекс:* {data.get('postal', '—')}"
        )
        await message.answer(text, parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
