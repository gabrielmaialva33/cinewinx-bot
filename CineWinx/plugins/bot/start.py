import asyncio
import time

from pyrogram import filters, Client
from pyrogram.enums import ChatType, ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from youtubesearchpython.__future__ import VideosSearch

import config
from CineWinx import Telegram, YouTube, app
from CineWinx.misc import SUDOERS, _boot_
from CineWinx.plugins.play.playlist import del_plist_msg
from CineWinx.plugins.sudo.sudoers import sudoers_list
from CineWinx.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_assistant,
    get_lang,
    get_userss,
    is_on_off,
    is_served_private_chat,
)
from CineWinx.utils.decorators.language import language_start
from CineWinx.utils.formatters import get_readable_time
from CineWinx.utils.functions import MARKDOWN, WELCOMEHELP
from CineWinx.utils.inline import alive_panel, private_panel, start_pannel
from config import BANNED_USERS, START_IMG_URL
from config.config import OWNER_ID
from strings import get_string
from .help import help_parser

loop = asyncio.get_running_loop()


@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@language_start
async def start_comm(client: app, message: Message, _):
    chat_id = message.chat.id
    await add_served_user(message.from_user.id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = await help_parser(message.from_user.mention)
            if config.START_IMG_URL:
                return await message.reply_photo(
                    photo=START_IMG_URL,
                    caption=_["help_1"],
                    reply_markup=keyboard,
                )
            else:
                return await message.reply_text(
                    text=_["help_1"],
                    reply_markup=keyboard,
                )
        if name[0:4] == "song":
            await message.reply_text(_["song_2"])
            return
        if name == "mkdwn_help":
            await message.reply(
                MARKDOWN,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        if name == "greetings":
            await message.reply(
                WELCOMEHELP,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        if name[0:3] == "sta":
            m = await message.reply_text(
                "🔎 <i>𝗕𝘂𝘀𝗰𝗮𝗻𝗱𝗼 𝘀𝘂𝗮𝘀 𝗲𝘀𝘁𝗮𝘁𝗶́𝘀𝘁𝗶𝗰𝗮𝘀 𝗽𝗲𝘀𝘀𝗼𝗮𝗶𝘀.</i>"
            )
            stats = await get_userss(message.from_user.id)
            tot = len(stats)
            if not stats:
                await asyncio.sleep(1)
                return await m.edit(_["ustats_1"])

            def get_stats():
                msg = ""
                limit = 0
                results = {}
                for i in stats:
                    top_list = stats[i]["spot"]
                    results[str(i)] = top_list
                    list_arranged = dict(
                        sorted(
                            results.items(),
                            key=lambda item: item[1],
                            reverse=True,
                        )
                    )
                if not results:
                    return m.edit(_["ustats_1"])
                tota = 0
                videoid = None
                for vidid, count in list_arranged.items():
                    tota += count
                    if limit == 10:
                        continue
                    if limit == 0:
                        videoid = vidid
                    limit += 1
                    details = stats.get(vidid)
                    title = (details["title"][:35]).title()
                    if vidid == "telegram":
                        msg += (
                            f"🔗[Arquivos e áudios do Telegram]({config.SUPPORT_GROUP}) <b>tocados {count} vezes"
                            f"</b>\n\n"
                        )
                    else:
                        msg += f"🔗 <a href='https://www.youtube.com/watch?v={vidid}'>{title}</a> <b>tocado {count} vezes</b>\n\n"
                msg = _["ustats_2"].format(tot, tota, limit) + msg
                return videoid, msg

            try:
                videoid, msg = await loop.run_in_executor(None, get_stats)
            except Exception as e:
                print(e)
                return
            thumbnail = await YouTube.thumbnail(videoid, True)
            await m.delete()
            await message.reply_photo(photo=thumbnail, caption=msg)
            return
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            await asyncio.sleep(1)
            if await is_on_off(config.LOG):
                sender_id = message.from_user.id
                sender_mention = message.from_user.mention
                sender_name = message.from_user.first_name
                return await app.send_message(
                    config.LOG_GROUP_ID,
                    f"📢 {message.from_user.mention} 𝗮𝗰𝗮𝗯𝗼𝘂 𝗱𝗲 𝗶𝗻𝗶𝗰𝗶𝗮𝗿 𝗼 𝗯𝗼𝘁 𝗽𝗮𝗿𝗮 𝘃𝗲𝗿𝗶𝗳𝗶𝗰𝗮𝗿 𝗮 <code>sudolist</code>\n\n"
                    f"🆔 <b>𝗜𝗗:</b> {sender_id}\n"
                    f"👤 <b>𝗡𝗼𝗺𝗲:</b> {sender_name}\n"
                    f"📧 <b>𝗨𝘀𝘂𝗮́𝗿𝗶𝗼:</b> @{sender_mention}",
                )
            return
        if name[0:3] == "lyr":
            query = (str(name)).replace("lyrics_", "", 1)
            lyrical = config.lyrical
            lyrics = lyrical.get(query)
            if lyrics:
                await Telegram.send_split_text(message, lyrics)
                return
            else:
                await message.reply_text("𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗼𝗯𝘁𝗲𝗿 𝗮 𝗹𝗲𝘁𝗿𝗮 𝗱𝗮 𝗺𝘂́𝘀𝗶𝗰𝗮. 🎵")
                return
        if name[0:3] == "del":
            await del_plist_msg(client=client, message=message, _=_)
            await asyncio.sleep(1)
        if name[0:3] == "inf":
            m = await message.reply_text("🔎 𝗕𝘂𝘀𝗰𝗮𝗻𝗱𝗼 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀!")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
                searched_text = f"""
🔍<u><b>𝗜𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝘀𝗼𝗯𝗿𝗲 𝗮 𝗳𝗮𝗶𝘅𝗮 𝗱𝗲 𝘃𝗶́𝗱𝗲𝗼</b></u>

❇️<b>𝗧𝗶́𝘁𝘂𝗹𝗼:</b> {title}

⏳<b>𝗗𝘂𝗿𝗮𝗰̧𝗮̃𝗼:</b> {duration} minutos
👀<b>𝗩𝗶𝘀𝘂𝗮𝗹𝗶𝘇𝗮𝗰𝗼̃𝗲𝘀:</b> `{views}`
⏰<b>𝗣𝘂𝗯𝗹𝗶𝗰𝗮𝗱𝗼 𝗲𝗺:</b> {published}
🎥<b>𝗖𝗮𝗻𝗮𝗹:</b> {channel}
📎<b>𝗟𝗶𝗻𝗸 𝗱𝗼 𝗰𝗮𝗻𝗮𝗹:</b> <a href="{channellink}">veja aqui</a>
🔗<b>𝗟𝗶𝗻𝗸 𝗱𝗼 𝘃𝗶́𝗱𝗲𝗼:</b> <a href="{link}">link</a>
"""
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="🎥 𝗔𝘀𝘀𝗶𝘀𝘁𝗶𝗿", url=f"{link}"),
                        InlineKeyboardButton(text="❌ 𝗙𝗲𝗰𝗵𝗮𝗿", callback_data="close"),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=key,
            )
            await asyncio.sleep(1)
            if await is_on_off(config.LOG):
                sender_id = message.from_user.id
                sender_name = message.from_user.first_name
                sender_mention = message.from_user.mention
                return await app.send_message(
                    config.LOG_GROUP_ID,
                    f"📢 {message.from_user.mention} 𝗮𝗰𝗮𝗯𝗼𝘂 𝗱𝗲 𝗶𝗻𝗶𝗰𝗶𝗮𝗿 𝗼 𝗯𝗼𝘁 𝗽𝗮𝗿𝗮 𝘃𝗲𝗿𝗶𝗳𝗶𝗰𝗮𝗿 "
                    f"<code>𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗲 𝘃𝗶́𝗱𝗲𝗼</code>\n\n"
                    f"🆔 <b>𝗜𝗗:</b> {sender_id}\n"
                    f"👤 <b>𝗡𝗼𝗺𝗲:</b> {sender_name}\n"
                    f"📧 <b>𝗨𝘀𝘂𝗮́𝗿𝗶𝗼:</b> @{sender_mention}",
                )
    else:
        try:
            await app.resolve_peer(OWNER_ID[0])
            OWNER = OWNER_ID[0]
        except:
            OWNER = None
        out = private_panel(_, app.username, OWNER)
        if config.START_IMG_URL:
            try:
                await message.reply_photo(
                    photo=config.START_IMG_URL,
                    caption=_["start_1"].format(app.mention),
                    reply_markup=InlineKeyboardMarkup(out),
                )
            except:
                await message.reply_text(
                    text=_["start_1"].format(app.mention),
                    reply_markup=InlineKeyboardMarkup(out),
                )
        else:
            await message.reply_text(
                text=_["start_1"].format(app.mention),
                reply_markup=InlineKeyboardMarkup(out),
            )
        if await is_on_off(config.LOG):
            sender_id = message.from_user.id
            sender_name = message.from_user.first_name
            username = message.from_user.username
            return await app.send_message(
                config.LOG_GROUP_ID,
                f"📢 {message.from_user.mention} <b>𝗶𝗻𝗶𝗰𝗶𝗼𝘂 𝗼 𝗯𝗼𝘁. \n\n</b>"
                f"🆔 <b>𝗜𝗗:</b> <code>{sender_id}</code>\n"
                f"👤 <b>𝗡𝗼𝗺𝗲:</b> {sender_name}\n"
                f"📧 <b>𝗨𝘀𝘂𝗮́𝗿𝗶𝗼:</b> @{username}",
            )


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@language_start
async def testbot(client: Client, message: Message, _):
    out = alive_panel(_)
    uptime = int(time.time() - _boot_)
    if config.START_IMG_URL:
        me = await client.get_me()
        img = await client.download_media(me.photo.big_file_id)
        await message.reply_photo(
            photo=img,
            caption=_["start_7"].format(app.mention, get_readable_time(uptime)),
            reply_markup=InlineKeyboardMarkup(out),
        )
    else:
        await message.reply_text(
            text=_["start_7"].format(app.mention, get_readable_time(uptime)),
            reply_markup=InlineKeyboardMarkup(out),
        )
    return await add_served_chat(message.chat.id)


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(_client: app, message: Message):
    chat_id = message.chat.id
    if config.PRIVATE_BOT_MODE == str(True):
        if not await is_served_private_chat(message.chat.id):
            await message.reply_text(
                f"<b>🔒 𝗢 𝗺𝗼𝗱𝗼 𝗽𝗿𝗶𝘃𝗮𝗱𝗼 𝗱𝗲𝘀𝘁𝗲 𝗯𝗼𝘁 𝗳𝗼𝗶 𝗮𝘁𝗶𝘃𝗮𝗱𝗼.</b>\n\n"
                f"👤 𝗦𝗼𝗺𝗲𝗻𝘁𝗲 𝗺𝗲𝘂 𝗱𝗼𝗻𝗼 𝗽𝗼𝗱𝗲 𝘂𝘀𝗮́-𝗹𝗼.\n"
                f"📝 𝗦𝗲 𝘃𝗼𝗰𝗲̂ 𝗾𝘂𝗶𝘀𝗲𝗿 𝘂𝘀𝗮𝗿 𝗲𝘀𝘁𝗲 𝗯𝗼𝘁 𝗲𝗺 𝘀𝗲𝘂 𝗰𝗵𝗮𝘁, 𝗽𝗲𝗰̧𝗮 𝗮𝗼 𝗺𝗲𝘂 𝗱𝗼𝗻𝗼 𝗽𝗮𝗿𝗮 𝗮𝘂𝘁𝗼𝗿𝗶𝘇𝗮𝗿.\n"
                f"🆔 𝗜𝗗 𝗱𝗼 𝗰𝗵𝗮𝘁: <code>{chat_id}</code>\n"
            )
            return await app.leave_chat(message.chat.id)
    else:
        await add_served_chat(chat_id)
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if member.id == app.id:
                chat_type = message.chat.type
                if chat_type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_5"])
                    return await app.leave_chat(message.chat.id)
                if chat_id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_6"].format(
                            f"https://t.me/{app.username}?start=sudolist"
                        )
                    )
                    return await app.leave_chat(chat_id)
                userbot = await get_assistant(message.chat.id)
                out = start_pannel(_)
                await message.reply_text(
                    _["start_2"].format(
                        app.mention,
                        userbot.username,
                        userbot.id,
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
            if member.id in config.OWNER_ID:
                return await message.reply_text(
                    _["start_3"].format(app.mention, member.mention)
                )
            if member.id in SUDOERS:
                return await message.reply_text(
                    _["start_4"].format(app.mention, member.mention)
                )
            return
        except:
            return


__MODULE__ = "𝗕𝗼𝘁 🤖"
__HELP__ = """

🤖 <u><b>𝗕𝗼𝘁 𝗱𝗼 𝗚𝗿𝘂𝗽𝗼</b></u>

📊 <code>/stats</code> - 𝗢𝗯𝘁𝗲𝗻𝗵𝗮 𝗮𝘀 𝗲𝘀𝘁𝗮𝘁𝗶́𝘀𝘁𝗶𝗰𝗮𝘀 𝗴𝗹𝗼𝗯𝗮𝗶𝘀 𝗱𝗮𝘀 10 𝗺𝘂́𝘀𝗶𝗰𝗮𝘀 𝗺𝗮𝗶𝘀 𝘁𝗼𝗰𝗮𝗱𝗮𝘀, 𝗼𝘀 10 𝗽𝗿𝗶𝗻𝗰𝗶𝗽𝗮𝗶𝘀 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗱𝗼 𝗯𝗼𝘁, 𝗼𝘀 10 𝗽𝗿𝗶𝗻𝗰𝗶𝗽𝗮𝗶𝘀 𝗰𝗵𝗮𝘁𝘀 𝗻𝗼 𝗯𝗼𝘁, 𝗮𝘀 10 𝗺𝗮𝗶𝘀 𝘁𝗼𝗰𝗮𝗱𝗮𝘀 𝗲𝗺 𝘂𝗺 𝗰𝗵𝗮𝘁, 𝗲𝘁𝗰.

👮‍♂️ <code>/sudolist</code> - 𝗩𝗲𝗿𝗶𝗳𝗶𝗾𝘂𝗲 𝗼𝘀 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗰𝗼𝗺 𝗽𝗿𝗶𝘃𝗶𝗹𝗲́𝗴𝗶𝗼𝘀 𝗱𝗲 𝗮𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿 (𝘀𝘂𝗱𝗼) 𝗱𝗼 𝗯𝗼𝘁.

🎤 <code>/lyrics</code> [𝗡𝗼𝗺𝗲 𝗱𝗮 𝗺𝘂́𝘀𝗶𝗰𝗮] - 𝗕𝘂𝘀𝗰𝗮 𝗮 𝗹𝗲𝘁𝗿𝗮 𝗱𝗮 𝗺𝘂́𝘀𝗶𝗰𝗮 𝗲𝘀𝗽𝗲𝗰𝗶𝗳𝗶𝗰𝗮𝗱𝗮 𝗻𝗮 𝘄𝗲𝗯.

🎵 <code>/song</code> [𝗡𝗼𝗺𝗲 𝗱𝗮 𝗺𝘂́𝘀𝗶𝗰𝗮] 𝗼𝘂 [𝗟𝗶𝗻𝗸 𝗱𝗼 𝗬𝗼𝘂𝗧𝘂𝗯𝗲] - 𝗕𝗮𝗶𝘅𝗲 𝗾𝘂𝗮𝗹𝗾𝘂𝗲𝗿 𝗺𝘂́𝘀𝗶𝗰𝗮 𝗱𝗼 𝗬𝗼𝘂𝗧𝘂𝗯𝗲 𝗻𝗼𝘀 𝗳𝗼𝗿𝗺𝗮𝘁𝗼𝘀 𝗠𝗣𝟯 𝗼𝘂 𝗠𝗣𝟰.

🎛️ <code>/player</code> - 𝗢𝗯𝘁𝗲𝗻𝗵𝗮 𝘂𝗺 𝗽𝗮𝗶𝗻𝗲𝗹 𝗱𝗲 𝗿𝗲𝗽𝗿𝗼𝗱𝘂𝗰̧𝗮̃𝗼 𝗶𝗻𝘁𝗲𝗿𝗮𝘁𝗶𝘃𝗼.

🔄 c significa tocar no canal.

📋 <code>/queue</code> ou <code>/cqueue</code> - 𝗩𝗲𝗿𝗶𝗳𝗶𝗾𝘂𝗲 𝗮 𝗹𝗶𝘀𝘁𝗮 𝗱𝗲 𝗿𝗲𝗽𝗿𝗼𝗱𝘂𝗰̧𝗮̃𝗼 (𝗳𝗶𝗹𝗮) 𝗱𝗲 𝗺𝘂́𝘀𝗶𝗰𝗮𝘀.
"""
