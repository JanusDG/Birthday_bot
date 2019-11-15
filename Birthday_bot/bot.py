import telebot
bot = telebot.TeleBot('999922859:AAHogSOQzI9Muvgcfc-216KSTZVpEhd7hkY')


mode = 'menu'
user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
user_markup.row("Записати", 'Редагувати дані', 'Вихід')
hide_markup = telebot.types.ReplyKeyboardRemove()


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
            bot.send_message(message.from_user.id, msg, reply_markup=hide_markup)
        elif line == "редагувати дані":
            msg = ' '
            bot.send_message(message.from_user.id, msg, reply_markup=hide_markup)
        elif line == "вихід":
            msg = 'введіть /start, щоб запустити бота'
            bot.send_message(message.from_user.id, msg, reply_markup=hide_markup)
    elif mode == 'bd':
        with open(message.from_user.username + '.txt', 'w') as f:
            f.write(line + '\n')
        mode = 'name'
        msg = "Введіть ім'я і прізвище через пробіл"
        bot.send_message(message.from_user.id, msg)
    elif mode == 'name':
        with open(message.from_user.username + '.txt', 'a') as f:
            f.write(line + '\n')
        mode = 'preference'
        msg = "Що ви хочете?"
        bot.send_message(message.from_user.id, msg)
    elif mode == 'preference':
        with open(message.from_user.username + '.txt', 'a') as f:
            f.write(line + '\n')
        mode = 'menu'
        msg = 'Готово'
        bot.send_message(message.from_user.id, msg, reply_markup=user_markup)


bot.polling()
