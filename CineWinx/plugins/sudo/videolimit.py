from pyrogram import filters
from pyrogram.types import Message

from CineWinx import app
from CineWinx.misc import SUDOERS
from CineWinx.utils.database import set_video_limit
from CineWinx.utils.decorators.language import language
from config import PREFIXES
from strings import get_command

VIDEOLIMIT_COMMAND = get_command("VIDEOLIMIT_COMMAND")


@app.on_message(filters.command(VIDEOLIMIT_COMMAND, PREFIXES) & SUDOERS)
@language
async def set_video_limit_kid(_client: app, message: Message, _):
    if len(message.command) != 2:
        usage = _["vid_1"]
        return await message.reply_text(usage)
    message.chat.id
    state = message.text.split(None, 1)[1].strip()
    if state.lower() == "disable":
        limit = 0
        await set_video_limit(limit)
        return await message.reply_text(_["vid_4"])
    if state.isnumeric():
        limit = int(state)
        await set_video_limit(limit)
        if limit == 0:
            return await message.reply_text(_["vid_4"])
        await message.reply_text(_["vid_3"].format(limit))
    else:
        return await message.reply_text(_["vid_2"])
