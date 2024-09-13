from datetime import datetime

from pyrogram import filters, Client
from pyrogram.types import Message

from CineWinx import app
from CineWinx.core.call import CineWinx
from CineWinx.utils import bot_sys_stats
from CineWinx.utils.decorators.language import language
from CineWinx.utils.inline import support_group_markup
from config import BANNED_USERS, PREFIXES
from strings import get_command

PING_COMMAND = get_command("PING_COMMAND")


@app.on_message(filters.command(PING_COMMAND, PREFIXES) & ~BANNED_USERS & filters.group)
@language
async def ping_com(client: Client, message: Message, _):
    me = await client.get_me()
    pic = await client.download_media(me.photo.big_file_id) if me.photo else None
    if pic:
        response = await message.reply_photo(
            photo=pic,
            caption=_["ping_1"].format(app.mention),
        )
    else:
        response = await message.reply_text(
            _["ping_1"].format(app.mention),
        )
    start = datetime.now()
    pytg_ping = await CineWinx.ping()
    up, cpu, ram, disk = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_text(
        _["ping_2"].format(
            resp,
            app.mention,
            up,
            ram,
            cpu,
            disk,
            pytg_ping,
        ),
        reply_markup=support_group_markup(_),
    )
