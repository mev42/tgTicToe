from telebot import types
from text_const import buttons
from requests import get
import random


def create_reply_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button1 = types.KeyboardButton(buttons.PLAY_BUTTON)
    button2 = types.KeyboardButton(buttons.HELP_BUTTON)
    button3 = types.KeyboardButton(buttons.CAT_BUTTON)
    button4 = types.KeyboardButton(buttons.REMOVE_MENU)
    markup.add(button1, button2, button3, button4)
    return markup


def send_url_photo(bot, inline_query):
    try:
        k = 1
        temp = ''
        photo_list = []
        while k < 5:
            source = get(f"https://aws.random.cat/view/{random.choice(range(1000))}").text
            if source != temp:
                photo = source.split("src=\"")[1].split("\"")[0]
                temp = photo
                r = types.InlineQueryResultPhoto(str(k), photo, photo)
                photo_list.append(r)
                k += 1
        bot.answer_inline_query(inline_query.id, photo_list, cache_time=1)
    except:
        return send_url_photo(bot, inline_query)


def send_file_photo(bot, message_id):
    try:
        photo = open('Cats/' + str(random.choice([i for i in range(601)])) + '.jpg', 'rb')
        bot.send_photo(message_id, photo)
        photo.close()
    except:
        return send_file_photo(bot, message_id)