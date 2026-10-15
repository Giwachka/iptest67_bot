import asyncio
import json
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

BOT_TOKEN = "8853343511:AAHa-qihnJulCYenM3PDyop85ZhLFIQZ_WY"
WEBAPP_URL = "https://giwachka.github.io/ipapp/index.html"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🔍 Открыть мини-приложение",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )]
    ])
    await message.answer(
        "Привет! Нажми кнопку ниже, чтобы узнать свой IP.",
        reply_markup=kb
    )


@dp.message(F.web_app_data)
async def handle_webapp(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        ip = data.get("ip", "неизвестен")
        city = data.get("city", "—")
        country = data.get("country", "—")
        org = data.get("org", "—")

        await message.answer(
            f"🌐 Твой IP: `{ip}`\n"
            f"📍 Город: {city}\n"
            f"🏳️ Страна: {country}\n"
            f"📡 Провайдер: {org}",
            parse_mode="Markdown"
        )
    except Exception as e:
        await message.answer(f"Ошибка: {e}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
