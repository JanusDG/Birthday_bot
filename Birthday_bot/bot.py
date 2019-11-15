import telebot
bot = telebot.TeleBot("899632234:AAGPE5m5tlL0luFSRweaOjrbDclMBFTFyNs")

@bot.message_handler(commands=['help', 'start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)

    user_markup.row("CS", "BA")
    user_markup.row("math", "meme")

    user_markup.row("/pain")

    msg = "Привіт, я твій перший бот!!!"
    bot.send_message(message.from_user.id, msg, reply_markup=user_markup)


@bot.message_handler(commands=["keyboard"])
def handle_start(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    msg = "Тепер ввімкнено режим звичайної клавіатури."
    bot.send_message(message.from_user.id, msg, reply_markup=hide_markup)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привіт':
        bot.send_message(message.chat.id, 'Привіт студент')
    elif message.text in ["Папа" , "Прощай", "Бувай"]:
        bot.send_message(message.chat.id, 'папа')
    elif message.text.lower() == "meme":
        photo = open('meme.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)
    elif message.text.lower() in "ba":
        sti = open('sticker.webp', 'rb')
        bot.send_sticker(message.chat.id, sti)
    elif message.text.lower() in "cs":
        photo = open('cs.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)

@bot.message_handler(commands=["pain"])
def handle_text(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    msg = "https://cms.ucu.edu.ua/my/"
    bot.send_message(message.from_user.id, msg, reply_markup=hide_markup)
        
    
bot.polling()
