from pyrogram import Client, filters
from pyrogram.types import Message

from Bot import app
from Bot.utils.decorators.play import play_wrapper
from strings import get_command

PLAY_COMMAND = get_command("PLAY_COMMAND")


@app.on_message(
    filters.command(PLAY_COMMAND, prefixes=["/", "!", "%", ",", "", ".", "@", "#"])
)
@play_wrapper
async def play(client: Client, message: Message):
    await message.reply("Play Command")
