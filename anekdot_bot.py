import random
import requests
from tok import key
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, executor, types

url = 'https://www.anekdot.ru/last/good/'


def parser(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    anekdots = soup.find_all('div', class_='text')
    return [c.text for c in anekdots]


last_jokes = parser(url)

bot = Bot(key)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Получить анекдот', callback_data='joke'))
    await message.reply('Привет хочешь анекдот?', reply_markup=markup)


@dp.callback_query_handler()
async def callbback(call):
    if call.data == 'joke':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Получить анекдот', callback_data='joke'))
        joke = random.choice(last_jokes)
        await call.message.answer(joke, reply_markup=markup)


@dp.message_handler(content_types=['text'])
async def reply(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Получить анекдот', callback_data='joke'))
    await message.reply('Еще анекдот?', reply_markup=markup)

executor.start_polling(dp)
