import logging

from pyrogram import filters
from pyrogram.types import Message

import config
from CineWinx import app
from CineWinx.misc import SUDOERS
from CineWinx.utils.database import (
    add_private_chat,
    get_private_served_chats,
    is_served_private_chat,
    remove_private_chat,
)
from CineWinx.utils.decorators.language import language
from config import PREFIXES
from strings import get_command

AUTHORIZE_COMMAND = get_command("AUTHORIZE_COMMAND")
UNAUTHORIZE_COMMAND = get_command("UNAUTHORIZE_COMMAND")
AUTHORIZED_COMMAND = get_command("AUTHORIZED_COMMAND")


@app.on_message(filters.command(AUTHORIZE_COMMAND, PREFIXES) & SUDOERS)
@language
async def authorize(_client: app, message: Message, _):
    if config.PRIVATE_BOT_MODE != str(True):
        return await message.reply_text(_["pbot_12"])
    if len(message.command) != 2:
        return await message.reply_text(_["pbot_1"])
    try:
        chat_id = int(message.text.strip().split()[1])
    except ValueError:
        return await message.reply_text(_["pbot_7"])
    if not await is_served_private_chat(chat_id):
        await add_private_chat(chat_id)
        await message.reply_text(_["pbot_3"])
    else:
        await message.reply_text(_["pbot_5"])


@app.on_message(filters.command(UNAUTHORIZE_COMMAND, PREFIXES) & SUDOERS)
@language
async def unauthorize(_client: app, message: Message, _):
    if config.PRIVATE_BOT_MODE != str(True):
        return await message.reply_text(_["pbot_12"])
    if len(message.command) != 2:
        return await message.reply_text(_["pbot_2"])
    try:
        chat_id = int(message.text.strip().split()[1])
    except ValueError:
        return await message.reply_text(_["pbot_7"])
    if not await is_served_private_chat(chat_id):
        return await message.reply_text(_["pbot_6"])
    else:
        await remove_private_chat(chat_id)
        return await message.reply_text(_["pbot_4"])


@app.on_message(filters.command(AUTHORIZED_COMMAND, PREFIXES) & SUDOERS)
@language
async def authorized(_client: app, message: Message, _):
    if config.PRIVATE_BOT_MODE != str(True):
        return await message.reply_text(_["pbot_12"])
    m = await message.reply_text(_["pbot_8"])
    served_chats = []
    text = _["pbot_9"]
    chats = await get_private_served_chats()
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))
    count = 0
    co = 0
    msg = _["pbot_13"]
    for served_chat in served_chats:
        try:
            title = (await app.get_chat(served_chat)).title
            count += 1
            text += f"{count}:- {title[:15]} [{served_chat}]\n"
        except Exception as e:
            logging.error(str(e))
            title = _["pbot_10"]
            co += 1
            msg += f"{co}:- {title} [{served_chat}]\n"
    if co == 0:
        if count == 0:
            return await m.edit(_["pbot_11"])
        else:
            return await m.edit(text)
    else:
        if count == 0:
            await m.edit(msg)
        else:
            text = f"{text} {msg}"
            return await m.edit(text)


__MODULE__ = "P-bot"
__HELP__ = """
⚡️<u>𝗙𝘂𝗻𝗰̧𝗮̃𝗼 𝗱𝗼 𝗯𝗼𝘁 𝗽𝗿𝗶𝘃𝗮𝗱𝗼:</u>
      
<code>/authorize [chat_id]</code> - 𝗣𝗲𝗿𝗺𝗶𝘁𝗶𝗿 𝘂𝗺 𝗰𝗵𝗮𝘁 𝘂𝘀𝗮𝗿 𝘀𝗲𝘂 𝗯𝗼𝘁.
<code>/unauthorize [chat_id]</code> - 𝗗𝗲𝘀𝗮𝘂𝘁𝗼𝗿𝗶𝘇𝗮𝗿 𝘂𝗺 𝗰𝗵𝗮𝘁 𝗱𝗲 𝘂𝘀𝗮𝗿 𝘀𝗲𝘂 𝗯𝗼𝘁.
<code>/authorized</code> - 𝗩𝗲𝗿𝗶𝗳𝗶𝗰𝗮𝗿 𝘁𝗼𝗱𝗼𝘀 𝗼𝘀 𝗰𝗵𝗮𝘁𝘀 𝗽𝗲𝗿𝗺𝗶𝘁𝗶𝗱𝗼𝘀 𝗱𝗼 𝘀𝗲𝘂 𝗯𝗼𝘁.
"""
