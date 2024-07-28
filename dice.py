from tok import key, apiwKey
from aiogram import Bot, Dispatcher, executor, types
from asyncio import sleep

bot = Bot(key)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, f'Hello {message.from_user.username} start game')

    dice1 = await bot.send_dice(message.from_user.id)
    value_dice1 = dice1['dice']['value']
    await sleep(4)

    dice2 = await bot.send_dice(message.from_user.id)
    value_dice2 = dice2['dice']['value']
    await sleep(4)

    if value_dice1 > value_dice2:
        await bot.send_message(message.from_user.id, 'Win user 1')
    elif value_dice2 > value_dice1:
        await bot.send_message(message.from_user.id, 'Win user 2')
    else:
        await bot.send_message(message.from_user.id, 'Equalise')

    markup = types.ReplyKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('/start'))
    await bot.send_message(message.from_user.id, 'Start repeed?', reply_markup=markup)


executor.start_polling(dp)
