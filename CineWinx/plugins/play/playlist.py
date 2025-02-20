import asyncio
import logging
import os
from random import randint

import requests
from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    CallbackQuery,
)
from youtube_search import YoutubeSearch

from CineWinx import Carbon, app
from CineWinx.utils.database import (
    delete_playlist,
    get_assistant,
    get_playlist,
    get_playlist_names,
    save_playlist,
)
from CineWinx.utils.decorators.language import language, language_cb
from CineWinx.utils.inline.playlist import (
    botplaylist_markup,
    get_cplaylist_markup,
    get_playlist_markup,
    warning_markup,
)
from CineWinx.utils.pastebin import winx_bin
from CineWinx.utils.stream.stream import stream
from config import BANNED_USERS, SERVER_PLAYLIST_LIMIT, PREFIXES
from strings import get_command

PLAYLIST_COMMAND = get_command("PLAYLIST_COMMAND")
DELETEPLAYLIST_COMMAND = get_command("DELETEPLAYLIST_COMMAND")
ADDPLAYLIST_COMMAND = get_command("ADDPLAYLIST_COMMAND")
PLAYLISTS_COMMAND = get_command("PLAYLISTS_COMMAND")


@app.on_message(filters.command(PLAYLIST_COMMAND, PREFIXES) & ~BANNED_USERS)
@language
async def check_playlist(_client: app, message: Message, _):
    _playlist = await get_playlist_names(message.from_user.id)
    if _playlist:
        get = await message.reply_text(_["playlist_2"])
    else:
        return await message.reply_text(_["playlist_3"])
    msg = _["playlist_4"]
    count = 0
    for ptlist in _playlist:
        _note = await get_playlist(message.from_user.id, ptlist)
        title = _note["title"]
        title = title.title()
        duration = _note["duration"]
        count += 1
        msg += f"\n\n{count}- {title[:70]}\n"
        msg += _["playlist_5"].format(duration)
    link = await winx_bin(msg)
    lines = msg.count("\n")
    if lines >= 17:
        car = os.linesep.join(msg.split(os.linesep)[:17])
    else:
        car = msg
    carbon = await Carbon.generate(car, randint(100, 10000000000))
    await get.delete()
    await message.reply_photo(carbon, caption=_["playlist_15"].format(link))


async def get_keyboard(_, user_id: int):
    keyboard = InlineKeyboard(row_width=5)
    _playlist = await get_playlist_names(user_id)
    count = len(_playlist)
    for x in _playlist:
        _note = await get_playlist(user_id, x)
        title = _note["title"]
        title = title.title()
        keyboard.row(
            InlineKeyboardButton(
                text=title,
                callback_data=f"del_playlist {x}",
            )
        )
    keyboard.row(
        InlineKeyboardButton(
            text=_["PL_B_5"],
            callback_data=f"delete_warning",
        ),
        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"close"),
    )
    return keyboard, count


@app.on_message(
    filters.command(DELETEPLAYLIST_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS
)
@language
async def del_group_message(_client: app, message: Message, _):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["PL_B_6"],
                    url=f"https://t.me/{app.username}?start=delplaylists",
                ),
            ]
        ]
    )
    await message.reply_text(_["playlist_6"], reply_markup=upl)


async def get_keyboard(_, user_id: int):
    keyboard = InlineKeyboard(row_width=5)
    _playlist = await get_playlist_names(user_id)
    count = len(_playlist)
    for x in _playlist:
        _note = await get_playlist(user_id, x)
        title = _note["title"]
        title = title.title()
        keyboard.row(
            InlineKeyboardButton(
                text=title,
                callback_data=f"del_playlist {x}",
            )
        )
    keyboard.row(
        InlineKeyboardButton(
            text=_["PL_B_5"],
            callback_data=f"delete_warning",
        ),
        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"close"),
    )
    return keyboard, count


@app.on_message(
    filters.command(DELETEPLAYLIST_COMMAND, PREFIXES) & filters.private & ~BANNED_USERS
)
@language
async def del_plist_msg(_client: app, message: Message, _):
    _playlist = await get_playlist_names(message.from_user.id)
    if _playlist:
        get = await message.reply_text(_["playlist_2"])
    else:
        return await message.reply_text(_["playlist_3"])
    keyboard, count = await get_keyboard(_, message.from_user.id)
    await get.edit_text(_["playlist_7"].format(count), reply_markup=keyboard)


@app.on_callback_query(filters.regex("play_playlist") & ~BANNED_USERS)
@language_cb
async def play_playlist(client: app, callback_query: CallbackQuery, _):
    userbot = await get_assistant(callback_query.message.chat.id)
    try:
        try:
            get = await app.get_chat_member(callback_query.message.chat.id, userbot.id)
        except ChatAdminRequired:
            return await callback_query.answer(
                f"Não tenho permissão para convidar usuários por link para adicionar "
                f"o assistente ao {callback_query.message.chat.title}.",
                show_alert=True,
            )
        if get.status == ChatMemberStatus.BANNED:
            return await callback_query.answer(
                text=f"»Assistente está banido em {callback_query.message.chat.title}",
                show_alert=True,
            )
    except UserNotParticipant:
        if callback_query.message.chat.username:
            invite_link = callback_query.message.chat.username
            try:
                await userbot.resolve_peer(invite_link)
            except Exception as ex:
                logging.exception(ex)
        else:
            try:
                invite_link = await client.export_chat_invite_link(
                    callback_query.message.chat.id
                )
            except ChatAdminRequired:
                return await callback_query.answer(
                    f"Não tenho permissões para convidar usuários por link "
                    f"para adicionar o assistente ao {callback_query.message.chat.title}.",
                    show_alert=True,
                )
            except InviteRequestSent:
                try:
                    await app.approve_chat_join_request(
                        callback_query.message.chat.id, userbot.id
                    )
                except Exception as e:
                    return await callback_query.message.reply_text(
                        f"Falha ao convidar o assistente para {callback_query.message.chat.title}\nMotivo: {e}"
                    )
            except Exception as ex:
                if "channels.JoinChannel" in str(ex) or "Username not found" in str(ex):
                    return await callback_query.answer(
                        f"Não tenho permissão para convidar usuários por link "
                        f"para adicionar o assistente ao {callback_query.message.chat.title}.",
                        show_alert=True,
                    )
                else:
                    return await callback_query.message.reply_text(
                        f"Falha ao convidar o assistente para {callback_query.message.chat.title}.\n\n<b>Motivo:</b> `{ex}`"
                    )
        if invite_link.startswith("https://t.me/+"):
            invite_link = invite_link.replace(
                "https://t.me/+", "https://t.me/joinchat/"
            )
        try:
            await userbot.join_chat(invite_link)
            await asyncio.sleep(2)
        except UserAlreadyParticipant:
            pass
        except InviteRequestSent:
            try:
                await app.approve_chat_join_request(
                    callback_query.message.chat.id, userbot.id
                )
            except Exception as e:
                if "messages.HideChatJoinRequest" in str(e):
                    return await callback_query.answer(
                        f"Não tenho permissão para convidar usuários por link para adicionar o assistente ao {callback_query.message.chat.title}.",
                        show_alert=True,
                    )
                else:
                    return await callback_query.message.reply_text(
                        f"Falha ao convidar o assistente para {callback_query.message.chat.title}.\n\nMotivo: {e}"
                    )
        except Exception as ex:
            if "channels.JoinChannel" in str(ex) or "Username not found" in str(ex):
                return await callback_query.answer(
                    f"Não tenho permissão para convidar usuários por link para adicionar o assistente ao {callback_query.message.chat.title}.",
                    show_alert=True,
                )
            else:
                return await callback_query.message.reply_text(
                    f"Falha ao convidar o assistente para {callback_query.message.chat.title}.\n\nMotivo: {ex}"
                )

        try:
            await userbot.resolve_peer(invite_link)
        except:
            pass

    callback_data = callback_query.data.strip()
    mode = callback_data.split(None, 1)[1]
    user_id = callback_query.from_user.id
    _playlist = await get_playlist_names(user_id)
    if not _playlist:
        try:
            return await callback_query.answer(
                _["playlist_3"],
                show_alert=True,
            )
        except:
            return
    chat_id = callback_query.message.chat.id
    user_name = callback_query.from_user.first_name
    await callback_query.message.delete()
    result = []
    try:
        await callback_query.answer()
    except Exception as e:
        logging.error(str(e))
    video = True if mode == "v" else None
    mystic = await callback_query.message.reply_text(_["play_1"])
    for vidids in _playlist:
        result.append(vidids)
    try:
        await stream(
            _,
            mystic,
            user_id,
            result,
            chat_id,
            user_name,
            callback_query.message.chat.id,
            video,
            stream_type="playlist",
        )
    except Exception as e:
        ex_type = type(e).__name__
        err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
        return await mystic.edit_text(err)
    return await mystic.delete()


@app.on_message(
    filters.command(PLAYLIST_COMMAND, PREFIXES) & ~BANNED_USERS & filters.group
)
@language_cb
async def play_playlist_command(client: app, message: Message, _):
    msg = await message.reply_text("⏳ 𝗔𝗴𝘂𝗮𝗿𝗱𝗲 𝘂𝗺 𝗺𝗼𝗺𝗲𝗻𝘁𝗼...")
    try:
        try:
            userbot = await get_assistant(message.chat.id)
            get = await app.get_chat_member(message.chat.id, userbot.id)
        except ChatAdminRequired:
            return await msg.edit_text(
                f"🚫 𝗡𝗮̃𝗼 𝘁𝗲𝗻𝗵𝗼 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗽𝗮𝗿𝗮 <b>𝗰𝗼𝗻𝘃𝗶𝗱𝗮𝗿 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗽𝗼𝗿 "
                f"𝗹𝗶𝗻𝗸</b> 𝗽𝗮𝗿𝗮 𝗮𝗱𝗶𝗰𝗶𝗼𝗻𝗮𝗿 𝗮 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 {userbot.mention} 𝗮𝗼 "
                f"{message.chat.title}."
            )
        if get.status == ChatMemberStatus.BANNED:
            return await msg.edit_text(
                text=f"🚫 𝗔 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 {userbot.mention} 𝗲𝘀𝘁𝗮́ 𝗯𝗮𝗻𝗶𝗱𝗮 𝗲𝗺 {message.chat.title}\n\n🆔 𝗜𝗗: `{userbot.id}`\n"
                f"👤 𝗡𝗼𝗺𝗲: {userbot.mention}\n📧 𝗡𝗼𝗺𝗲 𝗱𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼: @{userbot.username}\n\n🛑 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, "
                f"𝗿𝗲𝗺𝗼𝘃𝗮 𝗼 𝗯𝗮𝗻𝗶𝗺𝗲𝗻𝘁𝗼 𝗱𝗼 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗲 𝘁𝗲𝗻𝘁𝗲 𝗻𝗼𝘃𝗮𝗺𝗲𝗻𝘁𝗲..."
            )
    except UserNotParticipant:
        if message.chat.username:
            invite_link = message.chat.username
            try:
                await userbot.resolve_peer(invite_link)
            except Exception as ex:
                logging.exception(ex)
        else:
            try:
                invite_link = await client.export_chat_invite_link(message.chat.id)
            except ChatAdminRequired:
                return await msg.edit_text(
                    f"🚫 𝗡𝗮̃𝗼 𝘁𝗲𝗻𝗵𝗼 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗽𝗮𝗿𝗮 𝗰𝗼𝗻𝘃𝗶𝗱𝗮𝗿 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗽𝗼𝗿 "
                    f"𝗹𝗶𝗻𝗸 𝗽𝗮𝗿𝗮 𝗮𝗱𝗶𝗰𝗶𝗼𝗻𝗮𝗿 𝗮 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 {userbot.mention} 𝗮𝗼 "
                    f"{message.chat.title}."
                )
            except InviteRequestSent:
                try:
                    await app.approve_chat_join_request(message.chat.id, userbot.id)
                except Exception as e:
                    return await msg.edit(
                        f"❌ 𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗰𝗼𝗻𝘃𝗶𝗱𝗮𝗿 𝗼 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 {userbot.mention} 𝗽𝗮𝗿𝗮 {message.chat.title}.\n\n<b>🛑 𝗠𝗼𝘁𝗶𝘃𝗼:</b> `{e}`"
                    )
            except Exception as ex:
                if "channels.JoinChannel" in str(ex) or "Username not found" in str(ex):
                    return await msg.edit_text(
                        f"🚫 𝗡𝗮̃𝗼 𝘁𝗲𝗻𝗵𝗼 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗽𝗮𝗿𝗮 𝗰𝗼𝗻𝘃𝗶𝗱𝗮𝗿 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 "
                        f"𝗽𝗼𝗿 𝗹𝗶𝗻𝗸 𝗽𝗮𝗿𝗮 𝗮𝗱𝗶𝗰𝗶𝗼𝗻𝗮𝗿 𝗮 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 {userbot.mention} 𝗮𝗼 "
                        f"{message.chat.title}."
                    )
                else:
                    return await msg.edit_text(
                        f"❌ 𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗰𝗼𝗻𝘃𝗶𝗱𝗮𝗿 𝗮 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 {userbot.mention} 𝗽𝗮𝗿𝗮 {message.chat.title}.\n\n<b>🛑 𝗠𝗼𝘁𝗶𝘃𝗼:</b> `{ex}`"
                    )
        if invite_link.startswith("https://t.me/+"):
            invite_link = invite_link.replace(
                "https://t.me/+", "https://t.me/joinchat/"
            )
        anon = await msg.edit_text(
            f"⏳ 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗮𝗴𝘂𝗮𝗿𝗱𝗲...\n\n🔗 𝗖𝗼𝗻𝘃𝗶𝗱𝗮𝗻𝗱𝗼 {userbot.mention} 𝗽𝗮𝗿𝗮 {message.chat.title}."
        )
        try:
            await userbot.join_chat(invite_link)
            await asyncio.sleep(2)
            await msg.edit_text(
                f"✅ {userbot.mention} 𝗲𝗻𝘁𝗿𝗼𝘂 𝗰𝗼𝗺 𝘀𝘂𝗰𝗲𝘀𝘀𝗼,\n\n📡 𝗶𝗻𝗶𝗰𝗶𝗮𝗻𝗱𝗼 𝘁𝗿𝗮𝗻𝘀𝗺𝗶𝘀𝘀𝗮̃𝗼..."
            )
        except UserAlreadyParticipant:
            pass
        except InviteRequestSent:
            try:
                await app.approve_chat_join_request(message.chat.id, userbot.id)
            except Exception as e:
                logging.error(str(e))
                return await msg.edit(
                    f"❌ 𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗰𝗼𝗻𝘃𝗶𝗱𝗮𝗿 𝗼 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 {userbot.mention} 𝗽𝗮𝗿𝗮 {message.chat.title}.\n\n<b>🛑 𝗠𝗼𝘁𝗶𝘃𝗼:</b> `{ex}`"
                )
        except Exception as ex:
            if "channels.JoinChannel" in str(ex) or "Username not found" in str(ex):
                return await msg.edit_text(
                    f"🚫 𝗡𝗮̃𝗼 𝘁𝗲𝗻𝗵𝗼 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗽𝗮𝗿𝗮 𝗰𝗼𝗻𝘃𝗶𝗱𝗮𝗿 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗽𝗼𝗿 "
                    f"𝗹𝗶𝗻𝗸 𝗽𝗮𝗿𝗮 𝗮𝗱𝗶𝗰𝗶𝗼𝗻𝗮𝗿 𝗼 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 {userbot.mention} 𝗮𝗼 "
                    f"{message.chat.title}."
                )
            else:
                return await msg.edit_text(
                    f"❌ 𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗰𝗼𝗻𝘃𝗶𝗱𝗮𝗿 𝗼 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 {userbot.mention} 𝗽𝗮𝗿𝗮 {message.chat.title}.\n\n<b>🛑 𝗠𝗼𝘁𝗶𝘃𝗼:</b> `{ex}`"
                )

        try:
            await userbot.resolve_peer(invite_link)
        except Exception as e:
            logging.error(str(e))
    await msg.delete()
    mode = message.command[0][0]
    user_id = message.from_user.id
    _playlist = await get_playlist_names(user_id)
    if not _playlist:
        try:
            return await message.reply(
                _["playlist_3"],
                quote=True,
            )
        except Exception as e:
            logging.error(str(e))
            return

    chat_id = message.chat.id
    user_name = message.from_user.first_name

    try:
        await message.delete()
    except Exception as e:
        logging.error(str(e))

    result = []
    video = True if mode == "v" else None
    mystic = await message.reply_text(_["play_1"])

    for vidids in _playlist:
        result.append(vidids)

    try:
        await stream(
            _,
            mystic,
            user_id,
            result,
            chat_id,
            user_name,
            message.chat.id,
            video,
            stream_type="playlist",
        )
    except Exception as e:
        ex_type = type(e).__name__
        err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
        return await mystic.edit_text(err)

    return await mystic.delete()


@app.on_callback_query(filters.regex("play_cplaylist") & ~BANNED_USERS)
@language_cb
async def play_playlist(_client: app, callback_query: CallbackQuery, _):
    callback_data = callback_query.data.strip()
    mode = callback_data.split(None, 1)[1]
    user_id = callback_query.from_user.id
    _playlist = await get_playlist_names(callback_query.message.chat.id)
    if not _playlist:
        try:
            return await callback_query.answer(
                _["playlist_19"],
                show_alert=True,
            )
        except Exception as e:
            logging.error(str(e))
            return
    chat_id = callback_query.message.chat.id
    user_name = callback_query.from_user.first_name
    await callback_query.message.delete()
    result = []
    try:
        await callback_query.answer()
    except:
        pass
    video = True if mode == "v" else None
    mystic = await callback_query.message.reply_text(_["play_1"])
    for vidids in _playlist:
        result.append(vidids)
    try:
        await stream(
            _,
            mystic,
            user_id,
            result,
            chat_id,
            user_name,
            callback_query.message.chat.id,
            video,
            stream_type="playlist",
        )
    except Exception as e:
        ex_type = type(e).__name__
        err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
        return await mystic.edit_text(err)
    return await mystic.delete()


@app.on_message(
    filters.command(PLAYLISTS_COMMAND, PREFIXES) & ~BANNED_USERS & filters.group
)
@language_cb
async def play_playlist_command(_client: app, message: Message, _):
    mode = message.command[0][0]
    user_id = message.from_user.id
    _playlist = await get_playlist_names(message.chat.id)
    if not _playlist:
        try:
            return await message.reply(
                _["playlist_3"],
                quote=True,
            )
        except Exception as e:
            logging.error(str(e))
            return

    chat_id = message.chat.id
    user_name = message.from_user.first_name

    try:
        await message.delete()
    except Exception as e:
        logging.error(str(e))

    result = []
    video = True if mode == "v" else None
    mystic = await message.reply_text(_["play_1"])

    for vidids in _playlist:
        result.append(vidids)

    try:
        await stream(
            _,
            mystic,
            user_id,
            result,
            chat_id,
            user_name,
            message.chat.id,
            video,
            stream_type="playlist",
        )
    except Exception as e:
        ex_type = type(e).__name__
        err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
        return await mystic.edit_text(err)

    return await mystic.delete()


@app.on_message(filters.command(ADDPLAYLIST_COMMAND, PREFIXES) & ~BANNED_USERS)
@language
async def add_playlist(_client: app, message: Message, _):
    if len(message.command) < 2:
        return await message.reply_text(
            "📌 <b>𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗺𝗲 𝗳𝗼𝗿𝗻𝗲𝗰̧𝗮 𝘂𝗺 𝗻𝗼𝗺𝗲 𝗱𝗲 𝗺𝘂́𝘀𝗶𝗰𝗮, 𝘂𝗺 𝗹𝗶𝗻𝗸 𝗱𝗲 "
            "𝗺𝘂́𝘀𝗶𝗰𝗮 𝗼𝘂 𝘂𝗺 𝗹𝗶𝗻𝗸 𝗱𝗲 𝗽𝗹𝗮𝘆𝗹𝗶𝘀𝘁 𝗱𝗼 𝗬𝗼𝘂𝗧𝘂𝗯𝗲 𝗮𝗽𝗼́𝘀 𝗼"
            "𝗰𝗼𝗺𝗮𝗻𝗱𝗼.</b>\n\n<b>📋 𝗘𝘅𝗲𝗺𝗽𝗹𝗼𝘀:</b>\n\n▷ `/addplaylist Ram siya ram` (𝗶𝗻𝘀𝗶𝗿𝗮 𝗼 𝗻𝗼𝗺𝗲 𝗱𝗲 𝘂𝗺𝗮 𝗺𝘂́𝘀𝗶𝗰𝗮 "
            "𝗲𝘀𝗽𝗲𝗰𝗶́𝗳𝗶𝗰𝗮)\n\n▷ <code>/addplaylist [𝗹𝗶𝗻𝗸 𝗱𝗮 𝗽𝗹𝗮𝘆𝗹𝗶𝘀𝘁 𝗱𝗼 "
            "𝗬𝗼𝘂𝗧𝘂𝗯𝗲]</code> (𝗽𝗮𝗿𝗮 𝗮𝗱𝗶𝗰𝗶𝗼𝗻𝗮𝗿 𝘁𝗼𝗱𝗮𝘀 𝗮𝘀 𝗺𝘂́𝘀𝗶𝗰𝗮𝘀 𝗱𝗲 𝘂𝗺𝗮"
            "𝗽𝗹𝗮𝘆𝗹𝗶𝘀𝘁 𝗱𝗼 𝗬𝗼𝘂𝗧𝘂𝗯𝗲 𝗮̀ 𝗽𝗹𝗮𝘆𝗹𝗶𝘀𝘁 𝗱𝗼 𝗯𝗼𝘁.)"
        )

    query = message.command[1]

    # Check if the provided input is a YouTube playlist link
    if "youtube.com/playlist" in query:
        adding = await message.reply_text(
            "<b>Adicionando músicas à playlist, por favor aguarde...</b>"
        )
        try:
            from pytube import Playlist, YouTube

            playlist = Playlist(query)
            video_urls = playlist.video_urls

        except Exception as e:
            return await message.reply_text(f"Error: {e}")

        if not video_urls:
            return await message.reply_text(
                "<b>Nenhuma música encontrada nos links da playlist.</b>\n\n<b>Tente outro link de playlist</b>"
            )

        user_id = message.from_user.id
        for video_url in video_urls:
            video_id = video_url.split("v=")[-1]

            try:
                yt = YouTube(video_url)
                title = yt.title
                duration = yt.length
            except Exception as e:
                return await message.reply_text(
                    f"Erro ao obter informações do vídeo: {e}"
                )

            plist = {
                "videoid": video_id,
                "title": title,
                "duration": duration,
            }

            await save_playlist(user_id, video_id, plist)

        keyboardes = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="๏ Deseja remover alguma música? ๏",
                        url=f"https://t.me/{app.username}?start=delplaylists",
                    ),
                ]
            ]
        )
        await adding.delete()
        return await message.reply_text(
            text="<b>Todas as músicas da sua playlist do YouTube foram adicionadas com sucesso!</b>\n\n<b>Para remover "
            "alguma música, clique no botão abaixo.</b>",
            reply_markup=keyboardes,
        )
    if "youtube.com/@" in query:
        addin = await message.reply_text(
            "<b>Adicionando músicas à playlist, por favor aguarde...</b>"
        )
        try:
            from pytube import YouTube

            videos = YouTube_videos(f"{query}/videos")
            video_urls = [video["url"] for video in videos]

        except Exception as e:
            return await message.reply_text(f"Error: {e}")

        if not video_urls:
            return await message.reply_text(
                "<b>Nenhuma música encontrada no link da playlist.</b>\n\n<b>Tente outro link do YouTube</b>"
            )

        user_id = message.from_user.id
        for video_url in video_urls:
            video_id = query.split("/")[-1].split("?")[0]

            try:
                yt = YouTube(f"https://youtu.be/{video_id}")
                title = yt.title
                duration = yt.length
            except Exception as e:
                return await message.reply_text(
                    f"Erro ao buscar informações do vídeo: {e}"
                )

            plist = {
                "videoid": video_id,
                "title": title,
                "duration": duration,
            }

            await save_playlist(user_id, video_id, plist)
        keyboardes = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="๏ Deseja remover alguma música? ๏",
                        url=f"https://t.me/{app.username}?start=delplaylists",
                    ),
                ]
            ]
        )
        await addin.delete()
        return await message.reply_text(
            text="<b>Todas as músicas da sua playlist do YouTube foram adicionadas com sucesso!</b>\n\n<b>Para remover "
            "alguma música, clique no botão abaixo.</b>",
            reply_markup=keyboardes,
        )
    # Check if the provided input is a YouTube video link
    if "https://youtu.be" in query:
        try:
            add = await message.reply_text(
                "<b>Adicionando músicas à playlist, por favor aguarde...</b>"
            )
            from pytube import Playlist, YouTube

            # Extract video ID from the YouTube lin
            videoid = query.split("/")[-1].split("?")[0]
            user_id = message.from_user.id
            thumbnail = f"https://img.youtube.com/vi/{videoid}/maxresdefault.jpg"
            _check = await get_playlist(user_id, videoid)
            if _check:
                try:
                    await add.delete()
                    return await message.reply_photo(thumbnail, caption=_["playlist_8"])
                except KeyError:
                    pass

            _count = await get_playlist_names(user_id)
            count = len(_count)
            if count == SERVER_PLAYLIST_LIMIT:
                try:
                    return await message.reply_text(
                        _["playlist_9"].format(SERVER_PLAYLIST_LIMIT)
                    )
                except KeyError:
                    pass

            try:
                yt = YouTube(f"https://youtu.be/{videoid}")
                title = yt.title
                duration = yt.length
                thumbnail = f"https://img.youtube.com/vi/{videoid}/maxresdefault.jpg"
                plist = {
                    "videoid": videoid,
                    "title": title,
                    "duration": duration,
                }
                await save_playlist(user_id, videoid, plist)

                await add.delete()
                await message.reply_photo(
                    thumbnail, caption="<b>Música adicionada à sua playlist do bot</b>"
                )
            except Exception as e:
                print(f"Error: {e}")
                await message.reply_text(str(e))
        except Exception as e:
            return await message.reply_text(str(e))
    else:
        from CineWinx import YouTube

        # Add a specific song by name
        query = " ".join(message.command[1:])
        print(query)

        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            link = f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]["title"][:40]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            videoid = results[0]["id"]
            # Add these lines to define views and channel_name
            results[0]["views"]
            results[0]["channel"]

            user_id = message.from_user.id
            _check = await get_playlist(user_id, videoid)
            if _check:
                try:
                    return await message.reply_photo(thumbnail, caption=_["playlist_8"])
                except KeyError:
                    pass

            _count = await get_playlist_names(user_id)
            count = len(_count)
            if count == SERVER_PLAYLIST_LIMIT:
                try:
                    return await message.reply_text(
                        _["playlist_9"].format(SERVER_PLAYLIST_LIMIT)
                    )
                except KeyError:
                    pass

            m = await message.reply("<b>Adicionando, por favor aguarde...</b>")
            title, duration_min, _, _, _ = await YouTube.details(videoid, True)
            title = (title[:50]).title()
            plist = {
                "videoid": videoid,
                "title": title,
                "duration": duration_min,
            }

            await save_playlist(user_id, videoid, plist)
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "๏ Remover da playlist ๏",
                            callback_data=f"remove_playlist {videoid}",
                        )
                    ]
                ]
            )

            await m.delete()
            await message.reply_photo(
                thumbnail,
                caption="<b>Música adicionada à sua playlist do bot</b>",
                reply_markup=keyboard,
            )

        except KeyError:
            return await message.reply_text("<b>Formato de data inválido.</b>")
        except Exception:
            pass


@app.on_callback_query(filters.regex("remove_playlist") & ~BANNED_USERS)
@language_cb
async def del_plist(_client: app, callback_query: CallbackQuery, _):
    callback_data = callback_query.data.strip()
    videoid = callback_data.split(None, 1)[1]
    callback_query.from_user.id
    deleted = await delete_playlist(callback_query.from_user.id, videoid)
    if deleted:
        try:
            await callback_query.answer(_["playlist_11"], show_alert=True)
        except Exception as e:
            pass
    else:
        try:
            return await callback_query.answer(_["playlist_12"], show_alert=True)
        except Exception as e:
            return
    keyboards = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔄 𝗥𝗲𝗰𝘂𝗽𝗲𝗿𝗮𝗿 𝘀𝘂𝗮 𝗺𝘂́𝘀𝗶𝗰𝗮",
                    callback_data=f"recover_playlist {videoid}",
                )
            ]
        ]
    )
    return await callback_query.edit_message_text(
        text="<b>Sua música foi removida da sua playlist do bot</b>\n\n<b>"
        "Para recuperar sua música na playlist, clique no botão abaixo.</b>",
        reply_markup=keyboards,
    )


@app.on_callback_query(filters.regex("recover_playlist") & ~BANNED_USERS)
@language_cb
async def add_playlist(_client: app, callback_query: CallbackQuery, _):
    from CineWinx import YouTube

    callback_data = callback_query.data.strip()
    videoid = callback_data.split(None, 1)[1]
    user_id = callback_query.from_user.id
    _check = await get_playlist(user_id, videoid)
    if _check:
        try:
            return await callback_query.answer(_["playlist_8"], show_alert=True)
        except Exception as e:
            logging.error(str(e))
            return
    _count = await get_playlist_names(user_id)
    count = len(_count)
    if count == SERVER_PLAYLIST_LIMIT:
        try:
            return await callback_query.answer(
                _["playlist_9"].format(SERVER_PLAYLIST_LIMIT),
                show_alert=True,
            )
        except Exception as e:
            logging.error(str(e))
            return
    (
        title,
        duration_min,
        duration_sec,
        thumbnail,
        vidid,
    ) = await YouTube.details(videoid, True)
    title = (title[:50]).title()
    plist = {
        "videoid": vidid,
        "title": title,
        "duration": duration_min,
    }
    await save_playlist(user_id, videoid, plist)
    try:
        title = (title[:30]).title()
        return await callback_query.edit_message_text(
            text=f"🔄 <b>𝗠𝘂́𝘀𝗶𝗰𝗮 𝗿𝗲𝗰𝘂𝗽𝗲𝗿𝗮𝗱𝗮 𝗻𝗮 𝘀𝘂𝗮 𝗽𝗹𝗮𝘆𝗹𝗶𝘀𝘁: {title}</b>"
        )
    except Exception as e:
        logging.error(str(e))
        return


@app.on_callback_query(filters.regex("remove_playlist") & ~BANNED_USERS)
@language_cb
async def del_plist(_client: app, callback_query: CallbackQuery, _):
    callback_data = callback_query.data.strip()
    videoid = callback_data.split(None, 1)[1]
    callback_query.from_user.id
    deleted = await delete_playlist(callback_query.from_user.id, videoid)
    if deleted:
        try:
            await callback_query.answer(_["playlist_11"], show_alert=True)
        except Exception as e:
            logging.error(str(e))
    else:
        try:
            return await callback_query.answer(_["playlist_12"], show_alert=True)
        except Exception as e:
            logging.error(str(e))
            return

    return await callback_query.edit_message_text(
        text="❌ <b>𝗦𝘂𝗮 𝗺𝘂́𝘀𝗶𝗰𝗮 𝗳𝗼𝗶 𝗿𝗲𝗺𝗼𝘃𝗶𝗱𝗮 𝗱𝗮 𝘀𝘂𝗮 𝗽𝗹𝗮𝘆𝗹𝗶𝘀𝘁 𝗱𝗼 𝗯𝗼𝘁</b>"
    )


@app.on_callback_query(filters.regex("add_playlist") & ~BANNED_USERS)
@language_cb
async def add_playlist(_client: app, callback_query: CallbackQuery, _):
    try:
        from CineWinx import YouTube
    except ImportError as e:
        print(f"ERROR {e}")
        return

    callback_data = callback_query.data.strip()
    videoid = callback_data.split(None, 1)[1]
    user_id = callback_query.from_user.id
    _check = await get_playlist(user_id, videoid)
    if _check:
        try:
            return await callback_query.answer(_["playlist_8"], show_alert=True)
        except Exception as e:
            logging.error(str(e))
            return
    _count = await get_playlist_names(user_id)
    count = len(_count)
    if count == SERVER_PLAYLIST_LIMIT:
        try:
            return await callback_query.answer(
                _["playlist_9"].format(SERVER_PLAYLIST_LIMIT),
                show_alert=True,
            )
        except:
            return
    (
        title,
        duration_min,
        duration_sec,
        thumbnail,
        vidid,
    ) = await YouTube.details(videoid, True)
    title = (title[:50]).title()
    plist = {
        "videoid": vidid,
        "title": title,
        "duration": duration_min,
    }
    await save_playlist(user_id, videoid, plist)
    try:
        title = (title[:30]).title()
        return await callback_query.answer(
            _["playlist_10"].format(title), show_alert=True
        )
    except:
        return


@app.on_callback_query(filters.regex("group_addplaylist") & ~BANNED_USERS)
@language_cb
async def add_playlist(_client: app, callback_query: CallbackQuery, _):
    try:
        from CineWinx import YouTube
    except ImportError as e:
        print(f"ERROR {e}")
        return

    callback_data = callback_query.data.strip()
    videoid = callback_data.split(None, 1)[1]
    user_id = callback_query.from_user.id
    _check = await get_playlist(callback_query.message.chat.id, videoid)
    if _check:
        try:
            return await callback_query.answer(
                "🔄 𝗝𝗮́ 𝗲𝘅𝗶𝘀𝘁𝗲\n\n𝗘𝘀𝘁𝗮 𝗳𝗮𝗶𝘅𝗮 𝗷𝗮́ 𝗲𝘅𝗶𝘀𝘁𝗲 𝗻𝗮 𝗽𝗹𝗮𝘆𝗹𝗶𝘀𝘁 𝗱𝗼 𝗴𝗿𝘂𝗽𝗼.",
                show_alert=True,
            )
        except Exception as e:
            logging.error(str(e))
            return
    _count = await get_playlist_names(callback_query.message.chat.id)
    count = len(_count)
    if count == SERVER_PLAYLIST_LIMIT:
        try:
            return await callback_query.answer(
                _["playlist_9"].format(SERVER_PLAYLIST_LIMIT),
                show_alert=True,
            )
        except:
            return
    (
        title,
        duration_min,
        duration_sec,
        thumbnail,
        vidid,
    ) = await YouTube.details(videoid, True)
    title = (title[:50]).title()
    plist = {
        "videoid": vidid,
        "title": title,
        "duration": duration_min,
    }
    await save_playlist(callback_query.message.chat.id, videoid, plist)
    try:
        title = (title[:30]).title()
        return await callback_query.answer(
            _["playlist_10"].format(title), show_alert=True
        )
    except:
        return


@app.on_callback_query(filters.regex("del_playlist") & ~BANNED_USERS)
@language_cb
async def del_plist(_client: app, callback_query: CallbackQuery, _):
    pass

    callback_data = callback_query.data.strip()
    videoid = callback_data.split(None, 1)[1]
    user_id = callback_query.from_user.id
    deleted = await delete_playlist(callback_query.from_user.id, videoid)
    if deleted:
        try:
            await callback_query.answer(_["playlist_11"], show_alert=True)
        except Exception as e:
            pass
    else:
        try:
            return await callback_query.answer(_["playlist_12"], show_alert=True)
        except Exception as e:
            return
    keyboard, count = await get_keyboard(_, user_id)
    return await callback_query.edit_message_reply_markup(reply_markup=keyboard)


@app.on_callback_query(filters.regex("del_cplaylist") & ~BANNED_USERS)
@language_cb
async def del_plist(_client: app, callback_query: CallbackQuery, _):
    pass

    callback_data = callback_query.data.strip()
    videoid = callback_data.split(None, 1)[1]
    user_id = callback_query.from_user.id
    deleted = await delete_playlist(callback_query.message.chat.id, videoid)
    if deleted:
        try:
            await callback_query.answer(_["playlist_11"], show_alert=True)
        except Exception as e:
            logging.error(str(e))
    else:
        try:
            return await callback_query.answer(_["playlist_12"], show_alert=True)
        except Exception as e:
            logging.error(str(e))
            return
    keyboard, count = await get_keyboard(_, callback_query.message.chat.id)
    return await callback_query.edit_message_reply_markup(reply_markup=keyboard)


@app.on_callback_query(filters.regex("delete_whole_playlist") & ~BANNED_USERS)
@language_cb
async def del_whole_playlist(_client: app, callback_query: CallbackQuery, _):
    pass

    _playlist = await get_playlist_names(callback_query.from_user.id)
    for x in _playlist:
        await callback_query.answer(
            "⏳ 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗮𝗴𝘂𝗮𝗿𝗱𝗲.\n𝗘𝘅𝗰𝗹𝘂𝗶𝗻𝗱𝗼 𝘀𝘂𝗮 𝗽𝗹𝗮𝘆𝗹𝗶𝘀𝘁...", show_alert=True
        )
        await delete_playlist(callback_query.from_user.id, x)
    return await callback_query.edit_message_text(_["playlist_13"])


@app.on_callback_query(filters.regex("get_cplaylist_playmode") & ~BANNED_USERS)
@app.on_callback_query(filters.regex("get_playlist_playmode") & ~BANNED_USERS)
@language_cb
async def get_playlist_playmode_(_client: app, callback_query: CallbackQuery, _):
    try:
        await callback_query.answer()
    except Exception as e:
        logging.error(str(e))
    if callback_query.data.startswith("get_playlist_playmode"):
        buttons = get_playlist_markup(_)
        return await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    if callback_query.data.startswith("get_cplaylist_playmode"):
        buttons = get_cplaylist_markup(_)
        return await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )


@app.on_callback_query(filters.regex("delete_warning") & ~BANNED_USERS)
@language_cb
async def delete_warning_message(_client: app, callback_query: CallbackQuery, _):
    pass

    try:
        await callback_query.answer()
    except Exception as e:
        logging.error(str(e))
    upl = warning_markup(_)
    return await callback_query.edit_message_text(_["playlist_14"], reply_markup=upl)


@app.on_callback_query(filters.regex("home_play") & ~BANNED_USERS)
@language_cb
async def home_play_(_client: app, callback_query: CallbackQuery, _):
    pass

    try:
        await callback_query.answer()
    except Exception as e:
        logging.error(str(e))
    buttons = botplaylist_markup(_)
    return await callback_query.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex("del_back_playlist") & ~BANNED_USERS)
@language_cb
async def del_back_playlist(_client: app, callback_query: CallbackQuery, _):
    pass

    user_id = callback_query.from_user.id
    _playlist = await get_playlist_names(user_id)
    if _playlist:
        try:
            await callback_query.answer(_["playlist_2"], show_alert=True)
        except Exception as e:
            logging.error(str(e))
    else:
        try:
            return await callback_query.answer(_["playlist_3"], show_alert=True)
        except Exception as e:
            logging.error(str(e))
            return
    keyboard, count = await get_keyboard(_, user_id)
    return await callback_query.edit_message_text(
        _["playlist_7"].format(count), reply_markup=keyboard
    )


__MODULE__ = "𝗣𝗹𝗮𝘆𝗹𝗶𝘀𝘁 📃"
__HELP__ = """
🎵<b>𝗙𝘂𝗻𝗰𝗶𝗼𝗻𝗮𝗹𝗶𝗱𝗮𝗱𝗲𝘀 𝗱𝗲 𝗣𝗹𝗮𝘆𝗹𝗶𝘀𝘁 𝗽𝗮𝗿𝗮 𝘃𝗼𝗰𝗲̂:</b>

📋 <code>/playlist</code> - 𝗩𝗲𝗿𝗶𝗳𝗶𝗾𝘂𝗲 𝘀𝘂𝗮 𝗽𝗹𝗮𝘆𝗹𝗶𝘀𝘁 𝘀𝗮𝗹𝘃𝗮 𝗻𝗼𝘀 𝘀𝗲𝗿𝘃𝗶𝗱𝗼𝗿𝗲𝘀.

❌ <code>/delplaylist</code> - 𝗘𝘅𝗰𝗹𝘂𝗮 𝗾𝘂𝗮𝗹𝗾𝘂𝗲𝗿 𝗺𝘂́𝘀𝗶𝗰𝗮 𝘀𝗮𝗹𝘃𝗮 𝗲𝗺 𝘀𝘂𝗮 𝗽𝗹𝗮𝘆𝗹𝗶𝘀𝘁.

▶️ <code>/play</code> - 𝗖𝗼𝗺𝗲𝗰̧𝗲 𝗮 𝗿𝗲𝗽𝗿𝗼𝗱𝘂𝘇𝗶𝗿 𝘀𝘂𝗮 𝗽𝗹𝗮𝘆𝗹𝗶𝘀𝘁 𝘀𝗮𝗹𝘃𝗮 𝗱𝗼𝘀 𝘀𝗲𝗿𝘃𝗶𝗱𝗼𝗿𝗲𝘀.

🎧 <code>/playplaylist</code> - 𝗖𝗼𝗺𝗲𝗰̧𝗲 𝗮 𝗿𝗲𝗽𝗿𝗼𝗱𝘂𝘇𝗶𝗿 𝗱𝗶𝗿𝗲𝘁𝗮𝗺𝗲𝗻𝘁𝗲 𝘀𝘂𝗮 𝗽𝗹𝗮𝘆𝗹𝗶𝘀𝘁 𝘀𝗮𝗹𝘃𝗮 𝗱𝗼𝘀 𝘀𝗲𝗿𝘃𝗶𝗱𝗼𝗿𝗲𝘀 [𝗮𝗽𝗲𝗻𝗮𝘀 𝗮́𝘂𝗱𝗶𝗼, 𝘀𝗲𝗺 𝘃𝗶́𝗱𝗲𝗼].

📹 <code>/vplayplaylist</code> - 𝗖𝗼𝗺𝗲𝗰̧𝗲 𝗮 𝗿𝗲𝗽𝗿𝗼𝗱𝘂𝘇𝗶𝗿 𝗱𝗶𝗿𝗲𝘁𝗮𝗺𝗲𝗻𝘁𝗲 𝘀𝘂𝗮 𝗽𝗹𝗮𝘆𝗹𝗶𝘀𝘁 𝘀𝗮𝗹𝘃𝗮 𝗱𝗼𝘀 𝘀𝗲𝗿𝘃𝗶𝗱𝗼𝗿𝗲𝘀 [𝗮́𝘂𝗱𝗶𝗼 𝗰𝗼𝗺 𝘃𝗶́𝗱𝗲𝗼].

➕ <code>/addplaylist</code> - [𝗹𝗶𝗻𝗸 𝗱𝗼 𝘃𝗶́𝗱𝗲𝗼 𝗱𝗼 𝗬𝗼𝘂𝗧𝘂𝗯𝗲] 𝗼𝘂 [𝗹𝗶𝗻𝗸 𝗱𝗮 𝗽𝗹𝗮𝘆𝗹𝗶𝘀𝘁 𝗱𝗼 𝗬𝗼𝘂𝗧𝘂𝗯𝗲] 𝗼𝘂 [𝗻𝗼𝗺𝗲 𝗱𝗮 𝗺𝘂́𝘀𝗶𝗰𝗮] 𝗽𝗮𝗿𝗮 𝗮𝗱𝗶𝗰𝗶𝗼𝗻𝗮𝗿 𝗮̀ 𝘀𝘂𝗮 𝗽𝗹𝗮𝘆𝗹𝗶𝘀𝘁 𝗱𝗼 𝗯𝗼𝘁.
"""
