import logging

from pyrogram import filters
from pyrogram.types import Message

from CineWinx import app
from CineWinx.core.userbot import assistants
from CineWinx.utils.assistant import (
    is_avl_assistant as assistant,
    get_assistant_details,
)
from CineWinx.utils.database import get_assistant, save_assistant, set_assistant
from CineWinx.utils.decorators import admin_actual
from config import LOG_GROUP_ID, BANNED_USERS, PREFIXES
from strings import get_command

CHANGE_ASSISTANT = get_command("CHANGE_ASSISTANT")
SET_ASSISTANT = get_command("SET_ASSISTANT")
CHECK_ASSISTANT = get_command("CHECK_ASSISTANT")


@app.on_message(filters.command(CHANGE_ASSISTANT, PREFIXES) & ~BANNED_USERS)
@admin_actual
async def assis_change(_client: app, message: Message, _):
    if await assistant():
        return await message.reply_text(
            "⚠️ 𝗗𝗲𝘀𝗰𝘂𝗹𝗽𝗲! 𝗡𝗼 𝘀𝗲𝗿𝘃𝗶𝗱𝗼𝗿 𝗱𝗼 𝗯𝗼𝘁, 𝗵𝗮́ 𝗮𝗽𝗲𝗻𝗮𝘀 𝘂𝗺 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 "
            "𝗱𝗶𝘀𝗽𝗼𝗻𝗶́𝘃𝗲𝗹. 𝗣𝗼𝗿𝘁𝗮𝗻𝘁𝗼, 𝘃𝗼𝗰𝗲̂ 𝗻𝗮̃𝗼 𝗽𝗼𝗱𝗲 𝗮𝗹𝘁𝗲𝗿𝗮𝗿 𝗼 "
            "𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲."
        )
    usage = (
        f"⚠️ <b>𝗨𝘀𝗼 𝗶𝗻𝗰𝗼𝗿𝗿𝗲𝘁𝗼 𝗱𝗼 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 𝗱𝗲𝘁𝗲𝗰𝘁𝗮𝗱𝗼</b>\n<b>📋 "
        f"𝗨𝘀𝗼:</b>\n<code>/changeassistant</code> - 𝗣𝗮𝗿𝗮 𝗮𝗹𝘁𝗲𝗿𝗮𝗿 𝗼 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗮𝘁𝘂𝗮𝗹 𝗱𝗼"
        f"𝘀𝗲𝘂 𝗴𝗿𝘂𝗽𝗼 𝗽𝗮𝗿𝗮 𝘂𝗺 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗮𝗹𝗲𝗮𝘁𝗼́𝗿𝗶𝗼 𝗻𝗼 𝘀𝗲𝗿𝘃𝗶𝗱𝗼𝗿 𝗱𝗼 𝗯𝗼𝘁"
    )
    if len(message.command) > 2:
        return await message.reply_text(usage)
    a = await get_assistant(message.chat.id)
    details = f"🔄 𝗢 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗱𝗼 𝘀𝗲𝘂 𝗰𝗵𝗮𝘁 𝗳𝗼𝗶 𝗮𝗹𝘁𝗲𝗿𝗮𝗱𝗼 𝗱𝗲 <a href='https://t.me/{a.username}'>{a.name}</a> "
    if not message.chat.id == LOG_GROUP_ID:
        try:
            await a.leave_chat(message.chat.id)
        except Exception as e:
            logging.error(e)
            pass
    b = await set_assistant(message.chat.id)
    details += f"𝗽𝗮𝗿𝗮 <a href='https://t.me/{b.username}'>{b.name}</a>"
    try:
        await b.join_chat(message.chat.id)
    except Exception as e:
        logging.error(e)
        pass
    await message.reply_text(details, disable_web_page_preview=True)


@app.on_message(filters.command(SET_ASSISTANT, PREFIXES) & ~BANNED_USERS)
@admin_actual
async def assis_set(_client: app, message: Message, _):
    if await assistant():
        return await message.reply_text(
            "⚠️ 𝗗𝗲𝘀𝗰𝘂𝗹𝗽𝗲! 𝗡𝗼 𝘀𝗲𝗿𝘃𝗶𝗱𝗼𝗿 𝗱𝗼 𝗯𝗼𝘁, 𝗵𝗮́ 𝗮𝗽𝗲𝗻𝗮𝘀 𝘂𝗺 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 "
            "𝗱𝗶𝘀𝗽𝗼𝗻𝗶́𝘃𝗲𝗹. 𝗣𝗼𝗿𝘁𝗮𝗻𝘁𝗼, 𝘃𝗼𝗰𝗲̂ 𝗻𝗮̃𝗼 𝗽𝗼𝗱𝗲 𝗮𝗹𝘁𝗲𝗿𝗮𝗿 𝗼 "
            "𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲."
        )
    usage = await get_assistant_details()
    if len(message.command) != 2:
        return await message.reply_text(usage, disable_web_page_preview=True)
    query = message.text.split(None, 1)[1].strip()
    if query not in assistants:
        return await message.reply_text(usage, disable_web_page_preview=True)
    a = await get_assistant(message.chat.id)
    try:
        await a.leave_chat(message.chat.id)
    except Exception as e:
        logging.error(e)
        pass
    await save_assistant(message.chat.id, query)
    b = await get_assistant(message.chat.id)
    try:
        await b.join_chat(message.chat.id)
    except Exception as e:
        logging.error(e)
        pass
    await message.reply_text(
        f"ℹ️ <b>𝗗𝗲𝘁𝗮𝗹𝗵𝗲𝘀 𝗱𝗼 𝗻𝗼𝘃𝗼 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗱𝗼 𝘀𝗲𝘂 𝗰𝗵𝗮𝘁:</b>\n"
        f"👤 𝗔𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲: {b.name}\n"
        f"📧 𝗨𝘀𝘂𝗮́𝗿𝗶𝗼: @{b.username}\n"
        f"🆔 𝗜𝗗: {b.id}",
        disable_web_page_preview=True,
    )


@app.on_message(filters.command(CHANGE_ASSISTANT, PREFIXES) & filters.group & ~BANNED_USERS)
@admin_actual
async def check_ass(_client: app, message: Message, _):
    a = await get_assistant(message.chat.id)
    await message.reply_text(
        f"<b>📋 𝗗𝗲𝘁𝗮𝗹𝗵𝗲𝘀 𝗱𝗼 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗱𝗼 𝘀𝗲𝘂 𝗰𝗵𝗮𝘁:</b>\n"
        f"🤖 𝗔𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲: {a.name}\n"
        f"👤 𝗨𝘀𝘂𝗮́𝗿𝗶𝗼: @{a.username}\n"
        f"🆔 𝗜𝗗 𝗱𝗼 𝗔𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲: {a.id}",
        disable_web_page_preview=True,
    )
