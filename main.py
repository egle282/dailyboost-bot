import os
import telebot
from telebot import types
from dotenv import load_dotenv
from database import init_db, get_user, create_user, update_user, get_all_users
from voice import text_to_voice
from languages import t
from error_handler import safe_execute, safe_send
from datetime import datetime, timedelta

load_dotenv()
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
init_db()

# === КОНСТАНТЫ ПРЕМИУМА ===
PREMIUM_PRICE_STARS = 499  # ≈ 650 ₽
PREMIUM_DAYS = 30
REFERRAL_BONUS_DAYS = 7

# === Проверка премиума ===
def is_premium(user_id):
    user = get_user(user_id)
    return user and user.get("premium_until", 0) > datetime.now().timestamp()

# === Реферальная система ===
@bot.message_handler(commands=['start'])
@safe_execute
def start(message):
    user_id = message.from_user.id
    name = message.from_user.first_name or "друг"
    lang_code = (message.from_user.language_code or "en").lower()
    lang = "es" if lang_code.startswith("es") else "ru" if lang_code.startswith("ru") else "en"

    # Реферальная ссылка
    ref_id = message.text.split()[-1] if len(message.text.split()) > 1 else None
    if ref_id and ref_id.isdigit() and int(ref_id) != user_id:
        referrer = get_user(int(ref_id))
        if referrer:
            bonus_until = referrer.get("premium_until", 0) + (REFERRAL_BONUS_DAYS * 86400)
            update_user(int(ref_id), premium_until=bonus_until)
            bot.send_message(int(ref_id), f"Ты пригласил друга! +{REFERRAL_BONUS_DAYS} дней премиум!")

    user = get_user(user_id)
    if not user:
        create_user(user_id, name)
        update_user(user_id, language=lang)

    lang = get_user(user_id)["language"]
    bot.send_message(message.chat.id, t(lang, "start", name=name), reply_markup=main_keyboard(lang))

    voice_file = text_to_voice(t(lang, "voice_welcome", name=name), lang)
    safe_send(bot, message.chat.id, voice_path=voice_file)

# === Команда Премиум ===
@bot.message_handler(commands=['premium'])
@safe_execute
def premium_cmd(message):
    user_id = message.from_user.id
    if is_premium(user_id):
        days_left = int((get_user(user_id)["premium_until"] - datetime.now().timestamp()) / 86400)
        bot.send_message(message.chat.id, f"У тебя уже премиум! Осталось {days_left} дней")
        return

    bot.send_invoice(
        chat_id=message.chat.id,
        title="DailyBoost Premium — 30 дней",
        description="• Голосовые напоминания 2 раза в день\n• Персональный план под твои цели\n• Без рекламы\n• Поддержка проекта ❤️",
        payload=f"premium_{user_id}",
        provider_token="",  # ПУСТО для Stars
        currency="XTR",
        prices=[types.LabeledPrice("Premium 30 дней", PREMIUM_PRICE_STARS)],
        start_parameter="premium",
        photo_url="https://i.imgur.com/5eX8kZJ.png",
        need_name=False,
        need_phone_number=False,
        need_shipping_address=False
    )

@bot.pre_checkout_query_handler(func=lambda q: True)
def checkout(q):
    bot.answer_pre_checkout_query(q.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
@safe_execute
def got_payment(message):
    user_id = message.from_user.id
    days = PREMIUM_DAYS
    new_until = int(datetime.now().timestamp()) + days * 86400
    update_user(user_id, premium_until=new_until)

    lang = get_user(user_id)["language"]
    text = "ПРЕМИУМ АКТИВИРОВАН! Теперь ты в элите\n\nГолос по утрам и вечерам\nПерсональные планы\nНикакой рекламы\nСпасибо, что поддержал проект!"
    bot.send_message(message.chat.id, text, reply_markup=main_keyboard(lang))

    voice_file = text_to_voice("Поздравляю с премиумом! Теперь я твой личный голосовой коуч 24 на 7", lang)
    safe_send(bot, message.chat.id, voice_path=voice_file)

# === Утренние голосовые только для премиум ===
def send_morning_to_all():
    for user in get_all_users():
        if is_premium(user["user_id"]):
            voice_file = text_to_voice(t(user["language"], "morning_greeting", name=user["name"]), user["language"])
            safe_send(bot, user["user_id"], voice_path=voice_file)

# === Твоя реферальная ссылка ===
@bot.message_handler(commands=['invite'])
@safe_execute
def invite(message):
    bot.send_message(message.chat.id,
        f"Пригласи друзей — получи +7 дней премиум за каждого!\n\n"
        f"Твоя ссылка:\nhttps://t.me/{bot.get_me().username}?start={message.from_user.id}")

# === Остальные функции (план, фото, профиль) — как было ===
# (вставь сюда свой предыдущий код)

# === Запуск ===
if __name__ == "__main__":
    from apscheduler.schedulers.background import BackgroundScheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_morning_to_all, 'cron', hour=8, minute=0)
    scheduler.start()
    
    print("DailyBoost Premium + Stars АКТИВИРОВАН! Готов к миллиону")
    bot.infinity_polling(none_stop=True)
