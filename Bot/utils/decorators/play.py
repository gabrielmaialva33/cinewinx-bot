import asyncio
import logging

from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from Bot import YouTube, app
from Bot.database import (
    get_assistant,
    get_cmode,
    get_lang,
    get_playmode,
    get_playtype,
    is_active_chat,
    is_command_delete_on,
    is_served_private_chat,
)
from Bot.misc import SUDOERS
from Bot.utils import bot_playlist_markup
from config import PLAYLIST_IMG_URL, PRIVATE_BOT_MODE, adminlist
from strings import get_string

links = {}


def play_wrapper(command):
    async def wrapper(client: Client, message: Message):
        language = await get_lang(message.chat.id)
        _ = get_string(language)

        # check if the message is from a sender chat
        if message.sender_chat:
            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Como corrigir? 🛠️",
                            callback_data="anonymous_admin",
                        ),
                    ]
                ]
            )
            return await message.reply_text(_["anonymous_2"], reply_markup=upl)

        # check if the bot is private, and if the chat is authorized
        if PRIVATE_BOT_MODE == str(True):
            if not await is_served_private_chat(message.chat.id):
                await message.reply_text(
                    "🚫 Bot Privado 🚫\n\n➜ Este bot é privado para chats autorizados."
                )
                return await client.leave_chat(message.chat.id)

        # delete the command message if the delete command is on
        if await is_command_delete_on(message.chat.id):
            try:
                member = await client.get_chat_member(message.chat.id, app.me.id)
                if member.status == ChatMemberStatus.ADMINISTRATOR:
                    await message.delete()
            except Exception as e:
                logging.error(e)

        audio_telegram = (
            (message.reply_to_message.audio or message.reply_to_message.voice)
            if message.reply_to_message
            else None
        )

        video_telegram = (
            (message.reply_to_message.video or message.reply_to_message.document)
            if message.reply_to_message
            else None
        )

        url = await YouTube.url(message)

        if audio_telegram is None and video_telegram is None and url is None:
            if len(message.command) < 2:
                if "stream" in message.command:
                    return await message.reply_text(_["str_1"])
                buttons = bot_playlist_markup(_)
                return await message.reply_photo(
                    photo=PLAYLIST_IMG_URL,
                    caption=_["playlist_1"],
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
        if message.command[0][0] == "c":
            chat_id = await get_cmode(message.chat.id)
            if chat_id is None:
                return await message.reply_text(_["setting_12"])
            try:
                chat = await app.get_chat(chat_id)
            except Exception as e:
                logging.error(e)
                return await message.reply_text(_["cplay_4"])
            channel = chat.title
        else:
            chat_id = message.chat.id
            channel = None
        playmode = await get_playmode(message.chat.id)
        playty = await get_playtype(message.chat.id)
        if playty != "Everyone":
            if message.from_user.id not in SUDOERS:
                admins = adminlist.get(message.chat.id)
                if not admins:
                    return await message.reply_text(_["admin_18"])
                else:
                    if message.from_user.id not in admins:
                        return await message.reply_text(_["play_4"])
        if message.command[0][0] == "v":
            video = True
        else:
            if "-v" in message.text:
                video = True
            else:
                video = True if message.command[0][1] == "v" else None
        if message.command[0][-1] == "e":
            if not await is_active_chat(chat_id):
                return await message.reply_text(_["play_18"])
            fplay = True
        else:
            fplay = None

        if not await is_active_chat(chat_id):
            userbot = await get_assistant(message.chat.id)
            try:
                try:
                    get = await app.get_chat_member(chat_id, userbot.id)
                except ChatAdminRequired:
                    return await message.reply_text(_["call_1"])
                if (
                    get.status == ChatMemberStatus.BANNED
                    or get.status == ChatMemberStatus.RESTRICTED
                ):
                    return await message.reply_text(
                        text=_["call_2"].format(userbot.username, userbot.id),
                    )
            except UserNotParticipant:
                if chat_id in links:
                    invite_link = links[chat_id]
                else:
                    if message.chat.username:
                        invite_link = message.chat.username
                        try:
                            await userbot.resolve_peer(invite_link)
                        except Exception as e:
                            logging.error(e)
                            pass
                    else:
                        try:
                            await client.get_chat_member(message.chat.id, "me")
                            invite_link = await client.export_chat_invite_link(
                                message.chat.id
                            )
                        except ChatAdminRequired:
                            return await message.reply_text(_["call_1"])
                        except Exception as e:
                            logging.error(e)
                            return await message.reply_text(
                                _["call_3"].format(app.mention, type(e).__name__)
                            )

                if invite_link.startswith("https://t.me/+"):
                    invite_link = invite_link.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
                myu = await message.reply_text(_["call_17"])
                try:
                    await asyncio.sleep(1)
                    await userbot.join_chat(invite_link)
                except InviteRequestSent:
                    try:
                        await app.approve_chat_join_request(chat_id, userbot.id)
                    except Exception as e:
                        return await message.reply_text(
                            _["call_3"].format(type(e).__name__)
                        )
                    await asyncio.sleep(3)
                    await myu.edit(_["call_5"].format(app.mention))
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    return await message.reply_text(
                        _["call_3"].format(type(e).__name__)
                    )

                links[chat_id] = invite_link

                try:
                    await userbot.resolve_peer(chat_id)
                except Exception as e:
                    logging.error(e)

        return await command(
            client,
            message,
            _,
            chat_id,
            video,
            channel,
            playmode,
            url,
            fplay,
        )

    return wrapper
