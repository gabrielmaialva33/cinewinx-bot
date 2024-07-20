from pyrogram import filters, Client
from pyrogram.types import Message

from CineWinx import app
from CineWinx.core.call import CineWinx
from CineWinx.utils.database import is_music_playing, music_on
from CineWinx.utils.decorators import admin_rights_check
from config import BANNED_USERS, PREFIXES
from strings import get_command

# Commands
RESUME_COMMAND = get_command("RESUME_COMMAND")


@app.on_message(
    filters.command(RESUME_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS
)
@admin_rights_check
async def resume_com(_client: Client, message: Message, _, chat_id: int):
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    if await is_music_playing(chat_id):
        return await message.reply_text(_["admin_3"])
    await music_on(chat_id)
    await CineWinx.resume_stream(chat_id)
    await message.reply_text(_["admin_4"].format(message.from_user.mention))
