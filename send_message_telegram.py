import telebot
from telebot import types
from env import TOKEN
from env import VERSION


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Текущая версия")
    btn2 = types.KeyboardButton("Проверить обновление")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, text="Привет, {0.first_name}!\nЯ бот, проверяющий обновления версий 1С".format(message.from_user), reply_markup=markup)
    
@bot.message_handler(content_types=['text'])
def send_message(message):
    if(message.text.lower() == "текущая версия"):
        bot.send_message(message.chat.id, text=f"Текущая версия {VERSION}")
    elif(message.text.lower() == "проверить обновление"):        
        bot.send_message(message.chat.id, text="Подождите, проверяю...")
    
bot.polling(none_stop=True)
