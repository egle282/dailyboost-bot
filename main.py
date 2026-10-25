"""DailyBoost Telegram Bot — Personal Voice Coach & Motivator."""
import os, sys, logging
from datetime import datetime
import telebot
from telebot import types
from dotenv import load_dotenv

from database import init_db, get_user, create_user, update_user, get_all_users
from voice import text_to_voice
from languages import t
from keyboards import main_keyboard, profile_inline_keyboard
from error_handler import safe_execute, safe_send

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN if TOKEN else "DUMMY_TOKEN")
PREMIUM_PRICE_STARS = 499
PREMIUM_DAYS = 30
REFERRAL_BONUS_DAYS = 7


def is_premium(user_id: int) -> bool:
    user = get_user(user_id)
    return bool(user and (user.get("premium_until") or 0) > datetime.now().timestamp())


@bot.message_handler(commands=['start'])
@safe_execute
def handle_start(message: types.Message):
    user_id = message.from_user.id
    name = message.from_user.first_name or "друг"
    lang_code = (message.from_user.language_code or "en").lower()
    lang = "es" if lang_code.startswith("es") else "ru" if lang_code.startswith("ru") else "en"

    parts = message.text.split()
    if len(parts) > 1 and parts[1].isdigit() and int(parts[1]) != user_id:
        ref_id = int(parts[1])
        referrer = get_user(ref_id)
        if referrer and not get_user(user_id):
            now_ts = int(datetime.now().timestamp())
            base = max(now_ts, referrer.get("premium_until") or 0)
            update_user(ref_id, premium_until=base + (REFERRAL_BONUS_DAYS * 86400))
            safe_send(bot, ref_id, f"🎁 Твой друг присоединился! +{REFERRAL_BONUS_DAYS} дней Premium!")

    if not get_user(user_id):
        create_user(user_id, name, language=lang)

    user = get_user(user_id)
    cur_lang = user["language"] if user else lang
    safe_send(bot, message.chat.id, t(cur_lang, "start", name=name), reply_markup=main_keyboard(cur_lang))

    voice_path = text_to_voice(t(cur_lang, "voice_welcome", name=name), cur_lang)
    if voice_path:
        safe_send(bot, message.chat.id, voice_path=voice_path)


@bot.message_handler(commands=['premium'])
@bot.callback_query_handler(func=lambda call: call.data == "cmd_premium")
@safe_execute
def handle_premium(event):
    chat_id = event.message.chat.id if isinstance(event, types.CallbackQuery) else event.chat.id
    user_id = event.from_user.id
    user = get_user(user_id)
    lang = user["language"] if user else "ru"

    if is_premium(user_id):
        days_left = max(0, int(((user.get("premium_until") or 0) - datetime.now().timestamp()) / 86400))
        safe_send(bot, chat_id, t(lang, "already_premium", days=days_left))
        return

    bot.send_invoice(
        chat_id=chat_id,
        title=f"DailyBoost Premium ({PREMIUM_DAYS} days)",
        description="• Ежедневные аудио-напоминания\n• Персональный план продуктивности\n• Без рекламы",
        payload=f"premium_{user_id}",
        provider_token="",
        currency="XTR",
        prices=[types.LabeledPrice(f"Premium {PREMIUM_DAYS} days", PREMIUM_PRICE_STARS)],
        start_parameter="premium",
    )


@bot.pre_checkout_query_handler(func=lambda q: True)
def handle_pre_checkout(query: types.PreCheckoutQuery):
    bot.answer_pre_checkout_query(query.id, ok=True)


@bot.message_handler(content_types=['successful_payment'])
@safe_execute
def handle_payment(message: types.Message):
    user_id = message.from_user.id
    user = get_user(user_id)
    lang = user["language"] if user else "ru"
    now_ts = int(datetime.now().timestamp())
    current_until = (user.get("premium_until") or 0) if user else 0
    new_until = max(now_ts, current_until) + (PREMIUM_DAYS * 86400)
    update_user(user_id, premium_until=new_until)

    safe_send(bot, message.chat.id, t(lang, "premium_activated"), reply_markup=main_keyboard(lang))
    voice_path = text_to_voice(t(lang, "premium_voice_congrats"), lang)
    if voice_path:
        safe_send(bot, message.chat.id, voice_path=voice_path)


@bot.message_handler(commands=['invite'])
@safe_execute
def handle_invite(message: types.Message):
    user_id = message.from_user.id
    bot_name = bot.get_me().username if TOKEN else "DailyBoostBot"
    ref_link = f"https://t.me/{bot_name}?start={user_id}"
    user = get_user(user_id)
    lang = user["language"] if user else "ru"
    safe_send(bot, message.chat.id, t(lang, "invite_info", ref_link=ref_link))


@bot.message_handler(func=lambda msg: any(kw in (msg.text or "") for kw in ["Сегодняшний план", "Today's Plan", "Plan de hoy"]))
@safe_execute
def handle_plan(message: types.Message):
    user = get_user(message.from_user.id)
    safe_send(bot, message.chat.id, t(user["language"] if user else "ru", "plan_text"))


@bot.message_handler(func=lambda msg: any(kw in (msg.text or "") for kw in ["Быстрое напоминание", "Quick Reminder", "Recordatorio"]))
@safe_execute
def handle_reminder(message: types.Message):
    user = get_user(message.from_user.id)
    safe_send(bot, message.chat.id, t(user["language"] if user else "ru", "reminder_text"))


@bot.message_handler(func=lambda msg: any(kw in (msg.text or "") for kw in ["Анализ фото", "Photo Analysis", "Analizar foto"]))
@safe_execute
def handle_photo_btn(message: types.Message):
    user = get_user(message.from_user.id)
    safe_send(bot, message.chat.id, t(user["language"] if user else "ru", "photo_prompt"))


@bot.message_handler(content_types=['photo'])
@safe_execute
def handle_incoming_photo(message: types.Message):
    user = get_user(message.from_user.id)
    safe_send(bot, message.chat.id, t(user["language"] if user else "ru", "photo_received"))


@bot.message_handler(func=lambda msg: any(kw in (msg.text or "") for kw in ["Мой профиль", "My Profile", "Mi perfil"]))
@safe_execute
def handle_profile(message: types.Message):
    user_id = message.from_user.id
    user = get_user(user_id)
    lang = user["language"] if user else "ru"
    bot_name = bot.get_me().username if TOKEN else "DailyBoostBot"
    ref_link = f"https://t.me/{bot_name}?start={user_id}"

    if is_premium(user_id):
        p_until = user.get("premium_until", 0)
        dt_str = datetime.fromtimestamp(p_until).strftime("%d.%m.%Y")
        days = max(0, int((p_until - datetime.now().timestamp()) / 86400))
        status_str = t(lang, "status_premium", date=dt_str, days=days)
    else:
        status_str = t(lang, "status_free")

    text = t(lang, "profile_text", name=user["name"] if user else message.from_user.first_name, status=status_str, friends="0", ref_link=ref_link)
    safe_send(bot, message.chat.id, text, reply_markup=profile_inline_keyboard(lang, ref_link))


@bot.message_handler(func=lambda msg: any(kw in (msg.text or "") for kw in ["Premium", "Премиум"]))
@safe_execute
def handle_premium_button(message: types.Message):
    handle_premium(message)


def send_morning_to_all():
    for user in get_all_users():
        if is_premium(user["user_id"]):
            greeting = t(user["language"], "morning_greeting", name=user["name"])
            voice_path = text_to_voice(greeting, user["language"])
            safe_send(bot, user["user_id"], text=greeting, voice_path=voice_path)


def start_scheduler():
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        scheduler = BackgroundScheduler()
        scheduler.add_job(send_morning_to_all, 'cron', hour=8, minute=0)
        scheduler.start()
    except Exception as e:
        logging.error(f"Failed to start scheduler: {e}")


if __name__ == "__main__":
    init_db()
    if not TOKEN:
        print("ERROR: TELEGRAM_TOKEN environment variable not set. Please provide it in .env")
        sys.exit(1)
    start_scheduler()
    print("DailyBoost bot is running...")
    bot.infinity_polling(none_stop=True)
