import telebot
import urllib.request
import ssl
import src.functions as functions
import pygal
from pygal.style import Style

token = '773006241:AAHEeR71QohqkICGXbQQPQ2S515UmULLeoY'

bot = telebot.TeleBot(token)
database = {}


def get_object(id):
    """
    Gets an object of user's file or show the message
    """
    if 'user_' + str(id) in database:
        return database['user_' + str(id)]

    bot.send_message(id, "Please, send me a file first")


def write_diagram(chart, id, title):
    """
    Function that receives an id of the user, type of char and title of it,
    and creates a char.
    """
    db_object = get_object(id)
    if db_object:
        chart.title = title
        for i in range(len(db_object['values'])):
            chart.add(db_object['names'][i], db_object['values'][i])
        chart.render_to_file("diagram.svg")
        with open("diagram.svg") as svg:
            bot.send_document(id, svg)

@bot.message_handler(commands=["start"])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)

    user_markup.row("/min", "/max")
    user_markup.row("/std_deviation", "/median")
    user_markup.row("/mean", "/mode")
    user_markup.row("/harmonic_mean", "/geometric_mean")
    user_markup.row("/bar", "/pie")
    user_markup.row("/horizontal_bar", "/stacked_bar")
    user_markup.row("/solid_gauge", "/gauge")

    user_markup.row("/data")

    msg = "Hello, please, send me a file to get started"
    bot.send_message(message.from_user.id, msg, reply_markup=user_markup)


@bot.message_handler(commands=["keyboard"])
def handle_start(message):
    hide_markup = telebot.types.ReplyKeyboardRemove()
    msg = "Now you can use default keyboard"
    bot.send_message(message.from_user.id, msg, reply_markup=hide_markup)


@bot.message_handler(commands=["bar"])
def handle_text(message):
    id = message.from_user.id
    write_diagram(pygal.Bar(), id, 'Your diagrams')


@bot.message_handler(commands=["solid_gauge"])
def handle_text(message):
    id = message.from_user.id
    write_diagram(pygal.SolidGauge(), id, 'Your diagrams')


@bot.message_handler(commands=["gauge"])
def handle_text(message):
    id = message.from_user.id
    write_diagram(pygal.Gauge(), id, 'Your diagrams')


@bot.message_handler(commands=["horizontal_bar"])
def handle_text(message):
    id = message.from_user.id
    write_diagram(pygal.HorizontalBar(), id, 'Your diagrams')


@bot.message_handler(commands=["stacked_bar"])
def handle_text(message):
    id = message.from_user.id
    write_diagram(pygal.StackedBar(), id, 'Your diagrams')


@bot.message_handler(commands=["pie"])
def handle_text(message):
    id = message.from_user.id
    write_diagram(pygal.Pie(), id, 'Your diagrams')



@bot.message_handler(commands=["data"])
def handle_text(message):
    id = message.chat.id
    db_object = get_object(id)
    if db_object:
        bot.send_message(id, db_object['source'])


@bot.message_handler(commands=["min"])
def handle_text(message):
    id = message.chat.id
    db_object = get_object(id)
    if db_object:
        bot.send_message(id, min(db_object['values']))


@bot.message_handler(commands=["max"])
def handle_text(message):
    id = message.chat.id
    db_object = get_object(id)
    if db_object:
        bot.send_message(id, max(db_object['values']))


@bot.message_handler(commands=["std_deviation"])
def handle_text(message):
    id = message.chat.id
    db_object = get_object(id)
    if db_object:
        bot.send_message(id, functions.standard_deviation(db_object['values']))


@bot.message_handler(commands=["median"])
def handle_text(message):
    id = message.chat.id
    db_object = get_object(id)
    if db_object:
        bot.send_message(id, functions.median(db_object['values']))


@bot.message_handler(commands=["mean"])
def handle_text(message):
    id = message.chat.id
    db_object = get_object(id)
    if db_object:
        bot.send_message(id, functions.mean(db_object['values']))


@bot.message_handler(commands=["mode"])
def handle_text(message):
    id = message.chat.id
    db_object = get_object(id)
    if db_object:
        bot.send_message(id, functions.mode(db_object['values']))


@bot.message_handler(commands=["harmonic_mean"])
def handle_text(message):
    id = message.chat.id
    db_object = get_object(id)
    if db_object:
        bot.send_message(id, functions.harmonic_mean(db_object['values']))


@bot.message_handler(commands=["geometric_mean"])
def handle_text(message):
    id = message.chat.id
    db_object = get_object(id)
    if db_object:
        bot.send_message(id, functions.geometric_mean(db_object['values']))


@bot.message_handler(content_types=["document"])
def handle_doc(message):
    file_obj = bot.get_file(message.document.file_id)
    f_path = file_obj.file_path
    url = 'https://api.telegram.org/file/bot' + token + '/' + f_path
    context = ssl._create_unverified_context()
    f = urllib.request.urlopen(url, context=context)

    global database
    resp = f.read().decode("utf-8")

    session = {
        "names": [],
        "values": [],
        "source": resp
    }

    resp = resp.split('\n')
    # slice last unneded(empty) element
    if resp[-1] == '':
        resp = resp[:-1]

    # save data to "database"
    for i in resp:
        row = i.split(',')
        session['names'].append(row[0])
        session['values'].append(int(row[1]))
    database['user_' + str(message.from_user.id)] = session
    bot.send_message(message.chat.id, 'Your file was successfully received')


bot.polling(none_stop=True, interval=0)
