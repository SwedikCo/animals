from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command, Text
from config_data.config import load_config
import requests

config = load_config('config_data')
API_TOKEN: str = config.tg_bot.token
ADMIN_ID: str = config.tg_bot.admin_ids[0]
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

cat_url: str = 'https://api.thecatapi.com/v1/images/search'
dog_url: str = 'https://random.dog/woof.json'

@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer('Привет! \nжми /help и узнаешь что можно сделать')
    await bot.send_message(
        chat_id=ADMIN_ID, 
        text=f'{message.from_user.first_name} (username: {message.from_user.username}) запустил бота в {message.date.hour}:{message.date.minute}'
        )

@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('Хочешь котика? \nОтправть слово: CAT\n\nХочешь собачку? \nОтправть слово: DOG')


@dp.message(Text(text=['CAT', 'кот', 'кошка', 'котик', 'кошечка'], ignore_case=True))
async def send_echo(message: Message):
    await bot.send_photo(message.chat.id, photo=requests.get(cat_url).json()[0]['url'])
    await bot.send_message(
        chat_id=ADMIN_ID, 
        text=f'{message.from_user.first_name} (username: {message.from_user.username}) запросил котика в {message.date.hour}:{message.date.minute}'
        )

@dp.message(Text(text=['DOG', 'собака', 'собачка'], ignore_case=True))
async def send_echo(message: Message):
    await bot.send_photo(message.chat.id, photo=requests.get(dog_url).json()['url'])
    await bot.send_message(
        chat_id=ADMIN_ID, 
        text=f'{message.from_user.first_name} (username: {message.from_user.username}) запросил собачку в {message.date.hour}:{message.date.minute}'
        )

@dp.message()
async def send_echo(message: Message):
    await bot.send_message(message.chat.id, text='Не знаешь что спросить?\nОтправить команду:\n/help')

dp.run_polling(bot, polling_timeout=50)
