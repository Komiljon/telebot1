from tok import key
from aiogram import Bot, Dispatcher, executor, types

bot = Bot(key)
dp = Dispatcher(bot)


@dp.message_handler(content_types=['photo'])
async def photo(message: types.Message):
    await message.reply('This is photo')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Site', url='aptechestvo.ru'))
    markup.add(types.InlineKeyboardButton('List comands', callback_data='list'))
    await message.reply('Hello', reply_markup=markup)


@dp.callback_query_handler()
async def callbback(call):
    if call.data == 'list':
        await call.message.answer('/bye\n/start')


@dp.message_handler(commands=['bye'])
async def reply(message: types.Message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add(types.InlineKeyboardButton('/start'))
    markup.add(types.InlineKeyboardButton('good bye'))
    await message.reply('Listen', reply_markup=markup)


executor.start_polling(dp)
