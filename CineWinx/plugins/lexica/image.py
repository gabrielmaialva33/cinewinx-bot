from pyrogram import filters, Client
from pyrogram.types import (
    Message,
)

from CineWinx import app
from CineWinx.utils import LexicaClient
from config import PREFIXES, BANNED_USERS
from strings import get_command

DRAW_COMMAND = get_command("DRAW_COMMAND")

client = LexicaClient()


@app.on_message(filters.command(DRAW_COMMAND, PREFIXES) & ~BANNED_USERS)
async def draw(_client: Client, message: Message):
    pass
