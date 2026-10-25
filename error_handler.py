"""Error handling and safe messaging wrappers for DailyBoost bot.
Ensures stability, prevents unhandled exceptions from stopping polling,
and cleanly manages temporary resources.
"""
import functools
import logging
import os
import traceback
from typing import Callable, Any, Optional

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO
)
logger = logging.getLogger("DailyBoost")


def safe_execute(func: Callable) -> Callable:
    """Decorator to catch and log any exception in Telegram message handlers."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception:
            logger.error(f"Error in {func.__name__}: {traceback.format_exc()}")
            return None
    return wrapper


def safe_send(
    bot: Any,
    chat_id: int,
    text: Optional[str] = None,
    voice_path: Optional[str] = None,
    reply_markup: Optional[Any] = None,
    parse_mode: str = "Markdown"
) -> bool:
    """Sends text or voice message safely. Cleans up voice files automatically."""
    try:
        if voice_path and os.path.exists(voice_path):
            try:
                with open(voice_path, "rb") as audio:
                    bot.send_voice(chat_id, audio, reply_markup=reply_markup)
                return True
            finally:
                try:
                    os.remove(voice_path)
                except OSError:
                    pass

        if text:
            bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode=parse_mode)
            return True
        return False
    except Exception as e:
        logger.error(f"Failed to send message to chat {chat_id}: {e}")
        # Retry plain text if markdown formatting failed
        if text and parse_mode:
            try:
                bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode=None)
                return True
            except Exception:
                pass
        return False
