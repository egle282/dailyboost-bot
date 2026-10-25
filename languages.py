"""Localization dictionary and translation helper for DailyBoost bot.
Supports Russian (ru), English (en), and Spanish (es).
"""
from typing import Dict, Any

LANGUAGES: Dict[str, Dict[str, str]] = {
    "ru": {
        "start": "Привет, {name}! Я DailyBoost — твой голосовой мотиватор и личный коуч!",
        "morning_greeting": "Доброе утро, {name}! Новый день — новые возможности. Сделай сегодня максимум!",
        "voice_welcome": "Привет, {name}! Я твой личный коуч. Готов стать лучше?",
        "button_plan": "📋 Сегодняшний план",
        "button_reminder": "⏰ Быстрое напоминание",
        "button_photo": "📸 Анализ фото",
        "button_profile": "👤 Мой профиль и цели",
        "button_premium": "⭐️ DailyBoost Premium",
        "plan_text": "🎯 **Твой план на сегодня:**\n1. 💧 Выпить стакан воды и размяться\n2. 🚀 Сделать главную задачу дня (Focus Session 45 мин)\n3. 📚 Уделить 20 минут чтению или развитию\n4. 🚶 Прогулка на свежем воздухе\n\n*Совет дня: дисциплина бьет мотивацию!*",
        "reminder_text": "⏰ **Напоминание установлено!**\nЧерез 2 часа я пришлю тебе короткий чек-ин активности. Не отвлекайся от главного!",
        "photo_prompt": "📸 Отправь мне фото своего рабочего места, блокнота с задачами или тренировки — я дам тебе заряд мотивации и совет!",
        "photo_received": "🔥 Отличное фото! Вижу твою целеустремленность. Продолжай в том же духе, ты на верном пути!",
        "profile_text": (
            "👤 **Твой профиль: {name}**\n\n"
            "🌐 Язык: Русский\n"
            "💎 Статус: {status}\n"
            "👥 Приглашено друзей: {friends}\n\n"
            "🔗 Твоя ссылка для приглашения:\n`{ref_link}`\n"
            "_(+7 дней премиума за каждого друга!)_"
        ),
        "status_free": "Базовый доступ",
        "status_premium": "Премиум до {date} ({days} дн.)",
        "premium_activated": "🎉 **ПРЕМИУМ АКТИВИРОВАН!**\n\nТеперь тебе доступны:\n• Утренние и вечерние аудио-напутствия\n• Персональные планы\n• Приоритетные ответы",
        "premium_voice_congrats": "Поздравляю с премиумом! Теперь я твой личный голосовой коуч 24 на 7.",
        "already_premium": "⭐️ У тебя уже активен Premium! Осталось дней: {days}.",
        "invite_info": (
            "🎁 Приглашай друзей в DailyBoost и получай +7 дней Premium за каждого!\n\n"
            "Твоя персональная ссылка:\n{ref_link}"
        )
    },
    "en": {
        "start": "Hey {name}! I'm DailyBoost — your personal voice coach & motivator!",
        "morning_greeting": "Good morning, {name}! Today is full of opportunities. Let's make it count!",
        "voice_welcome": "Hi {name}! Ready to level up every day?",
        "button_plan": "📋 Today's Plan",
        "button_reminder": "⏰ Quick Reminder",
        "button_photo": "📸 Photo Analysis",
        "button_profile": "👤 My Profile & Goals",
        "button_premium": "⭐️ DailyBoost Premium",
        "plan_text": "🎯 **Your plan for today:**\n1. 💧 Drink a glass of water and stretch\n2. 🚀 Complete the #1 MIT (Most Important Task) for 45 mins\n3. 📚 Read or learn for 20 minutes\n4. 🚶 Go for a brisk walk\n\n*Quote of the day: Consistency is king!*",
        "reminder_text": "⏰ **Reminder scheduled!**\nI'll check in with you in 2 hours. Stay focused!",
        "photo_prompt": "📸 Send me a photo of your workspace, journal, or workout — I'll give you a motivational boost!",
        "photo_received": "🔥 Great photo! Keep pushing forward, you're making steady progress!",
        "profile_text": (
            "👤 **Profile: {name}**\n\n"
            "🌐 Language: English\n"
            "💎 Status: {status}\n"
            "👥 Friends invited: {friends}\n\n"
            "🔗 Your referral link:\n`{ref_link}`\n"
            "_(+7 days of Premium for each invited friend!)_"
        ),
        "status_free": "Free Tier",
        "status_premium": "Premium until {date} ({days} days)",
        "premium_activated": "🎉 **PREMIUM ACTIVATED!**\n\nUnlocked features:\n• Daily morning & evening voice guidance\n• Tailored action plans\n• Ad-free experience",
        "premium_voice_congrats": "Congratulations on getting Premium! I am now your personal 24/7 voice coach.",
        "already_premium": "⭐️ You already have active Premium! {days} days remaining.",
        "invite_info": (
            "🎁 Invite friends to DailyBoost and get +7 days of Premium for each!\n\n"
            "Your link:\n{ref_link}"
        )
    },
    "es": {
        "start": "¡Hola, {name}! Soy DailyBoost — ¡tu coach y motivador personal por voz!",
        "morning_greeting": "¡Buenos días, {name}! Cada día es una nueva oportunidad. ¡A darlo todo hoy!",
        "voice_welcome": "¡Hola, {name}! ¿Listo para mejorar cada día?",
        "button_plan": "📋 Plan de hoy",
        "button_reminder": "⏰ Recordatorio rápido",
        "button_photo": "📸 Analizar foto",
        "button_profile": "👤 Mi perfil y objetivos",
        "button_premium": "⭐️ DailyBoost Premium",
        "plan_text": "🎯 **Tu plan de hoy:**\n1. 💧 Tomar un vaso de agua y estirarse\n2. 🚀 Completar la tarea principal (sesión de foco 45 min)\n3. 📚 Leer o aprender durante 20 minutos\n4. 🚶 Caminata al aire libre\n\n*Consejo: La disciplina vence a la motivación.*",
        "reminder_text": "⏰ **¡Recordatorio configurado!**\nTe escribiré en 2 horas para revisar tu progreso.",
        "photo_prompt": "📸 Envíame una foto de tu espacio de trabajo o rutina y te daré un consejo motivador.",
        "photo_received": "🔥 ¡Excelente foto! Veo tu dedicación. ¡Sigue así!",
        "profile_text": (
            "👤 **Perfil: {name}**\n\n"
            "🌐 Idioma: Español\n"
            "💎 Estado: {status}\n"
            "👥 Amigos invitados: {friends}\n\n"
            "🔗 Tu enlace de invitación:\n`{ref_link}`\n"
            "_(¡+7 días de Premium por cada amigo!)_"
        ),
        "status_free": "Acceso básico",
        "status_premium": "Premium hasta {date} ({days} días)",
        "premium_activated": "🎉 **¡PREMIUM ACTIVADO!**\n\nFunciones desbloqueadas:\n• Audios diarios de motivación\n• Planes personalizados\n• Soporte prioritario",
        "premium_voice_congrats": "¡Felicidades por tu suscripción Premium! Ahora soy tu coach de voz 24/7.",
        "already_premium": "⭐️ ¡Ya tienes Premium activo! Te quedan {days} días.",
        "invite_info": (
            "🎁 ¡Invita a tus amigos y consigue +7 días de Premium gratis!\n\n"
            "Tu enlace:\n{ref_link}"
        )
    }
}


def t(lang: str, key: str, **kw: Any) -> str:
    """Translates a message key into the requested language with fallback to English."""
    lang_dict = LANGUAGES.get(lang, LANGUAGES["en"])
    template = lang_dict.get(key, LANGUAGES["en"].get(key, key))
    try:
        return template.format(**kw)
    except KeyError:
        return template
