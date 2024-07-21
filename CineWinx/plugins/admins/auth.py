import logging

from pyrogram import filters, Client
from pyrogram.types import Message

from CineWinx import app
from CineWinx.utils.database import (
    delete_authuser,
    get_authuser,
    get_authuser_names,
    save_authuser,
)
from CineWinx.utils.decorators import admin_actual, language
from CineWinx.utils.formatters import int_to_alpha
from config import BANNED_USERS, adminlist, PREFIXES
from strings import get_command

# Command
AUTH_COMMAND = get_command("AUTH_COMMAND")
UNAUTH_COMMAND = get_command("UNAUTH_COMMAND")
AUTHUSERS_COMMAND = get_command("AUTHUSERS_COMMAND")


@app.on_message(filters.command(AUTH_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS)
@admin_actual
async def auth(_client: Client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        user_id = message.from_user.id
        token = await int_to_alpha(user.id)
        from_user_name = message.from_user.first_name
        from_user_id = message.from_user.id
        _check = await get_authuser_names(message.chat.id)
        count = len(_check)
        if int(count) == 20:
            return await message.reply_text(_["auth_1"])
        if token not in _check:
            assis = {
                "auth_user_id": user.id,
                "auth_name": user.first_name,
                "admin_id": from_user_id,
                "admin_name": from_user_name,
            }
            get = adminlist.get(message.chat.id)
            if get:
                if user.id not in get:
                    get.append(user.id)
            await save_authuser(message.chat.id, token, assis)
            return await message.reply_text(_["auth_2"])
        else:
            await message.reply_text(_["auth_3"])
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    user_name = message.reply_to_message.from_user.first_name
    token = await int_to_alpha(user_id)
    from_user_name = message.from_user.first_name
    _check = await get_authuser_names(message.chat.id)
    count = 0
    for smex in _check:
        count += 1
    if int(count) == 20:
        return await message.reply_text(_["auth_1"])
    if token not in _check:
        assis = {
            "auth_user_id": user_id,
            "auth_name": user_name,
            "admin_id": from_user_id,
            "admin_name": from_user_name,
        }
        get = adminlist.get(message.chat.id)
        if get:
            if user_id not in get:
                get.append(user_id)
        await save_authuser(message.chat.id, token, assis)
        return await message.reply_text(_["auth_2"])
    else:
        await message.reply_text(_["auth_3"])


@app.on_message(
    filters.command(UNAUTH_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS
)
@admin_actual
async def unauthusers(_client: Client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        token = await int_to_alpha(user.id)
        deleted = await delete_authuser(message.chat.id, token)
        get = adminlist.get(message.chat.id)
        if get:
            if user.id in get:
                get.remove(user.id)
        if deleted:
            return await message.reply_text(_["auth_4"])
        else:
            return await message.reply_text(_["auth_5"])
    user_id = message.reply_to_message.from_user.id
    token = await int_to_alpha(user_id)
    deleted = await delete_authuser(message.chat.id, token)
    get = adminlist.get(message.chat.id)
    if get:
        if user_id in get:
            get.remove(user_id)
    if deleted:
        return await message.reply_text(_["auth_4"])
    else:
        return await message.reply_text(_["auth_5"])


@app.on_message(
    filters.command(AUTHUSERS_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS
)
@language
async def authusers(_client: Client, message: Message, _):
    _playlist = await get_authuser_names(message.chat.id)
    if not _playlist:
        return await message.reply_text(_["setting_5"])
    else:
        j = 0
        mystic = await message.reply_text(_["auth_6"])
        text = _["auth_7"]
        for note in _playlist:
            _note = await get_authuser(message.chat.id, note)
            user_id = _note["auth_user_id"]
            admin_id = _note["admin_id"]
            admin_name = _note["admin_name"]
            try:
                user = await app.get_users(user_id)
                user = user.first_name
                j += 1
            except Exception as e:
                logging.warning(e)
                continue
            text += f"<b>{j}</b> {user}[{user_id}]\n"
            text += f"{_['auth_8']} {admin_name}[{admin_id}]\n\n"
        await mystic.delete()
        await message.reply_text(text)


__MODULE__ = "Autorização"
__HELP__ = """<b><u>🔒 𝗨𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗔𝘂𝘁𝗼𝗿𝗶𝘇𝗮𝗱𝗼𝘀 </u></b>\n
👥 𝗨𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗮𝘂𝘁𝗼𝗿𝗶𝘇𝗮𝗱𝗼𝘀 𝗽𝗼𝗱𝗲𝗺 𝘂𝘀𝗮𝗿 𝗰𝗼𝗺𝗮𝗻𝗱𝗼𝘀 𝗱𝗲 𝗮𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿 𝘀𝗲𝗺 𝗱𝗶𝗿𝗲𝗶𝘁𝗼𝘀 𝗱𝗲 𝗮𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿 𝗻𝗼 𝘀𝗲𝘂 𝗰𝗵𝗮𝘁.

➕ <code>/auth [𝗻𝗼𝗺𝗲 𝗱𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼]</code> - 𝗮𝗱𝗶𝗰𝗶𝗼𝗻𝗮 𝘂𝗺 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 à 𝗟𝗜𝗦𝗧𝗔 𝗗𝗘 𝗔𝗨𝗧𝗢𝗥𝗜𝗭𝗔𝗗𝗢𝗦 𝗱𝗼 𝗴𝗿𝘂𝗽𝗼.
➖ <code>/unauth [𝗻𝗼𝗺𝗲 𝗱𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼]</code> - 𝗿𝗲𝗺𝗼𝘃𝗲 𝘂𝗺 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗱𝗮 𝗟𝗜𝗦𝗧𝗔 𝗗𝗘 𝗔𝗨𝗧𝗢𝗥𝗜𝗭𝗔𝗗𝗢𝗦 𝗱𝗼 𝗴𝗿𝘂𝗽𝗼.
📋 <code>/authusers</code> - 𝘃𝗲𝗿𝗶𝗳𝗶𝗰𝗮 𝗮 𝗟𝗜𝗦𝗧𝗔 𝗗𝗘 𝗔𝗨𝗧𝗢𝗥𝗜𝗭𝗔𝗗𝗢𝗦 𝗱𝗼 𝗴𝗿𝘂𝗽𝗼.
"""
