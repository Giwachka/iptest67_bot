import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

BOT_TOKEN = "8853343511:AAHa-qihnJulCYenM3PDyop85ZhLFIQZ_WY"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def get_ip_info(ip: str = ""):
    url = f"https://ipinfo.io/{ip}/json" if ip else "https://ipinfo.io/json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! Отправь /myip, чтобы узнать информацию о своём IP-адресе."
    )

@dp.message(Command("myip"))
async def my_ip(message: types.Message):
    # Получаем IP пользователя из заголовков Telegram (не всегда доступно)
    # В Telegram API нет прямого IP пользователя. Можно узнать только IP сервера.
    # Поэтому показываем IP, с которого бот делает запрос, либо просим пользователя ввести свой IP.
    await message.answer(
        "Telegram не передаёт боту IP-адрес пользователя. "
        "Отправь /ip <адрес>, чтобы проверить любой IP."
    )

@dp.message(Command("ip"))
async def ip_info(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("Укажи IP: /ip 8.8.8.8")
        return
    ip = args[1].strip()
    data = await get_ip_info(ip)
    if "error" in data:
        await message.answer("Не удалось получить информацию об этом IP.")
        return
    text = (
        f"IP: {data.get('ip')}\n"
        f"Город: {data.get('city')}\n"
        f"Регион: {data.get('region')}\n"
        f"Страна: {data.get('country')}\n"
        f"Организация: {data.get('org')}\n"
        f"Координаты: {data.get('loc')}\n"
        f"Часовой пояс: {data.get('timezone')}"
    )
    await message.answer(text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())