import random

from pyrogram import filters, Client
from pyrogram.types import Message

from CineWinx import app
from CineWinx.misc import db
from CineWinx.utils.decorators import admin_rights_check
from config import BANNED_USERS, PREFIXES
from strings import get_command

# Commands
SHUFFLE_COMMAND = get_command("SHUFFLE_COMMAND")


@app.on_message(
    filters.command(SHUFFLE_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS
)
@admin_rights_check
async def admins(_client: Client, message: Message, _, chat_id: int):
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    check = db.get(chat_id)
    if not check:
        return await message.reply_text(_["admin_21"])
    try:
        popped = check.pop(0)
    except IndexError:
        return await message.reply_text(_["admin_22"])
    check = db.get(chat_id)
    if not check:
        check.insert(0, popped)
        return await message.reply_text(_["admin_22"])
    random.shuffle(check)
    check.insert(0, popped)
    await message.reply_text(_["admin_23"].format(message.from_user.first_name))
