import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# ====== ХРАНЕНИЕ ПОЛЬЗОВАТЕЛЕЙ ======
users = {}

def get_user(chat_id):
    if chat_id not in users:
        users[chat_id] = {
            "mission": 1,
            "score": 0
        }
    return users[chat_id]

# ====== МИССИИ ======

missions = {
    1: {
        "text": "🎮 МИССИЯ 1: 'Я люблю'\n\nВ словенском:\nЯ (девочка) люблю = Rada\n\nПример:\n📖 Rada berem = Я люблю читать\n\n✍ Напиши по-словенски:\n'Я люблю читать'",
        "answer": "rada berem"
    },
    2: {
        "text": "🎮 МИССИЯ 2: 'Я иду'\n\nВ словенском:\nЯ иду = Grem\n\n✍ Напиши по-словенски:\n'Я иду в школу'\n(подсказка: šolo)",
        "answer": "grem v šolo"
    }
}

# ====== КОМАНДА START ======

@bot.message_handler(commands=['start'])
def start(message):
    user = get_user(message.chat.id)
    bot.send_message(message.chat.id, 
        "🎓 Добро пожаловать в Milana AI Academy!\n\nНапиши 'Урок', чтобы начать.")

# ====== ЗАПУСК УРОКА ======

@bot.message_handler(func=lambda message: message.text.lower() == "урок")
def start_lesson(message):
    user = get_user(message.chat.id)
    mission_id = user["mission"]

    if mission_id in missions:
        bot.send_message(message.chat.id, missions[mission_id]["text"])
    else:
        bot.send_message(message.chat.id, "🏆 Ты прошла все миссии!")

# ====== ПРОВЕРКА ОТВЕТА ======

@bot.message_handler(func=lambda message: True)
def check_answer(message):
    user = get_user(message.chat.id)
    mission_id = user["mission"]

    if mission_id not in missions:
        return

    correct_answer = missions[mission_id]["answer"]

    if message.text.lower() == correct_answer:
        user["score"] += 10
        user["mission"] += 1

        bot.send_message(message.chat.id,
            f"✨ БИНГО!\n+10 баллов\nТвои баллы: {user['score']} ⭐\n\n🚀 Миссия завершена!")

        if user["mission"] in missions:
            bot.send_message(message.chat.id,
                "Напиши 'Урок' для следующей миссии 😉")
        else:
            bot.send_message(message.chat.id,
                "🏆 Ты прошла все миссии!")
    else:
        bot.send_message(message.chat.id,
            "❌ Попробуй ещё раз 💛")

bot.infinity_polling()
