import logging
import os
import re

import yt_dlp
from pykeyboard import InlineKeyboard
from pyrogram import enums, filters, Client
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaAudio,
    InputMediaVideo,
    Message,
    CallbackQuery,
)

from CineWinx import YouTube, app
from CineWinx.utils.decorators.language import language, language_cb
from CineWinx.utils.formatters import convert_bytes
from CineWinx.utils.inline.song import song_markup
from config import (
    BANNED_USERS,
    SONG_DOWNLOAD_DURATION,
    SONG_DOWNLOAD_DURATION_LIMIT,
    PREFIXES,
)
from strings import get_command

SONG_COMMAND = get_command("SONG_COMMAND")


@app.on_message(filters.command(SONG_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS)
@language
async def song_commad_group(_client: Client, message: Message, _):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["SG_B_1"],
                    url=f"https://t.me/{app.username}?start=song",
                ),
            ]
        ]
    )
    await message.reply_text(_["song_1"], reply_markup=upl)


# Song Module


@app.on_message(
    filters.command(SONG_COMMAND, PREFIXES) & filters.private & ~BANNED_USERS
)
@language
async def song_commad_private(_client: Client, message: Message, _):
    await message.delete()

    url = await YouTube.url(message)
    if url:
        if not await YouTube.exists(url):
            return await message.reply_text(_["song_5"])
        mystic = await message.reply_text(_["play_1"])
        (
            title,
            duration_min,
            duration_sec,
            thumbnail,
            vidid,
        ) = await YouTube.details(url)

        if str(duration_min) == "None":
            return await mystic.edit_text(_["song_3"])

        if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
            return await mystic.edit_text(
                _["play_4"].format(SONG_DOWNLOAD_DURATION, duration_min)
            )

        buttons = song_markup(_, vidid)
        await mystic.delete()
        return await message.reply_photo(
            thumbnail,
            caption=_["song_4"].format(title),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        if len(message.command) < 2:
            return await message.reply_text(_["song_2"])
    mystic = await message.reply_text(_["play_1"])
    query = message.text.split(None, 1)[1]

    try:
        (
            title,
            duration_min,
            duration_sec,
            thumbnail,
            vidid,
        ) = await YouTube.details(query)
    except Exception as e:
        logging.exception(e)
        return await mystic.edit_text(_["play_3"])

    if str(duration_min) == "None":
        return await mystic.edit_text(_["song_3"])

    if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
        return await mystic.edit_text(
            _["play_6"].format(SONG_DOWNLOAD_DURATION, duration_min)
        )

    buttons = song_markup(_, vidid)
    await mystic.delete()

    return await message.reply_photo(
        thumbnail,
        caption=_["song_4"].format(title),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex(pattern=r"song_back") & ~BANNED_USERS)
@language_cb
async def songs_back_helper(_client: app, callback_query: CallbackQuery, _):
    callback_data = callback_query.data.strip()

    callback_request = callback_data.split(None, 1)[1]
    stype, vidid = callback_request.split("|")

    buttons = song_markup(_, vidid)

    return await callback_query.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex(pattern=r"song_helper") & ~BANNED_USERS)
@language_cb
async def song_helper_cb(_client: app, callback_query: CallbackQuery, _):
    callback_data = callback_query.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, vidid = callback_request.split("|")
    try:
        await callback_query.answer(_["song_6"], show_alert=True)
    except Exception as e:
        logging.exception(e)
    if stype == "audio":
        try:
            formats_available, link = await YouTube.formats(vidid, True)
        except Exception as e:
            logging.exception(e)
            return await callback_query.edit_message_text(_["song_7"])
        keyboard = InlineKeyboard()
        done = []
        for x in formats_available:
            check = x["format"]
            if "audio" in check:
                if x["filesize"] is None:
                    continue
                form = x["format_note"].title()
                if form not in done:
                    done.append(form)
                else:
                    continue
                sz = convert_bytes(x["filesize"])
                fom = x["format_id"]
                keyboard.row(
                    InlineKeyboardButton(
                        text=f"🎵 𝗤𝘂𝗮𝗹𝗶𝗱𝗮𝗱𝗲 𝗱𝗼 𝗮𝘂𝗱𝗶𝗼 = {sz}",
                        callback_data=f"song_download {stype}|{fom}|{vidid}",
                    ),
                )

        keyboard.row(
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data=f"song_back {stype}|{vidid}",
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"close"),
        )
        return await callback_query.edit_message_reply_markup(reply_markup=keyboard)

    else:
        try:
            formats_available, link = await YouTube.formats(vidid, True)
        except Exception as e:
            print(e)
            return await callback_query.edit_message_text(_["song_7"])

        keyboard = InlineKeyboard()

        # AVC Formats Only [ Alexa MUSIC BOT ]
        done = [160, 133, 134, 135, 136, 137, 298, 299, 264, 304, 266]
        for x in formats_available:
            check = x["format"]
            if x["filesize"] is None:
                continue

            if int(x["format_id"]) not in done:
                continue
            sz = convert_bytes(x["filesize"])
            ap = check.split("-")[1]
            to = f"{ap} = {sz}"

            keyboard.row(
                InlineKeyboardButton(
                    text=to,
                    callback_data=f"song_download {stype}|{x['format_id']}|{vidid}",
                )
            )

        keyboard.row(
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data=f"song_back {stype}|{vidid}",
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"close"),
        )

        return await callback_query.edit_message_reply_markup(reply_markup=keyboard)


# Downloading Songs Here


@app.on_callback_query(filters.regex(pattern=r"song_download") & ~BANNED_USERS)
@language_cb
async def song_download_cb(_client: app, callback_query: CallbackQuery, _):
    try:
        await callback_query.answer("⬇️ 𝗕𝗮𝗶𝘅𝗮𝗻𝗱𝗼...")
    except Exception as e:
        logging.exception(e)

    callback_data = callback_query.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, format_id, vidid = callback_request.split("|")
    mystic = await callback_query.edit_message_text(_["song_8"])
    yturl = f"https://www.youtube.com/watch?v={vidid}"

    with yt_dlp.YoutubeDL({"quiet": True}) as ytdl:
        x = ytdl.extract_info(yturl, download=False)
    title = (x["title"]).title()
    title = re.sub(r"\W+", " ", title)
    thumb_image_path = await callback_query.message.download()
    duration = x["duration"]

    if stype == "video":
        thumb_image_path = await callback_query.message.download()
        width = callback_query.message.photo.width
        height = callback_query.message.photo.height
        try:
            file_path = await YouTube.download(
                yturl,
                mystic,
                songvideo=True,
                format_id=format_id,
                title=title,
            )
        except Exception as e:
            return await mystic.edit_text(_["song_9"].format(e))
        med = InputMediaVideo(
            media=file_path,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb_image_path,
            caption=title,
            supports_streaming=True,
        )

        await mystic.edit_text(_["song_11"])

        await app.send_chat_action(
            chat_id=callback_query.message.chat.id,
            action=enums.ChatAction.UPLOAD_VIDEO,
        )

        try:
            await callback_query.edit_message_media(media=med)
        except Exception as e:
            print(e)
            return await mystic.edit_text(_["song_10"])
        os.remove(file_path)

    elif stype == "audio":
        try:
            filename = await YouTube.download(
                yturl,
                mystic,
                songaudio=True,
                format_id=format_id,
                title=title,
            )
        except Exception as e:
            return await mystic.edit_text(_["song_9"].format(e))

        med = InputMediaAudio(
            media=filename,
            caption=title,
            thumb=thumb_image_path,
            title=title,
            performer=x["uploader"],
        )

        await mystic.edit_text(_["song_11"])

        await app.send_chat_action(
            chat_id=callback_query.message.chat.id,
            action=enums.ChatAction.UPLOAD_AUDIO,
        )

        try:
            await callback_query.edit_message_media(media=med)
        except Exception as e:
            print(e)
            return await mystic.edit_text(_["song_10"])

        os.remove(filename)
