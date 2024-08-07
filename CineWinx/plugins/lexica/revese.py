from pyrogram import filters, Client
from pyrogram.types import Message

from CineWinx import app
from config import PREFIXES, BANNED_USERS
from strings import get_command

REVERSE_COMMAND = get_command("REVERSE_COMMAND")

context_db: dict = {}


@app.on_message(filters.command(REVERSE_COMMAND, PREFIXES) & ~BANNED_USERS)
async def reverse_command(_: Client, message: Message):
    pass
