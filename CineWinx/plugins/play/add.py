from pyrogram import filters, Client
from pyrogram.raw.types import Message

from CineWinx import app
from config import PREFIXES, BANNED_USERS
from strings import get_command

ADD_COMMAND = get_command("ADD_COMMAND")


@app.on_message(filters.command(ADD_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS)
async def add_command(client: Client, message: Message):
    pass
