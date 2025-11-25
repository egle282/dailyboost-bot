import logging, os, traceback
logging.basicConfig(filename='log.txt', level=logging.INFO)
logger = logging.getLogger("DailyBoost")

def safe_execute(func):
    def wrapper(message):
        try: return func(message)
        except Exception as e:
            logger.error(f"Ошибка: {traceback.format_exc()}")
    return wrapper

def safe_send(bot, chat_id, text=None, voice_path=None):
    try:
        if voice_path:
            with open(voice_path, 'rb') as f:
                bot.send_voice(chat_id, f)
            os.remove(voice_path)
        elif text:
            bot.send_message(chat_id, text)
    except: pass
