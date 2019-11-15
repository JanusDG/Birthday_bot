import telebot
bot = telebot.TeleBot('997891715:AAHFVn7j4lZd71ZOxK8oQatLEoiMJ4XxSNQ')


mode = 'menu'
user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
user_markup.row("Записати", 'Редагувати дані', 'Вихід')
hide_markup = telebot.types.ReplyKeyboardRemove()
mode_message = {
    'name': "Введіть ім'я і прізвище через пробіл",
    'preference': "Що ви хочете?",
    'menu': [' ', 'введіть /start, щоб запустити бота', 'Готово'],
    'bd': 'Введіть дату народження через крапку'
}

@bot.message_handler(commands=['start'])
def handle_start(message):
    msg = "Привіт, ти хочеш змінити свої дані, чи записатись?"
    bot.send_message(message.from_user.id, msg, reply_markup=user_markup)


@bot.message_handler(content_types=['text'])
def reply(message):
    global mode
    line = message.text.lower()
    if mode == 'menu':
        if line == "записати":
            msg = 'Введіть дату народження через крапку'
            mode = 'bd'
            bot.send_message(message.from_user.id,
                             msg,
                             reply_markup=hide_markup)
        elif line == "редагувати дані":
            bot.send_message(message.from_user.id,
                             mode_message[mode][0],
                             reply_markup=hide_markup)
        elif line == "вихід":
            bot.send_message(message.from_user.id,
                             mode_message[mode][1],
                             reply_markup=hide_markup)
    elif mode == 'bd':
        with open(message.from_user.username + '.txt', 'w') as f:
            f.write(line + '\n')
        mode = 'name'
        bot.send_message(message.from_user.id, mode_message[mode])
    elif mode == 'name':
        with open(message.from_user.username + '.txt', 'a') as f:
            f.write(line + '\n')
        mode = 'preference'
        bot.send_message(message.from_user.id, mode_message[mode])
    elif mode == 'preference':
        with open(message.from_user.username + '.txt', 'a') as f:
            f.write(line + '\n')
        mode = 'menu'
        bot.send_message(message.from_user.id,
                         mode_message[mode][2],
                         reply_markup=user_markup)


bot.polling()
