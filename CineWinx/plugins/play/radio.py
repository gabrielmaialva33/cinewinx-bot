import asyncio
import random
from datetime import datetime, timedelta

import math
from pyrogram import filters, Client
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InlineKeyboardMarkup

from CineWinx import app, Telegram, LOGGER
from CineWinx.core.call import CineWinx
from CineWinx.core.userbot import assistants
from CineWinx.misc import db
from CineWinx.utils import get_client, seconds_to_min, get_lang, is_active_chat, telegram_markup
from CineWinx.utils.stream.queue import put_queue
from config import PREFIXES, BANNED_USERS, TELEGRAM_AUDIO_URL
from strings import get_command, get_string

RADIO_COMMAND = get_command("RADIO_COMMAND")

# Variáveis globais para rastrear progresso
last_played_date = None
last_played_message_id = None

@app.on_message(
    filters.command(RADIO_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS
)
async def radio(client: Client, message: Message):
    global last_played_date, last_played_message_id
    language = await get_lang(message.chat.id)
    _ = get_string(language)

    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    mystic = await message.reply_text("🔍 𝗣𝗲𝘀𝗾𝘂𝗶𝘀𝗮𝗻𝗱𝗼 𝗺𝘂́𝘀𝗶𝗰𝗮𝘀 𝗻𝗼 𝗰𝗵𝗮𝘁...")

    # Inicializa a data para hoje se não houver uma data anterior
    if last_played_date is None:
        last_played_date = datetime.now()

    while True:
        music_list = await get_music_list_from_group(client, mystic, chat_id, last_played_date, last_played_message_id)

        if not music_list:
            # Se não encontrou músicas no dia atual, vá para o próximo dia
            last_played_date -= timedelta(days=1)
            last_played_message_id = None
            continue

        for music in music_list:
            file_path = music["file_path"]
            message_id = music["message_id"]

            music_message = await client.get_messages(
                chat_id, message_ids=[message_id]
            )

            if await Telegram.download(
                    _, message=music_message[0], mystic=mystic, filename=file_path
            ):
                message_link = f"https://t.me/{message.chat.username}/{message.id}"
                details = {
                    "title": music["title"].title(),
                    "link": message_link,
                    "path": file_path,
                    "dur": music["duration_min"],
                }

                if await is_active_chat(chat_id):
                    print("add music to queue", details)
                    await put_queue(
                        chat_id,
                        chat_id,
                        details["path"],
                        details["title"],
                        details["dur"],
                        user_name,
                        "telegram",
                        user_id,
                        "audio",
                    )
                else:
                    print("join call", details)
                    db[chat_id] = []

                    await CineWinx.join_call(chat_id, chat_id, details["path"], None, None)

                    await put_queue(
                        chat_id,
                        chat_id,
                        details["path"],
                        details["title"],
                        details["dur"],
                        user_name,
                        "telegram",
                        user_id,
                        "audio",
                    )

                    button = telegram_markup(_, chat_id)
                    run = await app.send_photo(
                        chat_id,
                        photo=TELEGRAM_AUDIO_URL,
                        caption=_["stream_1"].format(details["title"], details["link"], details["dur"], user_name),
                        reply_markup=InlineKeyboardMarkup(button),
                    )

                    db[chat_id][0]["mystic"] = run
                    db[chat_id][0]["markup"] = "tg"

            # Atualiza a variável global após tocar uma música
            last_played_message_id = message_id

        # Verifica se ainda há músicas no dia atual; caso contrário, avance para o próximo dia
        if len(music_list) < 10:
            last_played_date -= timedelta(days=1)
            last_played_message_id = None

async def get_music_list_from_group(_client: Client, mystic: Message, chat_id: int, date: datetime, last_id: int):
    music_list = []

    winx = random.choice(assistants)
    ubot = await get_client(winx)

    limit_count = 0

    # Verifica se o last_id é None e ajusta a chamada ao get_chat_history
    if last_id is not None:
        async for message in ubot.get_chat_history(chat_id=chat_id, offset_date=date, offset_id=last_id):
            if message.audio:
                # Processa a mensagem de áudio
                music = await process_audio_message(message)
                music_list.append(music)
                limit_count += 1
                if limit_count == 10:
                    break
    else:
        async for message in ubot.get_chat_history(chat_id=chat_id, offset_date=date):
            if message.audio:
                # Processa a mensagem de áudio
                music = await process_audio_message(message)
                music_list.append(music)
                limit_count += 1
                if limit_count == 10:
                    break

    return music_list

async def process_audio_message(message):
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
