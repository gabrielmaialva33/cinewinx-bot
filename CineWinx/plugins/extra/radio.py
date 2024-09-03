import logging

import asyncio
from pyrogram import filters, Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    UserNotParticipant,
    InviteRequestSent,
    UserAlreadyParticipant,
)
from pyrogram.types import Message

from CineWinx import app
from CineWinx.misc import SUDOERS
from CineWinx.utils import (
    get_lang,
    get_assistant,
    get_playmode,
    get_playtype,
    get_cmode,
    play_logs,
)
from CineWinx.utils.stream.stream import stream
from config import PREFIXES, BANNED_USERS, adminlist
from strings import get_command, get_string

RADIO_COMMAND = get_command("RADIO_COMMAND")


RADIO_STATION = {
    # "Air Bilaspur": "http://air.pc.cdn.bitgravity.com/air/live/pbaudio110/playlist.m3u8",
    # "Air Raipur": "http://air.pc.cdn.bitgravity.com/air/live/pbaudio118/playlist.m3u8",
    # "Capital FM": "http://media-ice.musicradio.com/CapitalMP3?.mp3&listening-from-radio-garden=1616312105154",
    # "English": "https://hls-01-regions.emgsound.ru/11_msk/playlist.m3u8",
    # "Mirchi": "http://peridot.streamguys.com:7150/Mirchi",
    "galaxie": "http://stream.zenolive.com/fp2nmjjwojuv",
    "Hits Of Kishore Kumar": "http://stream.zenolive.com/0ghtfp8ztm0uv",
    "Jovem Pan FM": "http://stream.zenolive.com/c45wbq2us3buv",
    "Dance Wave!": "http://stream.zenolive.com/867h0na557zuv",
    "ChillSynth FM": "https://www.youtube.com/watch?v=UedTcufyrHc",
    "METAL 24/7 ": "https://www.youtube.com/watch?v=lCjVa1c5zKw",
    "Chill Radio 24/7": "https://www.youtube.com/watch?v=Ndx2zSuAaRQ",
}

valid_stations = "\n".join(
    [f"<code>{name}</code>" for name in sorted(RADIO_STATION.keys())]
)


@app.on_message(
    filters.command(RADIO_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS
)
async def radio(client: Client, message: Message):
    msg = await message.reply_text("⏳ 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗮𝗴𝘂𝗮𝗿𝗱𝗲 𝘂𝗺 𝗺𝗼𝗺𝗲𝗻𝘁𝗼....")

    userbot = await get_assistant(message.chat.id)
    try:
        try:
            get = await app.get_chat_member(message.chat.id, userbot.id)
        except ChatAdminRequired:
            return await msg.edit_text(
                f"𝗡𝗮̃𝗼 𝘁𝗲𝗻𝗵𝗼 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗽𝗮𝗿𝗮 𝗶𝗻𝘃𝗶𝘁𝗮𝗿 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗽𝗼𝗿 𝗹𝗶𝗻𝗸 𝗽𝗮𝗿𝗮 𝗰𝗼𝗻𝘃𝗶𝗱𝗮𝗿 {userbot.mention} 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗽𝗮𝗿𝗮 {message.chat.title}."
            )
        if get.status == ChatMemberStatus.BANNED:
            return await msg.edit_text(
                text=f"{userbot.mention} 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗲𝘀𝘁𝗮́ 𝗯𝗮𝗻𝗶𝗱𝗼 𝗲𝗺 {message.chat.title}\n\n🚫 𝗜𝗗: {userbot.id}\n🆔 𝗡𝗼𝗺𝗲: {userbot.mention}\n👤 𝗨𝘀𝘂𝗮́𝗿𝗶𝗼: @{userbot.username}\n\n𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗱𝗲𝘀𝗯𝗮𝗻𝗲 𝗼 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗲 𝘁𝗲𝗻𝘁𝗲 𝗻𝗼𝘃𝗮𝗺𝗲𝗻𝘁𝗲..."
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
                    f"🚫 𝗡𝗮̃𝗼 𝘁𝗲𝗻𝗵𝗼 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗽𝗮𝗿𝗮 𝗶𝗻𝘃𝗶𝘁𝗮𝗿 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗽𝗼𝗿 𝗹𝗶𝗻𝗸 𝗽𝗮𝗿𝗮 𝗰𝗼𝗻𝘃𝗶𝗱𝗮𝗿 {userbot.mention} 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗽𝗮𝗿𝗮 {message.chat.title}."
                )
            except InviteRequestSent:
                try:
                    await app.approve_chat_join_request(message.chat.id, userbot.id)
                except Exception as e:
                    logging.exception(e)
                    return await msg.edit(
                        f"𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗶𝗻𝘃𝗶𝘁𝗮𝗿 {userbot.mention} 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗽𝗮𝗿𝗮 {message.chat.title}.\n\n𝗠𝗼𝘁𝗶𝘃𝗼:{e}` ❌"
                    )
            except Exception as ex:
                if "channels.JoinChannel" in str(ex) or "Username not found" in str(ex):
                    return await msg.edit_text(
                        f"𝗡𝗮̃𝗼 𝘁𝗲𝗻𝗵𝗼 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗽𝗮𝗿𝗮 𝗶𝗻𝘃𝗶𝘁𝗮𝗿 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗽𝗼𝗿 𝗹𝗶𝗻𝗸 𝗽𝗮𝗿𝗮 𝗶𝗻𝘃𝗶𝘁𝗮𝗿 {userbot.mention} 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗽𝗮𝗿𝗮 {message.chat.title}. ❌"
                    )
                else:
                    return await msg.edit_text(
                        f"𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗶𝗻𝘃𝗶𝘁𝗮𝗿 {userbot.mention} 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗽𝗮𝗿𝗮 {message.chat.title}.\n\n𝗠𝗼𝘁𝗶𝘃𝗼: {ex} ⚠️"
                    )
        if invite_link.startswith("https://t.me/+"):
            invite_link = invite_link.replace(
                "https://t.me/+", "https://t.me/joinchat/"
            )
        anon = await msg.edit_text(
            f"⏳ 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗮𝗴𝘂𝗮𝗿𝗱𝗲...\n\n𝗜𝗻𝘃𝗶𝘁𝗮𝗻𝗱𝗼 {userbot.mention} 𝗽𝗮𝗿𝗮 {message.chat.title}."
        )
        try:
            await userbot.join_chat(invite_link)
            await asyncio.sleep(2)
            await msg.edit_text(
                f"{userbot.mention} 𝗲𝗻𝘁𝗿𝗼𝘂 𝗰𝗼𝗺 𝘀𝘂𝗰𝗲𝘀𝘀𝗼,\n\n𝗶𝗻𝗶𝗰𝗶𝗮𝗻𝗱𝗼 𝗮 𝘁𝗿𝗮𝗻𝘀𝗺𝗶𝘀𝘀𝗮̃𝗼... 🎶"
            )
        except UserAlreadyParticipant:
            pass
        except InviteRequestSent:
            try:
                await app.approve_chat_join_request(message.chat.id, userbot.id)
            except Exception as e:
                logging.exception(e)
                return await msg.edit_text(
                    f"𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗶𝗻𝘃𝗶𝘁𝗮𝗿 {userbot.mention} 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗽𝗮𝗿𝗮 {message.chat.title}.\n\n𝗠𝗼𝘁𝗶𝘃𝗼: {e} ⚠️"
                )
        except Exception as ex:
            if "channels.JoinChannel" in str(ex) or "Username not found" in str(ex):
                return await msg.edit_text(
                    f"𝗡𝗮̃𝗼 𝘁𝗲𝗻𝗵𝗼 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗽𝗮𝗿𝗮 𝗶𝗻𝘃𝗶𝘁𝗮𝗿 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗽𝗼𝗿 𝗹𝗶𝗻𝗸 𝗽𝗮𝗿𝗮 𝗶𝗻𝘃𝗶𝘁𝗮𝗿 {userbot.mention} 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗽𝗮𝗿𝗮 {message.chat.title}. ❌"
                )
            else:
                return await msg.edit_text(
                    f"𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗶𝗻𝘃𝗶𝘁𝗮𝗿 {userbot.mention} 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗽𝗮𝗿𝗮 {message.chat.title}.\n\n𝗠𝗼𝘁𝗶𝘃𝗼: {ex} ⚠️"
                )

        try:
            await userbot.resolve_peer(invite_link)
        except BaseException as e:
            logging.exception(e)
    await msg.delete()
    station_name = " ".join(message.command[1:])
    RADIO_URL = RADIO_STATION.get(station_name)
    if RADIO_URL:
        language = await get_lang(message.chat.id)
        _ = get_string(language)
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
        if message.command[0][0] == "c":
            chat_id = await get_cmode(message.chat.id)
            if chat_id is None:
                return await message.reply_text(_["setting_12"])
            try:
                chat = await app.get_chat(chat_id)
            except BaseException as e:
                logging.exception(e)
                return await message.reply_text(_["cplay_4"])
            channel = chat.title
        else:
            chat_id = message.chat.id
            channel = None

        video = None
        mystic = await message.reply_text(
            _["play_2"].format(channel) if channel else _["play_1"]
        )
        try:
            await stream(
                _,
                mystic,
                message.from_user.id,
                RADIO_URL,
                chat_id,
                message.from_user.mention,
                message.chat.id,
                video=video,
                stream_type="index",
            )
        except Exception as e:
            ex_type = type(e).__name__
            err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
            return await mystic.edit_text(err)
        return await play_logs(message, stream_type="M3u8 or Index Link")
    else:
        await message.reply(
            f"📻 𝗗𝗶𝗳𝗶𝘁𝗲 𝘂𝗺 𝗻𝗼𝗺𝗲 𝗱𝗲 𝗲𝘀𝘁𝗮𝗰̧𝗮̃𝗼 𝗽𝗮𝗿𝗮 𝘁𝗼𝗰𝗮𝗿 𝗿𝗮́𝗱𝗶𝗼.\n📋 𝗔𝗯𝗮𝗶𝘅𝗼 𝗲𝘀𝘁𝗮̃𝗼 𝗮𝗹𝗴𝘂𝗻𝘀 𝗻𝗼𝗺𝗲𝘀 𝗱𝗲 𝗲𝘀𝘁𝗮𝗰̧𝗼̃𝗲𝘀:\n{valid_stations}"
        )
