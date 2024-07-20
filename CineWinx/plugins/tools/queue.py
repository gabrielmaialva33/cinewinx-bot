import asyncio
import logging

from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.types import CallbackQuery, InputMediaPhoto, Message

import config
from CineWinx import app
from CineWinx.misc import db
from CineWinx.utils import winx_bin, get_channeplay_cb, seconds_to_min
from CineWinx.utils.database import get_cmode, is_active_chat, is_music_playing
from CineWinx.utils.decorators.language import language, language_cb
from CineWinx.utils.inline import queue_back_markup, queue_markup
from config import BANNED_USERS, PREFIXES
from strings import get_command

QUEUE_COMMAND = get_command("QUEUE_COMMAND")

basic = {}


def get_image(video_id: str):
    try:
        url = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        return url
    except Exception as e:
        logging.error(str(e))
        return config.YOUTUBE_IMG_URL


def get_duration(playing):
    file_path = playing[0]["file"]
    if "index_" in file_path or "live_" in file_path:
        return "Unknown"
    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        return "Unknown"
    else:
        return "Inline"


@app.on_message(filters.command(QUEUE_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS)
@language
async def ping_com(_client: app, message: Message, _):
    if message.command[0][0] == "c":
        chat_id = await get_cmode(message.chat.id)
        if chat_id is None:
            return await message.reply_text(_["setting_12"])
        try:
            await app.get_chat(chat_id)
        except Exception as e:
            logging.error(str(e))
            return await message.reply_text(_["cplay_4"])
        cplay = True
    else:
        chat_id = message.chat.id
        cplay = False
    if not await is_active_chat(chat_id):
        return await message.reply_text(_["general_6"])
    got = db.get(chat_id)
    if not got:
        return await message.reply_text(_["queue_2"])
    file = got[0]["file"]
    videoid = got[0]["vidid"]
    user = got[0]["by"]
    title = (got[0]["title"]).title()
    typo = (got[0]["streamtype"]).title()
    DUR = get_duration(got)
    if "live_" in file:
        IMAGE = get_image(videoid)
    elif "vid_" in file:
        IMAGE = get_image(videoid)
    elif "index_" in file:
        IMAGE = config.STREAM_IMG_URL
    else:
        if videoid == "telegram":
            IMAGE = (
                config.TELEGRAM_AUDIO_URL
                if typo == "Audio"
                else config.TELEGRAM_VIDEO_URL
            )
        elif videoid == "soundcloud":
            IMAGE = config.SOUNCLOUD_IMG_URL
        else:
            IMAGE = get_image(videoid)
    send = (
        "<b>⌛️ 𝗗𝘂𝗿𝗮𝗰̧𝗮̃𝗼:</b> 𝗧𝗿𝗮𝗻𝘀𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗱𝗲 𝗱𝘂𝗿𝗮𝗰̧𝗮̃𝗼 𝗶𝗻𝗱𝗲𝘁𝗲𝗿𝗺𝗶𝗻𝗮𝗱𝗮.\n\n"
        "📋 𝗖𝗹𝗶𝗾𝘂𝗲 𝗻𝗼 𝗯𝗼𝘁𝗮̃𝗼 𝗮𝗯𝗮𝗶𝘅𝗼 𝗽𝗮𝗿𝗮 𝘃𝗲𝗿 𝗮 𝗹𝗶𝘀𝘁𝗮 𝗰𝗼𝗺𝗽𝗹𝗲𝘁𝗮 𝗱𝗮 "
        "𝗳𝗶𝗹𝗮."
        if DUR == "Unknown"
        else "📋 𝗖𝗹𝗶𝗾𝘂𝗲 𝗻𝗼 𝗯𝗼𝘁𝗮̃𝗼 𝗮𝗯𝗮𝗶𝘅𝗼 𝗽𝗮𝗿𝗮 𝘃𝗲𝗿 𝗮 𝗹𝗶𝘀𝘁𝗮 𝗰𝗼𝗺𝗽𝗹𝗲𝘁𝗮 𝗱𝗮 𝗳𝗶𝗹𝗮."
    )
    cap = f"""<b>{app.mention} 𝗣𝗹𝗮𝘆𝗲𝗿</b>

🎥 <b>𝗧𝗼𝗰𝗮𝗻𝗱𝗼:</b> {title}

🔗 <b>𝗧𝗶𝗽𝗼 𝗱𝗲 𝗦𝘁𝗿𝗲𝗮𝗺:</b> {typo}
🙍‍♂️ <b>𝗔𝗱𝗶𝗰𝗶𝗼𝗻𝗮𝗱𝗼 𝗽𝗼𝗿:</b> {user}
    {send}"""
    upl = (
        queue_markup(_, DUR, "c" if cplay else "g", videoid)
        if DUR == "Unknown"
        else queue_markup(
            _,
            DUR,
            "c" if cplay else "g",
            videoid,
            seconds_to_min(got[0]["played"]),
            got[0]["dur"],
        )
    )
    basic[videoid] = True
    mystic = await message.reply_photo(IMAGE, caption=cap, reply_markup=upl)
    if DUR != "Unknown":
        try:
            while db[chat_id][0]["vidid"] == videoid:
                await asyncio.sleep(5)
                if await is_active_chat(chat_id):
                    if basic[videoid]:
                        if await is_music_playing(chat_id):
                            try:
                                buttons = queue_markup(
                                    _,
                                    DUR,
                                    "c" if cplay else "g",
                                    videoid,
                                    seconds_to_min(db[chat_id][0]["played"]),
                                    db[chat_id][0]["dur"],
                                )
                                await mystic.edit_reply_markup(reply_markup=buttons)
                            except FloodWait:
                                pass
                        else:
                            pass
                    else:
                        break
                else:
                    break
        except Exception as e:
            logging.error(str(e))
            return


@app.on_callback_query(filters.regex("GetTimer") & ~BANNED_USERS)
async def quite_timer(_client: app, callback_query: CallbackQuery):
    try:
        await callback_query.answer()
    except FloodWait:
        pass


@app.on_callback_query(filters.regex("GetQueued") & ~BANNED_USERS)
@language_cb
async def queued_tracks(_client: app, callback_query: CallbackQuery, _):
    callback_data = callback_query.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    what, videoid = callback_request.split("|")
    try:
        chat_id, channel = await get_channeplay_cb(_, what, callback_query)
    except Exception as e:
        logging.error(str(e))
        return
    if not await is_active_chat(chat_id):
        return await callback_query.answer(_["general_6"], show_alert=True)
    got = db.get(chat_id)
    if not got:
        return await callback_query.answer(_["queue_2"], show_alert=True)
    if len(got) == 1:
        return await callback_query.answer(_["queue_5"], show_alert=True)
    await callback_query.answer()
    basic[videoid] = False
    buttons = queue_back_markup(_, what)
    med = InputMediaPhoto(
        media="https://telegra.ph/file/a52fcc73359b00743e75b.jpg",
        caption=_["queue_1"],
    )
    await callback_query.edit_message_media(media=med)
    j = 0
    msg = ""
    for x in got:
        j += 1
        if j == 1:
            msg += f'Tocando agora:\n\n🏷 Título: {x["title"]}\nDuração: {x["dur"]}\nPor: {x["by"]}\n\n'
        elif j == 2:
            msg += f'Na fila:\n\n🏷 Título: {x["title"]}\nDuração: {x["dur"]}\nPor: {x["by"]}\n\n'
        else:
            msg += f'🏷 Título: {x["title"]}\nDuração: {x["dur"]}\nPor: {x["by"]}\n\n'
    if "Queued" in msg:
        if len(msg) < 700:
            await asyncio.sleep(1)
            return await callback_query.edit_message_text(msg, reply_markup=buttons)

        if "🏷" in msg:
            msg = msg.replace("🏷", "")
        if "Atualmente tocando" in msg:
            msg = msg.replace("Tocando agora", "Tocando Agora")
        if "Título" in msg:
            msg = msg.replace("Título", "Título")
        if "Duração" in msg:
            msg = msg.replace("Duração", "Duração")
        if "Por" in msg:
            msg = msg.replace("Por", "Por")
        if "Na fila" in msg:
            msg = msg.replace("Na fila", "Na Fila")

        link = await winx_bin(msg)
        await callback_query.edit_message_text(
            _["queue_3"].format(link), reply_markup=buttons
        )
    else:
        if len(msg) > 700:
            if "🏷" in msg:
                msg = msg.replace("🏷", "")
            if "Atualmente tocando" in msg:
                msg = msg.replace("Tocando agora", "Tocando Agora")
            if "Título" in msg:
                msg = msg.replace("Título", "Título")
            if "Duração" in msg:
                msg = msg.replace("Duração", "Duração")
            if "Por" in msg:
                msg = msg.replace("Por", "Por")
            if "Na fila" in msg:
                msg = msg.replace("Na fila", "Na Fila")

            link = await winx_bin(msg)
            await asyncio.sleep(1)
            return await callback_query.edit_message_text(
                _["queue_3"].format(link), reply_markup=buttons
            )

        await asyncio.sleep(1)
        return await callback_query.edit_message_text(msg, reply_markup=buttons)


@app.on_callback_query(filters.regex("queue_back_timer") & ~BANNED_USERS)
@language_cb
async def queue_back(_client: app, callback_query: CallbackQuery, _):
    callback_data = callback_query.data.strip()
    cplay = callback_data.split(None, 1)[1]
    try:
        chat_id, channel = await get_channeplay_cb(_, cplay, callback_query)
    except Exception as e:
        logging.error(str(e))
        return
    if not await is_active_chat(chat_id):
        return await callback_query.answer(_["general_6"], show_alert=True)
    got = db.get(chat_id)
    if not got:
        return await callback_query.answer(_["queue_2"], show_alert=True)
    await callback_query.answer(_["set_cb_8"], show_alert=True)
    file = got[0]["file"]
    videoid = got[0]["vidid"]
    user = got[0]["by"]
    title = (got[0]["title"]).title()
    typo = (got[0]["streamtype"]).title()
    DUR = get_duration(got)
    if "live_" in file:
        IMAGE = get_image(videoid)
    elif "vid_" in file:
        IMAGE = get_image(videoid)
    elif "index_" in file:
        IMAGE = config.STREAM_IMG_URL
    else:
        if videoid == "telegram":
            IMAGE = (
                config.TELEGRAM_AUDIO_URL
                if typo == "Audio"
                else config.TELEGRAM_VIDEO_URL
            )
        elif videoid == "soundcloud":
            IMAGE = config.SOUNCLOUD_IMG_URL
        else:
            IMAGE = get_image(videoid)
    send = (
        "<b>⌛️Duração:</b> duração indeterminada.\n\n"
        "Clique no botão abaixo para ver a lista completa da "
        "fila."
        if DUR == "Unknown"
        else "\nClique no botão abaixo para ver a lista completa da fila."
    )
    cap = f"""<b>{app.mention} Player</b>

🎥<b>Tocando:</b> {title}

🔗<b>Tipo de stream:</b> {typo}
🙍‍♂️<b>Adicionado por:</b> {user}
{send}"""
    upl = (
        queue_markup(_, DUR, cplay, videoid)
        if DUR == "Unknown"
        else queue_markup(
            _,
            DUR,
            cplay,
            videoid,
            seconds_to_min(got[0]["played"]),
            got[0]["dur"],
        )
    )
    basic[videoid] = True

    med = InputMediaPhoto(media=IMAGE, caption=cap)
    mystic = await callback_query.edit_message_media(media=med, reply_markup=upl)
    if DUR != "Unknown":
        try:
            while db[chat_id][0]["vidid"] == videoid:
                await asyncio.sleep(5)
                if await is_active_chat(chat_id):
                    if basic[videoid]:
                        if await is_music_playing(chat_id):
                            try:
                                buttons = queue_markup(
                                    _,
                                    DUR,
                                    cplay,
                                    videoid,
                                    seconds_to_min(db[chat_id][0]["played"]),
                                    db[chat_id][0]["dur"],
                                )
                                await mystic.edit_reply_markup(reply_markup=buttons)
                            except FloodWait:
                                pass
                        else:
                            pass
                    else:
                        break
                else:
                    break
        except Exception as e:
            logging.error(str(e))
            return
