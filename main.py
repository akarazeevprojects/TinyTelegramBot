# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import argparse
import telegram
import sys
import logging
import os
import json

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - \
                            %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


sys.argv = ['--proxy 1']
parser = argparse.ArgumentParser(description="TinyTelegramBot")
parser.add_argument('--proxy', dest='proxy', type=int,
                    default=1, help='use proxy or not')

help_text = 'Пришли мне несколько разделённых пробелами чисел, а в ответ я тебе напишу их сумму. Например: "42 13 9".'
start_text = 'Привет!' + ' ' + help_text


def get_token():
    path = os.path.join('token.json')
    with open(path) as jsn:
        data = json.load(jsn)
    return data['token']


def start(bot, update):
    update.message.reply_text(start_text)
    return


def help(bot, update):
    update.message.reply_text(help_text)
    return


def process(text):
    """Метод, которым будет обрабатываться каждое текстовое сообщение.
    В нашем случае обработка следующая: разбить строку по пробелам -> перевести
    строки в числа -> посчитать сумму -> вернуть ответ.

    Аргументы:
        text (str): Строка, которую необзодимо обработать.

    Возвращает:
        int: Сумма чисел, содержащихся в сообщении.

    """
    # Получаем список чисел.
    numbers = list(map(int, text.split()))
    # Считаем сумму чисел.
    numbers_sum = sum(numbers)
    # Возвращаем ответ.
    return numbers_sum


def response(bot, update):
    # Текст сообщения, которое получил бот.
    text = update.message.text
    # Находим числа в сообщении и считаем их сумму.
    numbers_sum = process(text)
    # Строим ответную фразу.
    answer_text = 'Сумма: ' + str(numbers_sum)
    # И отвечаем с её помощью на сообщение от пользователя.
    update.message.reply_text(answer_text)


def main():
    token = get_token()

    args = parser.parse_args()
    bot = None

    if args.proxy == 1:
        print('-> USE PROXY')
        req = telegram.utils.request.Request(proxy_url='socks5://127.0.0.1:9050',
                                             read_timeout=30, connect_timeout=20,
                                             con_pool_size=10)
        bot = telegram.Bot(token=token, request=req)
    elif args.proxy == 0:
        print('-> NO PROXY')
        bot = telegram.Bot(token=token)
    else:
        raise ValueError('Wrong proxy.')

    updater = Updater(bot=bot)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(MessageHandler(Filters.text, response))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
