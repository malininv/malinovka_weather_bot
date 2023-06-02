from aiogram import Bot, Dispatcher, executor, types
from weather import create_message, DAYS_WEATHER
import os

API_KEY_BOT = os.environ['API_KEY_BOT']

bot = Bot(token=API_KEY_BOT)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer('Привет! 😊\n\nОтправь любое сообщение чтобы получить погоду в Малиновке на 3 дня.🌈')


@dp.message_handler()
async def echo(message: types.Message):
    for day in range(DAYS_WEATHER):
        await message.answer(create_message(day), parse_mode='HTML')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
