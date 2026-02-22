
import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     "Привет, Милана 💛\n"
                     "Сегодня учим словенский!\n\n"
                     "Напиши: rada berem")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = message.text.lower()

    if "rada berem" in text:
        bot.send_message(message.chat.id,
                         "Молодец! 🌟\n"
                         "Rada berem = Я люблю читать")
    else:
        bot.send_message(message.chat.id,
                         "Попробуй написать: rada berem")

bot.infinity_polling()  

