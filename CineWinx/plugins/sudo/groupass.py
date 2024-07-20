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
from config import LOG_GROUP_ID, BANNED_USERS


@app.on_message(filters.command("changeassistant") & ~BANNED_USERS)
@admin_actual
async def assis_change(_client: app, message: Message, _):
    if await assistant():
        return await message.reply_text(
            "Desculpe! No servidor do bot, há apenas um assistente disponível. Portanto, você não pode alterar o "
            "assistente."
        )
    usage = (
        f"<b>Uso incorreto do comando detectado</b>\n<b>Uso:</b>\n/changeassistant - Para alterar o assistente atual do "
        f"seu grupo para um assistente aleatório no servidor do bot"
    )
    if len(message.command) > 2:
        return await message.reply_text(usage)
    a = await get_assistant(message.chat.id)
    details = f"O assistente do seu chat foi alterado de [{a.name}](https://t.me/{a.username}) "
    if not message.chat.id == LOG_GROUP_ID:
        try:
            await a.leave_chat(message.chat.id)
        except:
            pass
    b = await set_assistant(message.chat.id)
    details += f"para [{b.name}](https://t.me/{b.username})"
    try:
        await b.join_chat(message.chat.id)
    except:
        pass
    await message.reply_text(details, disable_web_page_preview=True)


@app.on_message(filters.command("setassistant") & ~BANNED_USERS)
@admin_actual
async def assis_set(_client: app, message: Message, _):
    if await assistant():
        return await message.reply_text(
            "Desculpe! No servidor do bot, há apenas um assistente disponível. Portanto, você não pode alterar o "
            "assistente."
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
    except:
        pass
    await save_assistant(message.chat.id, query)
    b = await get_assistant(message.chat.id)
    try:
        await b.join_chat(message.chat.id)
    except:
        pass
    await message.reply_text(
        f"<b>Detalhes do novo assistente do seu chat:<b>\nNome do Assistente: {b.name}\nNome de Usuário: @{b.username}\nID: {b.id}",
        disable_web_page_preview=True,
    )


@app.on_message(filters.command("checkassistant") & filters.group & ~BANNED_USERS)
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
