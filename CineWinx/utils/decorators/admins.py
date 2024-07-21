import logging

from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from CineWinx import app
from CineWinx.misc import SUDOERS
from CineWinx.utils.database import (
    get_authuser_names,
    get_cmode,
    get_lang,
    is_active_chat,
    is_commanddelete_on,
    is_maintenance,
    is_nonadmin_chat,
)
from config import adminlist
from strings import get_string
from ..formatters import int_to_alpha


def admin_rights_check(mystic: callable):
    async def wrapper(client, message):
        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    "🔧 𝗢 𝗯𝗼𝘁 𝗲𝘀𝘁á 𝗲𝗺 𝗺𝗮𝗻𝘂𝘁𝗲𝗻çã𝗼. 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗮𝗴𝘂𝗮𝗿𝗱𝗲 𝘂𝗺 𝗺𝗼𝗺𝗲𝗻𝘁𝗼..."
                )
        if await is_commanddelete_on(message.chat.id):
            try:
                await message.delete()
            except Exception as e:
                logging.exception(e)
                pass
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
        except Exception as e:
            logging.exception(e)
            _ = get_string("pt")
        if message.sender_chat:
            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="❓ 𝗖𝗼𝗺𝗼 𝗮𝗿𝗿𝘂𝗺𝗮𝗿 𝗶𝘀𝘀𝗼?",
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
            except:
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
        return await mystic(client, message, _, chat_id)

    return wrapper


def admin_actual(mystic: callable):
    async def wrapper(client, message):
        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    "🔧 𝗢 𝗯𝗼𝘁 𝗲𝘀𝘁á 𝗲𝗺 𝗺𝗮𝗻𝘂𝘁𝗲𝗻çã𝗼. 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗮𝗴𝘂𝗮𝗿𝗱𝗲 𝘂𝗺 𝗺𝗼𝗺𝗲𝗻𝘁𝗼..."
                )
        if await is_commanddelete_on(message.chat.id):
            try:
                await message.delete()
            except Exception as e:
                logging.exception(e)
                pass
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
        except Exception as e:
            logging.exception(e)
            _ = get_string("pt")
        if message.sender_chat:
            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="❓ 𝗖𝗼𝗺𝗼 𝗮𝗿𝗿𝘂𝗺𝗮𝗿 𝗶𝘀𝘀𝗼?",
                            callback_data="AnonymousAdmin",
                        ),
                    ]
                ]
            )
            return await message.reply_text(_["general_4"], reply_markup=upl)
        if message.from_user.id not in SUDOERS:
            try:
                member = await app.get_chat_member(
                    message.chat.id, message.from_user.id
                )
                if member.status != ChatMemberStatus.ADMINISTRATOR:
                    if not member.privileges.can_manage_video_chats:
                        return await message.reply(_["general_5"])
            except Exception as e:
                return await message.reply(f"Error: {str(e)}")
        return await mystic(client, message, _)

    return wrapper


def actual_admin_cb(mystic: callable):
    async def wrapper(client: app, callback_query: CallbackQuery):
        if await is_maintenance() is False:
            if callback_query.from_user.id not in SUDOERS:
                return await callback_query.answer(
                    "🔧 𝗢 𝗯𝗼𝘁 𝗲𝘀𝘁á 𝗲𝗺 𝗺𝗮𝗻𝘂𝘁𝗲𝗻çã𝗼. 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗮𝗴𝘂𝗮𝗿𝗱𝗲 𝘂𝗺 𝗺𝗼𝗺𝗲𝗻𝘁𝗼...",
                    show_alert=True,
                )
        try:
            language = await get_lang(callback_query.message.chat.id)
            _ = get_string(language)
        except Exception as e:
            logging.exception(e)
            _ = get_string("pt")
        if callback_query.message.chat.type == ChatType.PRIVATE:
            return await mystic(client, callback_query, _)
        is_non_admin = await is_nonadmin_chat(callback_query.message.chat.id)
        if not is_non_admin:
            try:
                a = await app.get_chat_member(
                    callback_query.message.chat.id,
                    callback_query.from_user.id,
                )
                if a.status != ChatMemberStatus.ADMINISTRATOR:
                    if not a.privileges.can_manage_video_chats:
                        if callback_query.from_user.id not in SUDOERS:
                            token = await int_to_alpha(callback_query.from_user.id)
                            _check = await get_authuser_names(
                                callback_query.from_user.id
                            )
                            if token not in _check:
                                return await callback_query.answer(
                                    _["general_5"],
                                    show_alert=True,
                                )
                    elif a is None:
                        return await callback_query.answer(
                            "🚫 𝗩𝗼𝗰ê 𝗻ã𝗼 é 𝘂𝗺 𝗺𝗲𝗺𝗯𝗿𝗼 𝗱𝗲𝘀𝘁𝗲 𝗰𝗵𝗮𝘁."
                        )
            except Exception as e:
                return await callback_query.answer(f"Error: {str(e)}")
        return await mystic(client, callback_query, _)

    return wrapper
