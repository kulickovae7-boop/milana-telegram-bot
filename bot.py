import telebot
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# ===== ХРАНЕНИЕ ПОЛЬЗОВАТЕЛЕЙ =====
users = {}

def get_user(chat_id):
    if chat_id not in users:
        users[chat_id] = {
            "mission": 1,
            "score": 0,
            "waiting_answer": False
        }
    return users[chat_id]

# ===== МЕНЮ =====
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("📚 Урок"))
    markup.row(KeyboardButton("⭐ Мой уровень"),
               KeyboardButton("🔥 Челлендж дня"))
    return markup

# ===== МИССИИ =====
missions = {
    1: {
        "text": "🎮 МИССИЯ 1\n\nЯ (девочка) люблю = Rada\n\n✍ Напиши: Rada berem",
        "answer": "rada berem"
    },
    2: {
        "text": "🎮 МИССИЯ 2\n\nЯ иду = Grem\n\n✍ Напиши: Grem v šolo",
        "answer": "grem v šolo"
    },
    3: {
        "text": "🎮 МИССИЯ 3\n\nЯ хочу = Želim\n\n✍ Напиши: Želim čaj",
        "answer": "želim čaj"
    }
}

# ===== START =====
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "🎓 Добро пожаловать в Milana AI Academy!",
        reply_markup=main_menu()
    )

# ===== УРОК =====
@bot.message_handler(func=lambda m: m.text == "📚 Урок")
def start_lesson(message):
    user = get_user(message.chat.id)
    mission_id = user["mission"]

    if mission_id in missions:
        bot.send_message(message.chat.id, missions[mission_id]["text"])
        user["waiting_answer"] = True
    else:
        bot.send_message(message.chat.id,
                         "🏆 Ты прошла все миссии!",
                         reply_markup=main_menu())

# ===== МОЙ УРОВЕНЬ =====
@bot.message_handler(func=lambda m: m.text == "⭐ Мой уровень")
def level_info(message):
    user = get_user(message.chat.id)
    mission = user["mission"]
    score = user["score"]

    level = 1
    if mission > 5:
        level = 2
    if mission > 10:
        level = 3

    bot.send_message(
        message.chat.id,
        f"⭐ Твой уровень: {level}\n"
        f"📍 Текущая миссия: {mission}\n"
        f"💎 Баллы: {score}",
        reply_markup=main_menu()
    )

# ===== ЧЕЛЛЕНДЖ ДНЯ =====
@bot.message_handler(func=lambda m: m.text == "🔥 Челлендж дня")
def challenge(message):
    bot.send_message(
        message.chat.id,
        "🔥 Челлендж дня:\n\nНапиши 3 фразы с Rada 💛",
        reply_markup=main_menu()
    )

# ===== ПРОВЕРКА ОТВЕТА =====
@bot.message_handler(func=lambda m: True)
def check_answer(message):
    user = get_user(message.chat.id)

    if not user["waiting_answer"]:
        return

    mission_id = user["mission"]

    if mission_id not in missions:
        return

    correct_answer = missions[mission_id]["answer"]

    if message.text.lower() == correct_answer:
        user["score"] += 10
        user["mission"] += 1
        user["waiting_answer"] = False

        bot.send_message(
            message.chat.id,
            f"✨ БИНГО!\n+10 ⭐\nБаллы: {user['score']}",
            reply_markup=main_menu()
        )
    else:
        bot.send_message(
            message.chat.id,
            "❌ Попробуй ещё раз 💛"
        )

bot.infinity_polling()
