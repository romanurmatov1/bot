import telebot
from pymongo import MongoClient
from datetime import datetime


now = datetime.now()

year = now.year
month = now.month
day = now.day

hour = now.hour
minute = now.minute

date = str(day)+'/'+str(month)+'/'+str(year)+' '+str(int(hour)+5)+':'+str(minute)


def insert(ism, familiya, phone):
   cluster = MongoClient("mongodb+srv://raxmatjon:raxmatjon@cluster0.g3zlm.mongodb.net/RegisterBot?retryWrites=true&w=majority")
   db = cluster['bot']
   collection = db['bot']
   list = {"ism":ism,"familiya":familiya,"phone":phone, "date":date}
   collection.insert_one(list)
   

API_TOKEN = '2070033776:AAEb5lKaBnjENVaqeJsh_4TwH17wNq82cmE'

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}


class User:
    def __init__(self, ism):
        self.ism = ism
        self.familiya = ''
        self.phone = None

@bot.message_handler(commands=['help', 'start'])
def hello(message):
    bot.reply_to(message, "Salom! Iltimos ro'yhatdan o'ting: /register")


@bot.message_handler(commands=['register'])
def register(message):
    msg = bot.reply_to(message, "Ismingizni kiriting: ")
    bot.register_next_step_handler(msg, process_ism_step)


def process_ism_step(message):
    chat_id = message.chat.id
    ism = message.text
    user = User(ism)
    user_dict[chat_id] = user
    msg = bot.reply_to(message, 'Familiyangizni kiriting: ')
    bot.register_next_step_handler(msg, process_familiya_step)


def process_familiya_step(message):
    chat_id = message.chat.id
    familiya = message.text
    user = user_dict[chat_id]
    user.familiya = familiya
    msg = bot.reply_to(message, 'Telefoningizni kiriting(998991234567): ')
    bot.register_next_step_handler(msg, process_phone_step)


def process_phone_step(message):
    chat_id = message.chat.id
    phone = message.text
    user = user_dict[chat_id]
    user.phone = phone
    bot.send_message(chat_id, "Siz ro'yhatdan o'tdingiz. \nIsm: "+user.ism +
                     " \nFamiliya: "+user.familiya+" \nTelefon: "+str(user.phone))
    insert(user.ism, user.familiya, user.phone) 

bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.infinity_polling()
