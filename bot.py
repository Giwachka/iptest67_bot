import asyncio
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

# ==== НАСТРОЙКИ ====
BOT_TOKEN = "8853343511:AAHa-qihnJulCYenM3PDyop85ZhLFIQZ_WY"
WEBAPP_URL = "https://giwachka.github.io/ipapp/index.html"
# ===================

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message):
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

        lines = []

        # Telegram
        lines.append("👤 *Ваш Telegram*")
        if data.get('tg_first_name'):
            lines.append(f"• Имя: {data['tg_first_name']} {data.get('tg_last_name', '')}")
        if data.get('tg_username'):
            lines.append(f"• Username: @{data['tg_username']}")
        if data.get('tg_language'):
            lines.append(f"• Язык: {data['tg_language']}")
        if data.get('tg_premium'):
            lines.append(f"• Premium: Да ⭐")
        if data.get('tg_id'):
            lines.append(f"• Telegram ID: `{data['tg_id']}`")

        # IP
        lines.append("\n🌐 *IP-адрес*")
        for key, label in [('ip', 'IP'), ('hostname', 'Хостнейм'), ('type', 'Тип')]:
            if data.get(key):
                lines.append(f"• {label}: `{data[key]}`")

        # Гео
        lines.append("\n📍 *Геолокация*")
        if data.get('country'):
            flag = ''.join(chr(127397 + ord(c)) for c in data['country'].upper())
            lines.append(f"• Страна: {flag} {data['country']}")
        for key, label in [('region', 'Регион'), ('city', 'Город'),
                            ('postal', 'Индекс'), ('loc', 'Координаты'),
                            ('timezone', 'Часовой пояс')]:
            if data.get(key):
                lines.append(f"• {label}: {data[key]}")

        # Сеть
        lines.append("\n📡 *Сеть*")
        for key, label in [('org', 'Провайдер'), ('asn', 'ASN'),
                            ('asn_name', 'Название ASN'), ('asn_domain', 'Домен ASN'),
                            ('asn_type', 'Тип ASN')]:
            if data.get(key):
                lines.append(f"• {label}: {data[key]}")

        # Доп
        extras = []
        if data.get('mobile'): extras.append('Мобильный')
        if data.get('hosting'): extras.append('Хостинг')
        if data.get('anycast'): extras.append('Anycast')
        if data.get('bogon'): extras.append('Bogon')
        if extras:
            lines.append("\n🔍 *Дополнительно*")
            lines.append("• " + ', '.join(extras))

        await message.answer("\n".join(lines), parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")


# Удаляем сервисные сообщения о закреплении в ЛИЧКЕ С БОТОМ
@dp.message(F.pinned_message)
async def delete_pin_notifications(message: types.Message):
    try:
        await message.delete()
    except Exception:
        pass


async def main():
    print("Бот запущен")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
