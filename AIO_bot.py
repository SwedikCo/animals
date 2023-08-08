from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Text, Command
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove, KeyboardButtonPollType)
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types.web_app_info import WebAppInfo
from config_data.config import load_config
import requests

config = load_config('config_data')
API_TOKEN: str = config.tg_bot.token
ADMIN_ID: str = config.tg_bot.admin_ids[0]
bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

cat_url: str = 'https://api.thecatapi.com/v1/images/search'
dog_url: str = 'https://random.dog/woof.json'

# Инициализируем билдер
#kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

# Создаем кнопки
#contact_btn: KeyboardButton = KeyboardButton(
#                                text='Отправить телефон',
#                                request_contact=True)
#geo_btn: KeyboardButton = KeyboardButton(
#                                text='Отправить геолокацию',
##                                request_location=True)
#poll_btn: KeyboardButton = KeyboardButton(
#                                text='Создать опрос/викторину',
#                                request_poll=KeyboardButtonPollType())
#web_app_btn: KeyboardButton = KeyboardButton(
#                                text='Start Web App',
#                                web_app=WebAppInfo(url="https://wits-project-7j3f.glide.page"))

# Добавляем кнопки в билдер
#kb_builder.row(contact_btn, geo_btn, poll_btn, web_app_btn, width=1)

# Создаем объект клавиатуры
#keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(
#                                    resize_keyboard=True,
#                                    one_time_keyboard=True)

# Создаем объекты кнопок
button_1: KeyboardButton = KeyboardButton(text='Собачку 🦮')
button_2: KeyboardButton = KeyboardButton(text='Кошечку 🐈‍')

# Создаем объект клавиатуры, добавляя в него кнопки
keyboard_animals: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[button_1, button_2]], resize_keyboard=True,
                                    one_time_keyboard=False)


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer('Привет! \n?Кого хочешь посмотреть?\n\n',
                         reply_markup=keyboard_animals)
    await bot.send_message(
        chat_id=ADMIN_ID, 
        text=f'{message.from_user.first_name} (username: {message.from_user.username}) запустил бота в {message.date.hour}:{message.date.minute}'
        )

#@dp.message(Command(commands=['help']))
#async def process_help_command(message: Message):
#    await message.answer('Это эксперементы с кнопками\n\n',
#                         reply_markup=keyboard)


@dp.message(Text(text=['Кошечку 🐈‍']))
async def send_echo(message: Message):
    await bot.send_photo(message.chat.id, photo=requests.get(cat_url).json()[0]['url'])
    await bot.send_message(
        chat_id=ADMIN_ID, 
        text=f'{message.from_user.first_name} (username: {message.from_user.username}) запросил котика в {message.date.hour}:{message.date.minute}'
        )

@dp.message(Text(text=['Собачку 🦮']))
async def send_echo(message: Message):
    await bot.send_photo(message.chat.id, photo=requests.get(dog_url).json()['url'])
    await bot.send_message(
        chat_id=ADMIN_ID, 
        text=f'{message.from_user.first_name} (username: {message.from_user.username}) запросил собачку в {message.date.hour}:{message.date.minute}'
        )

@dp.message()
async def send_echo(message: Message):
    await bot.send_message(message.chat.id, text='Передохни, пиццу откуси\n 🍕')

dp.run_polling(bot, polling_timeout=50)
