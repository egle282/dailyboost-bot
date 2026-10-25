"""Voice generation module for DailyBoost bot.
Utilizes edge-tts for high-quality, free multilingual speech synthesis.
"""
import asyncio
import os
import uuid
import logging
from typing import Optional

logger = logging.getLogger("DailyBoost")

VOICE_DIR = "temp_audio"
VOICES = {
    "ru": "ru-RU-SvetlanaNeural",
    "en": "en-US-AriaNeural",
    "es": "es-ES-ElviraNeural"
}


def ensure_temp_dir() -> None:
    """Ensures temporary voice directory exists."""
    os.makedirs(VOICE_DIR, exist_ok=True)


async def _generate_tts_async(text: str, voice_code: str, output_path: str) -> None:
    """Invokes edge-tts to write audio file asynchronously."""
    import edge_tts
    communicate = edge_tts.Communicate(text, voice_code)
    await communicate.save(output_path)


def text_to_voice(text: str, lang: str = "ru") -> Optional[str]:
    """Generates an ogg/mp3 audio file from text. Returns filepath or None on failure."""
    try:
        ensure_temp_dir()
        voice_code = VOICES.get(lang, VOICES["en"])
        filename = f"voice_{uuid.uuid4().hex[:8]}.ogg"
        filepath = os.path.join(VOICE_DIR, filename)

        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Running within active loop: run in separate thread
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    pool.submit(asyncio.run, _generate_tts_async(text, voice_code, filepath)).result()
            else:
                loop.run_until_complete(_generate_tts_async(text, voice_code, filepath))
        except RuntimeError:
            asyncio.run(_generate_tts_async(text, voice_code, filepath))

        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            return filepath
        return None
    except Exception as e:
        logger.warning(f"Voice generation failed: {e}. Falling back to text.")
        return None
