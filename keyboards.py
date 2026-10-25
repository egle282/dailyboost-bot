"""Keyboards for DailyBoost bot.
Implements reply and inline markups for user interaction.
"""
from telebot import types
from languages import t


def main_keyboard(lang: str = "ru") -> types.ReplyKeyboardMarkup:
    """Constructs the primary reply keyboard based on user's language."""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_plan = types.KeyboardButton(t(lang, "button_plan"))
    btn_reminder = types.KeyboardButton(t(lang, "button_reminder"))
    btn_photo = types.KeyboardButton(t(lang, "button_photo"))
    btn_profile = types.KeyboardButton(t(lang, "button_profile"))
    btn_premium = types.KeyboardButton(t(lang, "button_premium"))

    markup.add(btn_plan, btn_reminder)
    markup.add(btn_photo, btn_profile)
    markup.add(btn_premium)
    return markup


def language_inline_keyboard() -> types.InlineKeyboardMarkup:
    """Constructs language selector markup."""
    markup = types.InlineKeyboardMarkup(row_width=3)
    btn_ru = types.InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")
    btn_en = types.InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")
    btn_es = types.InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es")
    markup.add(btn_ru, btn_en, btn_es)
    return markup


def profile_inline_keyboard(lang: str = "ru", ref_link: str = "") -> types.InlineKeyboardMarkup:
    """Constructs inline action buttons for the profile screen."""
    markup = types.InlineKeyboardMarkup(row_width=1)
    share_url = f"https://t.me/share/url?url={ref_link}&text=Присоединяйся+к+DailyBoost+—+твоему+голосовому+коучу!"
    btn_share = types.InlineKeyboardButton("📲 Поделиться ссылкой", url=share_url)
    btn_premium = types.InlineKeyboardButton(t(lang, "button_premium"), callback_data="cmd_premium")
    markup.add(btn_share, btn_premium)
    return markup
