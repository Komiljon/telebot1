import json

import requests

from tok import key, apiwKey
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(key)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Получть прогноз погоды', callback_data='city'))
    markup.add(types.InlineKeyboardButton('Список команд', callback_data='list'))
    await message.reply('Узнать прогноз погоды', reply_markup=markup)


@dp.message_handler(commands=['ListCity'])
async def reply(message: types.Message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.InlineKeyboardButton('London'))
    markup.add(types.InlineKeyboardButton('Tashkent'))
    await message.reply('Привет', reply_markup=markup)


@dp.callback_query_handler()
async def callbback(call):
    if call.data == 'list':
        await call.message.answer('/ListCity\n/start')
    elif call.data == 'city':
        await call.message.answer('Введите город')


@dp.message_handler(content_types=['text'])
async def reply(message: types.Message):
    city = message.text.lower().strip()
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&lang=ru&appid={apiwKey}&units=metric'
    res = requests.get(url)
    data = json.loads(res.text)
    if res.status_code == 200:
        temp = data['main']['temp']
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        desc = data['weather'][0]['description']
        await message.reply(f'Погода в городе: {message.text}\n'
                            f'Температура: {temp}C\n'
                            f'Влажность: {humidity}%\n'
                            f'Небо: {desc}\n')
    elif res.status_code == 404:
        await message.reply('Город не найден')

executor.start_polling(dp)