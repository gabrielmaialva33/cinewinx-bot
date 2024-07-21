from pyrogram import filters
from pyrogram.types import Message

from CineWinx import app
from CineWinx.misc import db
from CineWinx.utils.decorators import admin_rights_check
from config import BANNED_USERS, PREFIXES
from strings import get_command

PLAYER_COMMAND = get_command("PLAYER_COMMAND")


@app.on_message(filters.command(PLAYER_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS)
@admin_rights_check
async def pause_admin(_client: app, message: Message, _, chat_id):
    check = db.get(chat_id)
    reply_markup, thumbs, caption = (
        next(
            (
                item["mystic"].reply_markup
                for item in check
                if isinstance(item, dict)
                   and "mystic" in item
                   and hasattr(item["mystic"], "reply_markup")
            ),
            None,
        ),
        (
            next(
                (
                    item["mystic"].photo.thumbs
                    for item in check
                    if isinstance(item, dict)
                       and "mystic" in item
                       and hasattr(item["mystic"].photo, "thumbs")
                ),
                None,
            )
        )[0].file_id,
        next(
            (
                item["mystic"].caption
                for item in check
                if isinstance(item, dict)
                   and "mystic" in item
                   and hasattr(item["mystic"], "caption")
            ),
            None,
        ),
    )

    await message.reply_photo(photo=thumbs, caption=caption, reply_markup=reply_markup)
