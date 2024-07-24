import logging

from pyrogram import filters
from pyrogram.types import Message

from CineWinx import app
from CineWinx.misc import SUDOERS
from CineWinx.utils.database.memory_db import (
    get_active_chats,
    get_active_video_chats,
)
from config import PREFIXES
from strings import get_command

ACTIVEVC_COMMAND = get_command("ACTIVEVC_COMMAND")
ACTIVEVIDEO_COMMAND = get_command("ACTIVEVIDEO_COMMAND")
ACINFO_COMMAND = get_command("ACINFO_COMMAND")


@app.on_message(filters.command(ACTIVEVC_COMMAND, PREFIXES) & SUDOERS)
async def activevc(_, message: Message):
    mystic = await message.reply_text(
        "🎙️ 𝗢𝗯𝘁𝗲𝗻𝗱𝗼 𝗼 𝗰𝗵𝗮𝘁 𝗱𝗲 𝘃𝗼𝘇 𝗮𝘁𝗶𝘃𝗼... 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗮𝗴𝘂𝗮𝗿𝗱𝗲"
    )
    served_chats = await get_active_chats()
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
        except Exception as e:
            logging.error(e)
            title = "Grupo privado"
        if (await app.get_chat(x)).username:
            user = (await app.get_chat(x)).username
            text += f"<b>{j + 1}.</b>  <a href='https://t.me/{user}'>{title}</a>[{x}]\n"
        else:
            text += f"<b>{j + 1}. {title}</b> [{x}]\n"
        j += 1
    if not text:
        await mystic.edit_text("❌ 𝗡𝗲𝗻𝗵𝘂𝗺 𝗰𝗵𝗮𝘁 𝗱𝗲 𝘃𝗼𝘇 𝗮𝘁𝗶𝘃𝗼")
    else:
        await mystic.edit_text(
            f"🎙️ <b>𝗖𝗵𝗮𝘁𝘀 𝗱𝗲 𝗩𝗼𝘇 𝗔𝘁𝗶𝘃𝗼𝘀:</b>\n\n{text}",
            disable_web_page_preview=True,
        )


@app.on_message(filters.command(ACTIVEVIDEO_COMMAND, PREFIXES) & SUDOERS)
async def activevi_(_, message: Message):
    mystic = await message.reply_text(
        "🎙️ 𝗢𝗯𝘁𝗲𝗻𝗱𝗼 𝗰𝗵𝗮𝘁𝘀 𝗱𝗲 𝘃𝗼𝘇 𝗮𝘁𝗶𝘃𝗼𝘀... 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗮𝗴𝘂𝗮𝗿𝗱𝗲"
    )
    served_chats = await get_active_video_chats()
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
        except Exception as e:
            logging.error(e)
            title = "Grupo privado"
        if (await app.get_chat(x)).username:
            user = (await app.get_chat(x)).username
            text += f"<b>{j + 1}.</b>  <a href='https://t.me/{user}'>{title}</a>[{x}]\n"
        else:
            text += f"<b>{j + 1}. {title}</b> [{x}]\n"
        j += 1
    if not text:
        await mystic.edit_text("❌ 𝗡𝗲𝗻𝗵𝘂𝗺 𝗰𝗵𝗮𝘁 𝗱𝗲 𝘃𝗼𝘇 𝗮𝘁𝗶𝘃𝗼")
    else:
        await mystic.edit_text(
            f"🎙️ <b>𝗖𝗵𝗮𝘁𝘀 𝗱𝗲 𝗩𝗼𝘇 𝗔𝘁𝗶𝘃𝗼𝘀:</b>\n\n{text}",
            disable_web_page_preview=True,
        )


@app.on_message(filters.command(ACINFO_COMMAND, PREFIXES) & SUDOERS)
async def vc(client: app, message: Message):
    ac_audio = str(len(await get_active_chats()))
    ac_video = str(len(await get_active_video_chats()))
    await message.reply_text(
        f"ℹ️ <b><u>𝗜𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗲 𝗖𝗵𝗮𝘁𝘀 𝗔𝘁𝗶𝘃𝗼𝘀</u></b>:\n\n🎙️ 𝗩𝗼𝘇: {ac_audio}\n📹 𝗩𝗶́𝗱𝗲𝗼: {ac_video}"
    )


__MODULE__ = "Ativos"
__HELP__ = """<b>𝗖𝗼𝗺𝗮𝗻𝗱𝗼𝘀 𝗱𝗲 𝗖𝗵𝗮𝘁𝘀 𝗔𝘁𝗶𝘃𝗼𝘀:</b>

ℹ️ <code>/ac</code> - 𝗩𝗲𝗿𝗶𝗳𝗶𝗰𝗮𝗿 𝗼𝘀 𝗰𝗵𝗮𝘁𝘀 𝗱𝗲 𝘃𝗼𝘇 𝗮𝘁𝗶𝘃𝗼𝘀 𝗻𝗼 𝗯𝗼𝘁.
🎙️ <code>/activevoice</code> - 𝗩𝗲𝗿𝗶𝗳𝗶𝗰𝗮𝗿 𝗼𝘀 𝗰𝗵𝗮𝘁𝘀 𝗱𝗲 𝘃𝗼𝘇 𝗲 𝗰𝗵𝗮𝗺𝗮𝗱𝗮𝘀 𝗱𝗲 𝘃𝗶́𝗱𝗲𝗼 𝗮𝘁𝗶𝘃𝗼𝘀 𝗻𝗼 𝗯𝗼𝘁.
📹 <code>/activevideo</code> - 𝗩𝗲𝗿𝗶𝗳𝗶𝗰𝗮𝗿 𝗮𝘀 𝗰𝗵𝗮𝗺𝗮𝗱𝗮𝘀 𝗱𝗲 𝘃𝗶́𝗱𝗲𝗼 𝗮𝘁𝗶𝘃𝗮𝘀 𝗻𝗼 𝗯𝗼𝘁.
📊 <code>/stats</code> - 𝗩𝗲𝗿𝗶𝗳𝗶𝗰𝗮𝗿 𝗮𝘀 𝗲𝘀𝘁𝗮𝘁𝗶́𝘀𝘁𝗶𝗰𝗮𝘀 𝗱𝗼 𝗯𝗼𝘁.
"""
