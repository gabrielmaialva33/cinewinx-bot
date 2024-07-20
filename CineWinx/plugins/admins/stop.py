import logging

from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.types import Message

from CineWinx import app
from CineWinx.core.call import CineWinx
from CineWinx.misc import SUDOERS
from CineWinx.plugins import extra_plugins_enabled
from CineWinx.utils.database import (
    set_loop,
    delete_filter,
    is_maintenance,
    is_commanddelete_on,
    get_lang,
    is_nonadmin_chat,
    is_active_chat,
    get_cmode,
)
from config import BANNED_USERS, PREFIXES, adminlist
from strings import get_string, get_command

STOP_COMMAND = get_command("STOP_COMMAND")


@app.on_message(filters.command(STOP_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS)
async def stop_music(_client: Client, message: Message):
    if await is_maintenance() is False:
        if message.from_user.id not in SUDOERS:
            return await message.reply_text(
                "O bot está em manutenção. Por favor, aguarde um momento..."
            )
    if not len(message.command) < 2:
        if extra_plugins_enabled:
            if not message.command[0][0] == "c" and not message.command[0][0] == "e":
                filter = " ".join(message.command[1:])
                deleted = await delete_filter(message.chat.id, filter)
                if deleted:
                    return await message.reply_text(f"<b>Filtro {filter} deletado.</b>")
                else:
                    return await message.reply_text("<b>Nenhum filtro encontrado.</b>")

    if await is_commanddelete_on(message.chat.id):
        try:
            await message.delete()
        except Exception as e:
            logging.error(e)
    try:
        language = await get_lang(message.chat.id)
        _ = get_string(language)
    except Exception as e:
        logging.error(e)
        _ = get_string("pt")

    if message.sender_chat:
        upl = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Como arrumar isso? ",
                        callback_data="AnonymousAdmin",
                    ),
                ]
            ]
        )
        return await message.reply_text(_["general_4"], reply_markup=upl)

    if message.command[0][0] == "c":
        chat_id = await get_cmode(message.chat.id)
        if chat_id is None:
            return await message.reply_text(_["setting_12"])
        try:
            await app.get_chat(chat_id)
        except Exception as e:
            logging.error(e)
            return await message.reply_text(_["cplay_4"])
    else:
        chat_id = message.chat.id
    if not await is_active_chat(chat_id):
        return await message.reply_text(_["general_6"])
    is_non_admin = await is_nonadmin_chat(message.chat.id)
    if not is_non_admin:
        if message.from_user.id not in SUDOERS:
            admins = adminlist.get(message.chat.id)
            if not admins:
                return await message.reply_text(_["admin_18"])
            else:
                if message.from_user.id not in admins:
                    return await message.reply_text(_["admin_19"])
    await CineWinx.stop_stream(chat_id)
    await set_loop(chat_id, 0)
    await message.reply_text(_["admin_9"].format(message.from_user.mention))
