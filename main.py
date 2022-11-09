from telebot import *
import config
from text_const import buttons, messages
from game_functions import *
import random
from my_functions import create_reply_keyboard, send_url_photo, send_file_photo

bot = telebot.TeleBot(config.TG_TOKEN)
butt = {'0': 'error'}
playerchoice = {'0': 'error'}
curplayer = {'0': 'error'}
mess = {'0': 'error'}


@bot.inline_handler(func=lambda query: 'кот' in query.query or 'cat' in query.query)
def query_photo(inline_query):
    send_url_photo(bot, inline_query)


@bot.message_handler(commands=['start'])
def start(message):
    global butt
    global mess
    user_id = message.from_user.id
    mess[str(user_id)] = ''
    butt[str(user_id)] = ''
    last_name = message.from_user.last_name
    markup = create_reply_keyboard()
    if last_name is None:
        curplayer[str(user_id)] = message.from_user.first_name
        send_message = f'Привет, <b>{curplayer[str(user_id)]}</b>, выберите интересующую вас команду ниже'

    else:
        curplayer[str(user_id)] = message.from_user.first_name + message.from_user.last_name
        send_message = f'Привет, <b>{curplayer[str(user_id)]}</b>'
    bot.send_message(user_id, send_message, parse_mode='html', reply_markup=markup)


@bot.message_handler()
def bot_message(message):
    global playerchoice
    global butt
    global curplayer
    user_id = message.from_user.id
    if message.from_user.last_name is None:
        curplayer[str(user_id)] = message.from_user.first_name
    else:
        curplayer[str(user_id)] = message.from_user.first_name + message.from_user.last_name
    if message.text == buttons.HELP_BUTTON or message.text == '/help' or message.text == '/help@ghauruXO_bot' \
            or 'помощь' in message.text.lower():
        send_message = messages.CAT
        bot.send_message(user_id, send_message, parse_mode='html')
    if message.text == buttons.PLAY_BUTTON or message.text == '/play' or message.text == '/play@ghauruXO_bot' \
            or 'игра' in message.text.lower():
        butt[str(user_id)] = [messages.STAR, messages.STAR, messages.STAR,
                              messages.STAR, messages.STAR, messages.STAR,
                              messages.STAR, messages.STAR, messages.STAR]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        first_button = types.KeyboardButton(messages.X)
        second_button = types.KeyboardButton(messages.O)
        markup.add(first_button, second_button)
        bot.send_message(user_id, messages.SIDE_CHOICE, reply_markup=markup)
    if message.text == messages.X or message.text == messages.O:
        markup = types.ReplyKeyboardRemove()
        bot.send_message(user_id, 'Начинается игра...', reply_markup=markup)
        playerchoice[str(user_id)] = message.text
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(messages.STAR, callback_data='btn1')
        button2 = types.InlineKeyboardButton(messages.STAR, callback_data='btn2')
        button3 = types.InlineKeyboardButton(messages.STAR, callback_data='btn3')
        button4 = types.InlineKeyboardButton(messages.STAR, callback_data='btn4')
        button5 = types.InlineKeyboardButton(messages.STAR, callback_data='btn5')
        button6 = types.InlineKeyboardButton(messages.STAR, callback_data='btn6')
        button7 = types.InlineKeyboardButton(messages.STAR, callback_data='btn7')
        button8 = types.InlineKeyboardButton(messages.STAR, callback_data='btn8')
        button9 = types.InlineKeyboardButton(messages.STAR, callback_data='btn9')
        markup.add(button1, button2, button3, button4, button5, button6, button7, button8, button9)
        bot.send_message(user_id, 'Выберите кнопку', reply_markup=markup)
    if message.text == '/cat' or message.text == buttons.CAT_BUTTON or message.text == '/cat@ghauruXO_bot' \
            or 'кот' in message.text.lower():
        send_file_photo(bot, user_id)
    if 'скрыть' in message.text.lower() or message.text == '/remove':
        markup = types.ReplyKeyboardRemove()
        bot.send_message(user_id, 'Скрываю меню бота', reply_markup=markup)
    if message.text.lower() == 'меню' or message.text.lower() == 'menu' or message.text.lower() == '/menu':
        markup = create_reply_keyboard()
        bot.send_message(user_id, 'Меню бота', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data)
def change_callback_buttons(callback):
    global mess
    user_id = callback.from_user.id
    if check_victory(butt[str(user_id)]) or check_tie(butt[str(user_id)]):
        win = who_won(butt[str(user_id)], playerchoice[str(user_id)])
        if win != 'D':
            if playerchoice[str(user_id)] == win:
                mess[str(user_id)] = f'Игрок <b>{curplayer[str(user_id)]}</b> уже выйграл'
            else:
                mess[str(user_id)] = 'Бот уже выйграл'
        else:
            mess[str(user_id)] = f'Уже ничья между <b>{curplayer[str(user_id)]}</b> и ботом'
        bot.send_message(user_id, mess[str(user_id)], parse_mode='html')
    else:
        button_list = []
        markup = types.InlineKeyboardMarkup()
        for i in range(1, 10):
            if callback.data == 'btn' + str(i) and butt[str(user_id)][i - 1] == messages.STAR:
                butt[str(user_id)][i - 1] = playerchoice[str(user_id)]
                numbers = []
                mess[str(user_id)] = 'Выбирайте кнопку'
                for k in range(len(butt[str(user_id)])):
                    if butt[str(user_id)][k] == messages.STAR:
                        numbers.append(k)
                if playerchoice[str(user_id)] == messages.X and numbers:
                    butt[str(user_id)][random.choice(numbers)] = messages.O
                elif numbers:
                    butt[str(user_id)][random.choice(numbers)] = messages.X
            elif callback.data == 'btn' + str(i) and butt[str(user_id)][i - 1] != messages.STAR:
                if mess[str(user_id)] == messages.TAKEN_SPOT:
                    mess[str(user_id)] = messages.TAKEN_SPOT2
                else:
                    mess[str(user_id)] = messages.TAKEN_SPOT
        for i in range(1, 10):
            button = types.InlineKeyboardButton(butt[str(user_id)][i - 1], callback_data='btn' + str(i))
            button_list.append(button)
        markup.add(button_list[0], button_list[1], button_list[2], button_list[3], button_list[4],
                   button_list[5], button_list[6], button_list[7], button_list[8])
        if check_victory(butt[str(user_id)]) or check_tie(butt[str(user_id)]):
            win = who_won(butt[str(user_id)], playerchoice[str(user_id)])
            if win != 'D':
                if playerchoice[str(user_id)] == who_won(butt[str(user_id)],
                                                            playerchoice[str(user_id)]):
                    mess[str(user_id)] = f'Игрок <b>{curplayer[str(user_id)]}</b> выйграл'
                    bot.send_message(chat_id=user_id, text='Молодец, держи котика за победу!')
                    send_file_photo(bot, user_id)
                else:
                    mess[str(user_id)] = 'Бот выйграл'
            else:
                mess[str(user_id)] = f'Ничья между <b>{curplayer[str(user_id)]}</b> и ботом'
        bot.edit_message_text(chat_id=user_id, message_id=callback.message.id,
                              text=mess[str(user_id)], reply_markup=markup, parse_mode='html')


bot.polling(none_stop=True)
