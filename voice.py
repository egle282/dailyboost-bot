import asyncio, edge_tts, os
from datetime import datetime

async def tts(text, lang="ru"):
    voice = {"ru": "ru-RU-SvetlanaNeural", "en": "en-US-AriaNeural", "es": "es-ES-ElviraNeural"}[lang]
    file = f"voice_{int(datetime.now().timestamp())}.ogg"
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(file)
    return file

def text_to_voice(text, lang="ru"):
    return asyncio.run(tts(text, lang))
