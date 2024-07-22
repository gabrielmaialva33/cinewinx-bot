from pyrogram import filters

from CineWinx import app
from config import PREFIXES, BANNED_USERS


@app.on_message(filters.command("list", PREFIXES) & ~BANNED_USERS)
async def list_command(_client, message):
    await message.reply_text("List Command")
