import telebot
import os
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Временное хранилище баллов (пока без базы)
user_scores = {}

def main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📚 Урок")
    btn2 = types.KeyboardButton("⭐ Мой уровень")
    btn3 = types.KeyboardButton("🔥 Челлендж дня")
    markup.add(btn1)
    markup.add(btn2, btn3)

    bot.send_message(
        chat_id,
        "🎓 Milana AI Academy\n\nВыбери, куда идём сегодня 💛",
        reply_markup=markup
    )

@bot.message_handler(commands=['start'])
def start_message(message):
    user_scores[message.chat.id] = 0
    main_menu(message.chat.id)

@bot.message_handler(func=lambda message: message.text == "📚 Урок")
def lesson(message):
    bot.send_message(
        message.chat.id,
        "🎮 МИССИЯ 1: \"Я люблю\"\n\n"
        "В словенском:\n"
        "Я (девочка) люблю = Rada\n"
        "Например:\n"
        "📖 Rada berem = Я люблю читать\n\n"
        "✍️ Напиши по-словенски:\n"
        "\"Я люблю читать\""
    )

@bot.message_handler(func=lambda message: message.text and message.text.lower() == "rada berem")
def correct_answer(message):
    user_scores[message.chat.id] = user_scores.get(message.chat.id, 0) + 10

    bot.send_message(
        message.chat.id,
        f"🌟 БИНГО!\n\n+10 баллов\n"
        f"Твои баллы: {user_scores[message.chat.id]} ⭐\n\n"
        "🏆 Миссия 1 завершена!"
    )
    main_menu(message.chat.id)

@bot.message_handler(func=lambda message: message.text == "⭐ Мой уровень")
def level(message):
    score = user_scores.get(message.chat.id, 0)
    bot.send_message(
        message.chat.id,
        f"⭐ Твои баллы: {score}\n"
        "Уровень: 1 (пока 😉)"
    )

@bot.message_handler(func=lambda message: message.text == "🔥 Челлендж дня")
def challenge(message):
    bot.send_message(
        message.chat.id,
        "🔥 Челлендж дня:\n\n"
        "Напиши по-словенски:\n"
        "\"Я люблю танцевать\""
    )

@bot.message_handler(func=lambda message: True)
def fallback(message):
    bot.send_message(
        message.chat.id,
        "💛 Я пока не понимаю это сообщение.\n"
        "Выбери кнопку из меню."
    )

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling(timeout=60, long_polling_timeout=60)
