import random
from datetime import datetime

from pyrogram import Client
from pyrogram.types import Message

from CineWinx import Telegram
from CineWinx.core.userbot import assistants
from CineWinx.utils import get_client, seconds_to_min


async def get_music_list_from_group(
    _client: Client, mystic: Message, chat_id: int, date: datetime, last_id: int | None = None
):
    music_list = []

    winx = random.choice(assistants)
    ubot = await get_client(winx)

    limit_count = 0

    if last_id is not None:
        async for message in ubot.get_chat_history(
            chat_id=chat_id, offset_date=date, offset_id=last_id
        ):
            if message.audio:
                music = await process_audio_message(message)
                music_list.append(music)
                limit_count += 1
                if limit_count == 10:
                    break
    else:
        async for message in ubot.get_chat_history(chat_id=chat_id, offset_date=date):
            if message.audio:
                music = await process_audio_message(message)
                music_list.append(music)
                limit_count += 1
                if limit_count == 10:
                    break

    return music_list


async def process_audio_message(message: Message):
    audio_telegram = message.audio
    duration_min = seconds_to_min(audio_telegram.duration)
    file_path = await Telegram.get_filepath(audio=audio_telegram)

    music = {
        "file_id": message.audio.file_id,
        "duration": message.audio.duration,
        "duration_min": duration_min,
        "title": message.audio.title,
        "file_name": message.audio.file_name,
        "file_size": message.audio.file_size,
        "performer": message.audio.performer,
        "date": message.audio.date,
        "file_path": file_path,
        "message_id": message.id,
    }
    return music