# ⚡ DailyBoost Bot — Multilingual Voice Coach & Motivator

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Telegram Stars](https://img.shields.io/badge/Monetization-Telegram%20Stars-blue.svg)](https://telegram.org/blog/telegram-stars)
[![Code Style: ReFF](https://img.shields.io/badge/Code%20Style-ReFF%20(<200%20lines)-green.svg)](AGENTS.md)

**DailyBoost Bot** — это умный персональный ассистент и голосовой коуч в Telegram, созданный для повышения личной продуктивности, фокуса и мотивации.

Бот поддерживает многоязычность (🇷🇺 Русский, 🇬🇧 English, 🇪🇸 Español), синтез естественной речи на базе Edge-TTS, реферальную программу с бонусами и прямую оплату подписки через **Telegram Stars (XTR)**.

---

## ✨ Ключевые возможности

- 🎙 **Естественный голос**: Интеграция с нейросетевым синтезом речи Microsoft Edge-TTS без ограничений и платных API ключей.
- 🌍 **Мультиязычность**: Автоматическое определение языка пользователя Telegram (RU, EN, ES) с возможностью переключения.
- 📋 **План дня & Фокус**: Интерактивные рекомендации по планированию дня, питью воды и глубокому фокусу.
- ⏰ **Умные напоминания**: Фоновые утренние напоминания с использованием `APScheduler`.
- ⭐️ **Монетизация в Telegram Stars**: Оплата подписки прямо внутри мессенджера одной кнопкой без сторонних шлюзов.
- 👥 **Виральная реферальная механика**: Индивидуальные ссылки `t.me/bot?start=USER_ID` с начислением +7 дней Premium за каждого приглашенного друга.
- 🏗 **Чистая архитектура (ReFF & SOLID)**: Модульная структура, валидация входных данных, безопасный SQL и строгий лимит до 200 строк на файл.

---

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/dailyboost_bot.git
cd dailyboost_bot
```

### 2. Настройка виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Настройка переменных окружения

Создайте файл `.env` на основе [.env.example](.env.example):

```bash
cp .env.example .env
```

Откройте `.env` и вставьте ваш токен бота:

```env
TELEGRAM_TOKEN=123456789:ABCdefGHIjklMNOpqrSTUvwxYZ
```

> **Где взять токен?**  
> Напишите официальному боту [@BotFather](https://t.me/BotFather) в Telegram, отправьте команду `/newbot` и следуйте инструкциям.

### 4. Запуск бота

```bash
python main.py
```

---

## 🐳 Запуск через Docker & Docker Compose

### В одну команду:

```bash
docker-compose up -d --build
```

Просмотр логов:

```bash
docker-compose logs -f
```

Остановка:

```bash
docker-compose down
```

---

## ☁️ Деплой на Render.com (В 1 клик)

1. Создайте форк или загрузите данный репозиторий на ваш GitHub.
2. Авторизуйтесь на [Render.com](https://render.com/).
3. Нажмите **New +** → **Blueprint**.
4. Подключите ваш репозиторий `dailyboost_bot` (файл [render.yaml](render.yaml) настроит всё автоматически как Background Worker).
5. В настройках Environment добавьте переменную `TELEGRAM_TOKEN`.
6. Нажмите **Apply** — бот запустится и будет работать 24/7!

---

## ⭐️ Как включить Telegram Stars для оплаты

Telegram Stars не требуют открытия расчетного счета или заключения договоров с платежными шлюзами.

1. Откройте [@BotFather](https://t.me/BotFather).
2. Выберите вашего бота через `/mybots`.
3. Перейдите в **Bot Settings** → **Payments**.
4. Выберите **Telegram Stars** в качестве провайдера.
5. Готово! Покупки через команду `/premium` или кнопку меню начнут работать мгновенно.

---

## 🧪 Запуск тестов

В проекте настроены unit-тесты для проверки базы данных, локализации и клавиатур:

```bash
python -m unittest discover tests
```

---

## 📂 Структура проекта

```text
├── main.py              # Точка входа, хэндлеры команд и жизненный цикл бота (<200 строк)
├── database.py          # Работа с SQLite, миграции и безопасность запросов
├── keyboards.py         # Reply и Inline клавиатуры интерфейса
├── languages.py         # Словари переводов (RU, EN, ES)
├── voice.py             # Синтез речи Edge-TTS и управление аудиофайлами
├── error_handler.py     # Безопасное выполнение и логирование
├── requirements.txt     # Зависимости проекта
├── Dockerfile           # Docker образ для развертывания
├── docker-compose.yml   # Спецификация Docker Compose
├── render.yaml          # Конфигурация для Render.com
├── tests/               # Автоматические тесты
│   ├── test_database.py
│   └── test_languages.py
└── ROADMAP.md           # Дорожная карта развития проекта
```

---

## 📜 Лицензия

Проект распространяется под свободной лицензией [MIT](LICENSE).
