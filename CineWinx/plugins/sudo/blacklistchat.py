import logging

from pyrogram import filters
from pyrogram.types import Message

from CineWinx import app
from CineWinx.misc import SUDOERS
from CineWinx.utils.database import blacklist_chat, blacklisted_chats, whitelist_chat
from CineWinx.utils.decorators.language import language
from config import BANNED_USERS, PREFIXES
from strings import get_command

BLACKLISTCHAT_COMMAND = get_command("BLACKLISTCHAT_COMMAND")
WHITELISTCHAT_COMMAND = get_command("WHITELISTCHAT_COMMAND")
BLACKLISTEDCHAT_COMMAND = get_command("BLACKLISTEDCHAT_COMMAND")


@app.on_message(filters.command(BLACKLISTCHAT_COMMAND, PREFIXES) & SUDOERS)
@language
async def blacklist_chat_func(_client: app, message: Message, _):
    if len(message.command) != 2:
        return await message.reply_text(_["black_1"])
    chat_id = int(message.text.strip().split()[1])
    if chat_id in await blacklisted_chats():
        return await message.reply_text(_["black_2"])
    blacklisted = await blacklist_chat(chat_id)
    if blacklisted:
        await message.reply_text(_["black_3"])
    else:
        await message.reply_text("❗ 𝗔𝗹𝗴𝗼 𝗱𝗲𝘂 𝗲𝗿𝗿𝗮𝗱𝗼.")
    try:
        await app.leave_chat(chat_id)
    except Exception as e:
        logging.error(e)


@app.on_message(filters.command(WHITELISTCHAT_COMMAND, PREFIXES) & SUDOERS)
@language
async def white_funciton(_client: app, message: Message, _):
    if len(message.command) != 2:
        return await message.reply_text(_["black_4"])
    chat_id = int(message.text.strip().split()[1])
    if chat_id not in await blacklisted_chats():
        return await message.reply_text(_["black_5"])
    whitelisted = await whitelist_chat(chat_id)
    if whitelisted:
        return await message.reply_text(_["black_6"])
    await message.reply_text("Algo deu errado.")


@app.on_message(filters.command(BLACKLISTEDCHAT_COMMAND, PREFIXES) & ~BANNED_USERS)
@language
async def all_chats(_client: app, message: Message, _):
    text = _["black_7"]
    j = 0
    for count, chat_id in enumerate(await blacklisted_chats(), 1):
        try:
            title = (await app.get_chat(chat_id)).title
        except Exception as e:
            logging.error(e)
            title = "Privado"
        j = 1
        text += f"<b>{count}. {title}</b> [`{chat_id}`]\n"
    if j == 0:
        await message.reply_text(_["black_8"])
    else:
        await message.reply_text(text)
