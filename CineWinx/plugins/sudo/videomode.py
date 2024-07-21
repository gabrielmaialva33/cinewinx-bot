from pyrogram import filters
from pyrogram.types import Message

import config
from CineWinx import app
from CineWinx.misc import SUDOERS
from CineWinx.utils.database import add_off, add_on
from CineWinx.utils.decorators.language import language
from config import PREFIXES
from strings import get_command

VIDEOMODE_COMMAND = get_command("VIDEOMODE_COMMAND")


@app.on_message(filters.command(VIDEOMODE_COMMAND, PREFIXES) & SUDOERS)
@language
async def videoloaymode(_client: app, message: Message, _):
    usage = _["vidmode_1"]
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "download":
        await add_on(config.YTDOWNLOADER)
        await message.reply_text(_["vidmode_2"])
    elif state == "m3u8":
        await add_off(config.YTDOWNLOADER)
        await message.reply_text(_["vidmode_3"])
    else:
        await message.reply_text(usage)
