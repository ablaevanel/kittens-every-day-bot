import os
import requests
import logging
from dotenv import load_dotenv
from telebot import TeleBot, types


load_dotenv()

secret_token = os.getenv('TOKEN')
bot = TeleBot(token=secret_token)

URL = 'https://api.thecatapi.com/v1/images/search'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


def get_new_image():
    flag = False
    try:
        response = requests.get(URL)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)
        flag = True
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat, flag


@bot.message_handler(commands=['start'])
def start(message):
    chat = message.chat
    chat_id = chat.id
    name = chat.first_name
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_newcat = types.KeyboardButton('/newcat')
    keyboard.add(button_newcat)
    bot.send_message(chat_id=chat_id,
                     text=(f'Привет, {name}. '
                           'Посмотри, какого котика я тебе нашёл'),
                     reply_markup=keyboard)
    photo, is_dog = get_new_image()
    if is_dog:
        bot.send_message(chat_id=chat_id,
                         text='Котики закончились, но есть собачки!')
    bot.send_photo(chat_id=chat_id, photo=photo)


@bot.message_handler(commands=['newcat'])
def newcat(message):
    chat = message.chat
    chat_id = chat.id
    photo, is_dog = get_new_image()
    if is_dog:
        bot.send_message(chat_id=chat_id,
                         text='Котики закончились, но есть собачки!')
    bot.send_photo(chat_id=chat_id, photo=photo)


@bot.message_handler(content_types=['text'])
def say_hi(message):
    chat = message.chat
    chat_id = chat.id
    bot.send_message(chat_id=chat_id, text='Привет, я KittyBot!')


def main():
    bot.polling()


if __name__ == '__main__':
    main()
