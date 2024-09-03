import logging
from datetime import datetime, timedelta

import asyncio
from pyrogram import filters, Client
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InlineKeyboardMarkup

from CineWinx import app, Telegram
from CineWinx.core.call import CineWinx
from CineWinx.misc import db
from CineWinx.utils import (
    get_lang,
    is_active_chat,
    telegram_markup,
)
from CineWinx.utils.stream.chat import get_music_list_from_group
from CineWinx.utils.stream.queue import put_queue
from config import PREFIXES, BANNED_USERS, TELEGRAM_AUDIO_URL
from strings import get_command, get_string

ADD_COMMAND = get_command("ADD_COMMAND")

last_played_date = None
last_played_message_id = None

@app.on_message(filters.command(ADD_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS)
async def add_command(client: Client, message: Message):
    global last_played_date, last_played_message_id
    language = await get_lang(message.chat.id)
    _ = get_string(language)

    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    try:
        num_songs = int(message.command[1])
    except (IndexError, ValueError):
        await message.reply_text("🎶 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗲𝘀𝗽𝗲𝗰𝗶𝗳𝗶𝗾𝘂𝗲 𝘂𝗺 𝗻𝘂́𝗺𝗲𝗿𝗼 𝘃𝗮́𝗹𝗶𝗱𝗼 𝗱𝗲 𝗺𝘂́𝘀𝗶𝗰𝗮𝘀 𝗽𝗮𝗿𝗮 𝗮𝗱𝗶𝗰𝗶𝗼𝗻𝗮𝗿. 🎵")
        return

    mystic = await message.reply_text(f"🔍 𝗣𝗲𝘀𝗾𝘂𝗶𝘀𝗮𝗻𝗱𝗼 𝗮𝘀 𝘂𝗹𝘁𝗶𝗺𝗮𝘀 {num_songs} 𝗺𝘂́𝘀𝗶𝗰𝗮𝘀 𝗻𝗼 𝗰𝗵𝗮𝘁 ...")

    if last_played_date is None:
        last_played_date = datetime.now()

    added_songs = 0
    days_checked = 0

    while added_songs < num_songs and days_checked < 5:
        music_list = await get_music_list_from_group(
            client, mystic, chat_id, last_played_date, last_played_message_id
        )

        if not music_list:
            last_played_date -= timedelta(days=1)
            last_played_message_id = None
            days_checked += 1
            continue

        for music in music_list:
            if added_songs >= num_songs:
                break

            file_path = music["file_path"]
            message_id = music["message_id"]

            music_message = await client.get_messages(chat_id, message_ids=[message_id])

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
                    db[chat_id] = []

                    await CineWinx.join_call(chat_id, chat_id, details["path"])

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
                        caption=_["stream_1"].format(
                            details["title"], details["link"], details["dur"], user_name
                        ),
                        reply_markup=InlineKeyboardMarkup(button),
                    )

                    db[chat_id][0]["mystic"] = run
                    db[chat_id][0]["markup"] = "tg"

            last_played_message_id = message_id
            added_songs += 1

        if len(music_list) < 10:
            last_played_date -= timedelta(days=1)
            last_played_message_id = None
            days_checked += 1

        if added_songs < num_songs and days_checked < 5:
            try:
                await asyncio.sleep(30)
                continue
            except asyncio.TimeoutError:
                break

    if added_songs == 0:
        try:
            await mystic.edit_text("❌ 𝗡𝗮̃𝗼 𝗳𝗼𝗶 𝗽𝗼𝘀𝘀𝗶́𝘃𝗲𝗹 𝗲𝗻𝗰𝗼𝗻𝘁𝗿𝗮𝗿 𝗺𝘂́𝘀𝗶𝗰𝗮𝘀 𝗻𝗼𝘀 𝘂́𝗹𝘁𝗶𝗺𝗼𝘀 𝟱 𝗱𝗶𝗮𝘀.")
        except FloodWait as f:
            await asyncio.sleep(f.value)
        except Exception as e:
            logging.error(str(e))
            pass
    else:
        await mystic.edit_text(f"🎶 𝗔𝗱𝗶𝗰𝗶𝗼𝗻𝗮𝗱𝗼 {added_songs} 𝗺𝘂́𝘀𝗶𝗰𝗮𝘀 𝗮̀ 𝘀𝘁𝗿𝗲𝗮𝗺.")
