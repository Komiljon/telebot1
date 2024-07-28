import requests
import telebot
from telebot import types
import webbrowser
from tok import key

cash = 0
bot = telebot.TeleBot(key)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Введите сумму')
    bot.register_next_step_handler(message, convertor)


def convertor(message):
    global cash
    try:
        cash = float(message.text.strip())
    except ValueError:
        bot.delete_message(message.chat.id, 'Неверный формат')
        return

    if cash > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/EUR', callback_data="usd/eur")
        btn2 = types.InlineKeyboardButton('EUR/USD', callback_data="eur/usd")
        btn3 = types.InlineKeyboardButton('USD/GBR', callback_data="usd/gbr")
        btn4 = types.InlineKeyboardButton('Другое', callback_data="else")
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Введите число больше 0')
        bot.register_next_step_handler(message, convertor)


@bot.callback_query_handler(func=lambda call: True)
def callback_message(call):
    if call.data != 'else':
        val = call.data.upper().split('/')
        url = f'https://api.exchangerate.host/convert?from={val[0]}&to={val[1]}'
        response = requests.get(url)
        data = response.json()
        rate = data['info']['rate']
        res = cash * rate
        bot.send_message(call.message.chat.id, f'Итог {round(res, 2)} курс перевода {rate}')
        bot.register_next_step_handler(call.message, convertor)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару валют')
        bot.register_next_step_handler(call.message, my_cur)


def my_cur(message):
    val = message.text.upper().split('/')
    url = f'https://api.exchangerate.host/convert?from={val[0]}&to={val[1]}'
    response = requests.get(url)
    data = response.json()
    rate = data['info']['rate']
    res = cash * rate
    bot.send_message(message.chat.id, f'Итог {round(res, 2)} курс перевода {rate}')
    bot.register_next_step_handler(message, convertor)


bot.polling(non_stop=True)