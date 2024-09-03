import logging

import asyncio
import requests
from pyrogram import filters, Client
from pyrogram.errors import FloodWait
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    InputMediaAnimation,
    Message,
)

from config import BANNED_USERS, PREFIXES
from CineWinx import app

close_keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(text="𝗔𝘁𝘂𝗮𝗹𝗶𝘇𝗮𝗿", callback_data="refresh_cat")],
        [InlineKeyboardButton(text="𝗙𝗲𝗰𝗵𝗮𝗿", callback_data="close")],
    ]
)


@app.on_message(filters.command("cat", PREFIXES) & ~BANNED_USERS)
async def cat(_client: Client, m: Message):
    r = requests.get("https://api.thecatapi.com/v1/images/search")
    if r.status_code == 200:
        data = r.json()
        cat_url = data[0]["url"]
        if cat_url.endswith(".gif"):
            await m.reply_animation(
                cat_url, caption="𝗠𝗲𝗼𝘄 🐾", reply_markup=close_keyboard
            )
        else:
            await m.reply_photo(cat_url, caption="𝗠𝗲𝗼𝘄 🐾", reply_markup=close_keyboard)
    else:
        await m.reply_text("𝗡𝗮̃𝗼 𝗳𝗼𝗶 𝗽𝗼𝘀𝘀𝗶́𝘃𝗲𝗹 𝗯𝘂𝘀𝗰𝗮𝗿 𝘂𝗺𝗮 𝗳𝗼𝘁𝗼 𝗱𝗲 𝗴𝗮𝘁𝗶𝗻𝗵𝗼 🙀")


@app.on_callback_query(filters.regex("refresh_cat") & ~BANNED_USERS)
async def refresh_cat(_client: Client, m: CallbackQuery):
    r = requests.get("https://api.thecatapi.com/v1/images/search")
    if r.status_code == 200:
        data = r.json()
        cat_url = data[0]["url"]
        if cat_url.endswith(".gif"):
            await m.edit_message_media(
                InputMediaAnimation(media=cat_url, caption="𝗠𝗲𝗼𝘄 🐾"),
                reply_markup=close_keyboard,
            )
        else:
            try:
                await m.edit_message_media(
                    InputMediaPhoto(media=cat_url, caption="𝗠𝗲𝗼𝘄 🐾"),
                    reply_markup=close_keyboard,
                )
            except FloodWait as f:
                logging.warning(f)
                await asyncio.sleep(f.value)
                await m.edit_message_media(
                    InputMediaPhoto(media=cat_url, caption="𝗠𝗲𝗼𝘄 🐾"),
                    reply_markup=close_keyboard,
                )
            except Exception as e:
                logging.error(e)
                pass
    else:
        await m.edit_message_text("𝗡𝗮̃𝗼 𝗳𝗼𝗶 𝗽𝗼𝘀𝘀𝗶́𝘃𝗲𝗹 𝗯𝘂𝘀𝗰𝗮𝗿 𝘂𝗺𝗮 𝗳𝗼𝘁𝗼 𝗱𝗲 𝗴𝗮𝘁𝗶𝗻𝗵𝗼 🙀")