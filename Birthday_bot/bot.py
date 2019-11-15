import telebot
from os import listdir
from os.path import isfile, join


bot = telebot.TeleBot('997891715:AAHFVn7j4lZd71ZOxK8oQatLEoiMJ4XxSNQ')


files = [f for f in listdir() if isfile(f)]


mode = 'menu'
user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
user_markup.row("Записатись", 'Вихід')
choice = telebot.types.ReplyKeyboardMarkup(True, False)
choice.row('Перезаписати', 'Вихід')
hide_markup = telebot.types.ReplyKeyboardRemove()
mode_message = {
    'name': "Введіть ім'я і прізвище через пробіл",
    'preference': "Що ви хочете?",
    'menu': ['введіть /start, щоб запустити бота',
             'Готово',
             'Ви вже є в базі, перезаписати?'],
    'bd': 'Введіть дату народження через крапку',
    'error': 'Введіть ще раз'
}


@bot.message_handler(commands=['start'])
def handle_start(message):
    msg = "Привіт, ти хочеш зареєструватись?"
    bot.send_message(message.from_user.id, msg, reply_markup=user_markup)


@bot.message_handler(content_types=['text'])
def reply(message):
    global mode
    line = message.text.lower()
    if mode == 'menu':
        if line == "записатись":
            if message.from_user.username + '.txt' not in files:
                mode = 'bd'
                bot.send_message(message.from_user.id,
                                 mode_message[mode],
                                 reply_markup=hide_markup)
            else:
                bot.send_message(message.from_user.id,
                                 mode_message[mode][2],
                                 reply_markup=choice)
        elif line == "вихід":
            bot.send_message(message.from_user.id,
                             mode_message[mode][0],
                             reply_markup=hide_markup)
        elif line == "перезаписати":
            mode = 'bd'
            bot.send_message(message.from_user.id,
                             mode_message[mode],
                             reply_markup=hide_markup)
    elif mode == 'bd':
        with open(message.from_user.username + '.txt', 'w') as f:
            f.write(line + '\n')
        mode = 'name'
        bot.send_message(message.from_user.id, mode_message[mode])
    elif mode == 'name':
        if len(line.split()) != 2:
            bot.send_message(message.from_user.id, mode_message['error'])
        else:
            with open(message.from_user.username + '.txt', 'a') as f:
                f.write(line.split()[0].capitalize()
                        + ' '
                        + line.split()[1].capitalize()
                        + '\n')
            mode = 'preference'
            bot.send_message(message.from_user.id, mode_message[mode])
    elif mode == 'preference':
        with open(message.from_user.username + '.txt', 'a') as f:
            f.write(line + '\n')
        mode = 'menu'
        bot.send_message(message.from_user.id,
                         mode_message[mode][1],
                         reply_markup=user_markup)


bot.polling()
