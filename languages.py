LANGUAGES = {
    "ru": {"start": "Привет, {name}! Я DailyBoost — твой голосовой мотиватор!", "morning_greeting": "Доброе утро, {name}!", "voice_welcome": "Привет, {name}! Я твой личный коуч. Готов стать лучше?", "button_plan": "Сегодняшний план", "button_reminder": "Быстрое напоминание", "button_photo": "Анализ фото", "button_profile": "Мой профиль и цели"},
    "en": {"start": "Hey {name}! I'm DailyBoost — your voice coach!", "morning_greeting": "Good morning, {name}!", "voice_welcome": "Hi {name}! Ready to level up every day?", "button_plan": "Today’s Plan", "button_reminder": "Quick Reminder", "button_photo": "Photo Analysis", "button_profile": "My Profile & Goals"},
    "es": {"start": "¡Hola, {name}! Soy DailyBoost — tu coach con voz!", "morning_greeting": "¡Buenos días, {name}!", "voice_welcome": "¡Hola, {name}! ¿Listo para mejorar cada día?", "button_plan": "Plan de hoy", "button_reminder": "Recordatorio rápido", "button_photo": "Analizar foto", "button_profile": "Mi perfil y objetivos"}
}

def t(lang, key, **kw):
    return LANGUAGES.get(lang, LANGUAGES["en"]).get(key, key).format(**kw)
