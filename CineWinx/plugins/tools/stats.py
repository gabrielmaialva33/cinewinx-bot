import asyncio
import platform
from sys import version as pyver

import psutil
from ntgcalls import __version__ as ngtgver
from pyrogram import __version__ as pyrover
from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.errors import MessageIdInvalid
from pyrogram.types import CallbackQuery, InputMediaPhoto, Message
from pytgcalls.__version__ import __version__ as pytgver

import config
from CineWinx import YouTube, app
from CineWinx.core.userbot import assistants
from CineWinx.misc import SUDOERS, pymongodb
from CineWinx.plugins import ALL_MODULES
from CineWinx.utils.database import (
    get_global_tops,
    get_particulars,
    get_queries,
    get_served_chats,
    get_served_users,
    get_sudoers,
    get_top_chats,
    get_topp_users,
)
from CineWinx.utils.decorators.language import language, language_cb
from CineWinx.utils.inline.stats import (
    back_stats_buttons,
    back_stats_markup,
    get_stats_markup,
    overallback_stats_markup,
    stats_buttons,
    top_ten_stats_markup,
)
from config import BANNED_USERS, PREFIXES
from strings import get_command

loop = asyncio.get_running_loop()

# Commands
GSTATS_COMMAND = get_command("GSTATS_COMMAND")
STATS_COMMAND = get_command("STATS_COMMAND")


@app.on_message(filters.command(STATS_COMMAND, PREFIXES) & ~BANNED_USERS)
@language
async def stats_global(_client: app, message: Message, _):
    upl = stats_buttons(_, True if message.from_user.id in SUDOERS else False)
    await message.reply_photo(
        photo=config.STATS_IMG_URL,
        caption=_["gstats_11"],
        reply_markup=upl,
    )


@app.on_message(filters.command(GSTATS_COMMAND, PREFIXES) & ~BANNED_USERS)
@language
async def gstats_global(_client: app, message: Message, _):
    mystic = await message.reply_text(_["gstats_1"])
    stats = await get_global_tops()
    if not stats:
        await asyncio.sleep(1)
        return await mystic.edit(_["gstats_2"])

    def get_stats():
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
            return mystic.edit(_["gstats_2"])
        videoid = None
        co = None
        for vidid, count in list_arranged.items():
            if vidid == "telegram":
                continue
            else:
                videoid = vidid
                co = count
            break
        return videoid, co

    try:
        videoid, co = await loop.run_in_executor(None, get_stats)
    except Exception as e:
        print(e)
        return
    (
        title,
        duration_min,
        duration_sec,
        thumbnail,
        vidid,
    ) = await YouTube.details(videoid, True)
    title = title.title()
    final = (
        f"<b>🎶 𝗙𝗮𝗶𝘅𝗮𝘀 𝗺𝗮𝗶𝘀 𝘁𝗼𝗰𝗮𝗱𝗮𝘀</b> {app.mention}\n\n<b>🎵 𝗧𝗶́𝘁𝘂𝗹𝗼:</b> {title}\n\n<i>🎧 "
        f"𝗧𝗼𝗰𝗮𝗱𝗮𝘀 <b>{co}</b> 𝘃𝗲𝘇𝗲𝘀</i>"
    )
    upl = get_stats_markup(_, True if message.from_user.id in SUDOERS else False)
    try:
        await app.send_photo(
            message.chat.id,
            photo=thumbnail,
            caption=final,
            reply_markup=upl,
        )
    except FloodWait as e:
        await asyncio.sleep(e.value)
    await mystic.delete()


@app.on_callback_query(filters.regex("GetStatsNow") & ~BANNED_USERS)
@language_cb
async def top_users_ten(_client: app, callback_query: CallbackQuery, _):
    chat_id = callback_query.message.chat.id
    callback_data = callback_query.data.strip()
    what = callback_data.split(None, 1)[1]
    upl = back_stats_markup(_)
    try:
        await callback_query.answer()
    except FloodWait:
        pass
    mystic = await callback_query.edit_message_text(
        _["gstats_3"].format(
            f"𝗱𝗲 {callback_query.message.chat.title}" if what == "Here" else what
        )
    )
    if what == "Tracks":
        stats = await get_global_tops()
    elif what == "Chats":
        stats = await get_top_chats()
    elif what == "Users":
        stats = await get_topp_users()
    elif what == "Here":
        stats = await get_particulars(chat_id)
    if not stats:
        await asyncio.sleep(1)
        return await mystic.edit(_["gstats_2"], reply_markup=upl)
    queries = await get_queries()

    def get_stats():
        results = {}
        for i in stats:
            top_list = stats[i] if what in ["Chats", "Users"] else stats[i]["spot"]
            results[str(i)] = top_list
            list_arranged = dict(
                sorted(
                    results.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            )
        if not results:
            return mystic.edit(_["gstats_2"], reply_markup=upl)
        msg = ""
        limit = 0
        total_count = 0
        if what in ["Tracks", "Here"]:
            for items, count in list_arranged.items():
                total_count += count
                if limit == 10:
                    continue
                limit += 1
                details = stats.get(items)
                title = (details["title"][:35]).title()
                if items == "telegram":
                    msg += f"<a href='https://t.me/telegram'>🔗 𝗔𝗿𝗾𝘂𝗶𝘃𝗼𝘀 𝗲 á𝘂𝗱𝗶𝗼𝘀 𝗱𝗼 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺</a> <b>𝘁𝗼𝗰𝗮𝗱𝗼𝘀 {count} 𝘃𝗲𝘇𝗲𝘀</b>\n\n"
                else:
                    msg += (
                        f"🔗 <a href='https://www.youtube.com/watch?v={items}'>{title}</a> "
                        f"<b>𝗧𝗼𝗰𝗮𝗱𝗼𝘀 {count} 𝘃𝗲𝘇𝗲𝘀</b>\n\n"
                    )

            temp = (
                _["gstats_4"].format(
                    queries,
                    app.mention,
                    len(stats),
                    total_count,
                    limit,
                )
                if what == "Tracks"
                else _["gstats_7"].format(len(stats), total_count, limit)
            )
            msg = temp + msg
        return msg, list_arranged

    try:
        msg, list_arranged = await loop.run_in_executor(None, get_stats)
    except Exception as e:
        print(e)
        return
    limit = 0
    if what in ["Users", "Chats"]:
        for items, count in list_arranged.items():
            if limit == 10:
                break
            try:
                extract = (
                    (await app.get_users(items)).first_name
                    if what == "Users"
                    else (await app.get_chat(items)).title
                )
                if extract is None:
                    continue
                await asyncio.sleep(0.5)
            except:
                continue
            limit += 1
            msg += f"🔗 {extract} 𝗧𝗼𝗰𝗮𝗱𝗼 {count} 𝘃𝗲𝘇𝗲𝘀 𝗻𝗼 𝗯𝗼𝘁.\n\n"
        temp = (
            _["gstats_5"].format(limit, app.mention)
            if what == "Chats"
            else _["gstats_6"].format(limit, app.mention)
        )
        msg = temp + msg
    med = InputMediaPhoto(media=config.GLOBAL_IMG_URL, caption=msg)
    try:
        await callback_query.edit_message_media(media=med, reply_markup=upl)
    except MessageIdInvalid:
        await callback_query.message.reply_photo(
            photo=config.GLOBAL_IMG_URL, caption=msg, reply_markup=upl
        )


@app.on_callback_query(filters.regex("TopOverall") & ~BANNED_USERS)
@language_cb
async def overall_stats(_client: app, callback_query: CallbackQuery, _):
    callback_data = callback_query.data.strip()
    what = callback_data.split(None, 1)[1]
    if what != "s":
        upl = overallback_stats_markup(_)
    else:
        upl = back_stats_buttons(_)
    try:
        await callback_query.answer()
    except FloodWait:
        pass
    await callback_query.edit_message_text(_["gstats_8"])
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    total_queries = await get_queries()
    blocked = len(BANNED_USERS)
    sudoers = len(SUDOERS)
    mod = len(ALL_MODULES)
    assistant = len(assistants)
    playlist_limit = config.SERVER_PLAYLIST_LIMIT
    fetch_playlist = config.PLAYLIST_FETCH_LIMIT
    song = config.SONG_DOWNLOAD_DURATION
    play_duration = config.DURATION_LIMIT_MIN
    if config.AUTO_LEAVING_ASSISTANT == str(True):
        ass = "Yes"
    else:
        ass = "No"
    text = f"""<u><b>📊 𝗘𝘀𝘁𝗮𝘁𝗶́𝘀𝘁𝗶𝗰𝗮𝘀 𝗲 𝗜𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝗚𝗲𝗿𝗮𝗶𝘀:</b></u>

<b>📦 𝗠ó𝗱𝘂𝗹𝗼𝘀 𝗶𝗺𝗽𝗼𝗿𝘁𝗮𝗱𝗼𝘀:</b> {mod}
<b>💬 𝗖𝗵𝗮𝘁𝘀 𝗮𝘁𝗲𝗻𝗱𝗶𝗱𝗼𝘀:</b> {served_chats} 
<b>👥 𝗨𝘀𝘂á𝗿𝗶𝗼𝘀 𝗮𝘁𝗲𝗻𝗱𝗶𝗱𝗼𝘀:</b> {served_users} 
<b>🚫 𝗨𝘀𝘂á𝗿𝗶𝗼𝘀 𝗯𝗹𝗼𝗾𝘂𝗲𝗮𝗱𝗼𝘀:</b> {blocked} 
<b>🔧 𝗨𝘀𝘂á𝗿𝗶𝗼𝘀 𝘀𝘂𝗱𝗼:</b> {sudoers} 

<b>🔍 𝗧𝗼𝘁𝗮𝗹 𝗱𝗲 𝗰𝗼𝗻𝘀𝘂𝗹𝘁𝗮𝘀:</b> {total_queries} 
<b>🤖 𝗧𝗼𝘁𝗮𝗹 𝗱𝗲 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲𝘀:</b> {assistant}
<b>🔄 𝗔𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗱𝗲 𝘀á𝗶𝗱𝗮 𝗮𝘂𝘁𝗼𝗺á𝘁𝗶𝗰𝗮:</b> {ass}

<b>⏳ 𝗗𝘂𝗿𝗮𝗰̧𝗮̃𝗼 𝗱𝗲 𝗿𝗲𝗽𝗿𝗼𝗱𝘂𝗰̧𝗮̃𝗼:</b> {play_duration} m
<b>🎵 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗱𝗲 𝗺ú𝘀𝗶𝗰𝗮𝘀:</b> {song} m
<b>📋 𝗣𝗹𝗮𝘆𝗹𝗶𝘀𝘁 𝗱𝗼 𝘀𝗲𝗿𝘃𝗶𝗱𝗼𝗿:</b> {playlist_limit}
<b>▶️ 𝗥𝗲𝗽𝗿𝗼𝗱𝘂𝗰̧𝗮̃𝗼 𝗱𝗲 𝗽𝗹𝗮𝘆𝗹𝗶𝘀𝘁:</b> {fetch_playlist}"""

    med = InputMediaPhoto(media=config.STATS_IMG_URL, caption=text)
    try:
        await callback_query.edit_message_media(media=med, reply_markup=upl)
    except MessageIdInvalid:
        await callback_query.message.reply_photo(
            photo=config.STATS_IMG_URL, caption=text, reply_markup=upl
        )


@app.on_callback_query(filters.regex("bot_stats_sudo"))
@language_cb
async def overall_stats(_client: app, callback_query: CallbackQuery, _):
    if callback_query.from_user.id not in SUDOERS:
        return await callback_query.answer(
            "🔒 𝗦𝗼𝗺𝗲𝗻𝘁𝗲 𝗽𝗮𝗿𝗮 𝘂𝘀𝘂á𝗿𝗶𝗼𝘀 𝗦𝗨𝗗𝗢", show_alert=True
        )
    callback_data = callback_query.data.strip()
    what = callback_data.split(None, 1)[1]
    if what != "s":
        upl = overallback_stats_markup(_)
    else:
        upl = back_stats_buttons(_)
    try:
        await callback_query.answer()
    except FloodWait:
        pass
    await callback_query.edit_message_text(_["gstats_8"])
    sc = platform.system()
    p_core = psutil.cpu_count(logical=False)
    t_core = psutil.cpu_count(logical=True)
    ram = str(round(psutil.virtual_memory().total / (1024.0**3))) + " GB"
    try:
        cpu_freq = psutil.cpu_freq().current
        if cpu_freq >= 1000:
            cpu_freq = f"{round(cpu_freq / 1000, 2)}GHz"
        else:
            cpu_freq = f"{round(cpu_freq, 2)}MHz"
    except AttributeError:
        cpu_freq = "𝗡/𝗔"
    hdd = psutil.disk_usage("/")
    total = hdd.total / (1024.0**3)
    total = str(total)
    used = hdd.used / (1024.0**3)
    used = str(used)
    free = hdd.free / (1024.0**3)
    free = str(free)
    mod = len(ALL_MODULES)
    db = pymongodb
    call = db.command("dbstats")
    datasize = call["dataSize"] / 1024
    datasize = str(datasize)
    storage = call["storageSize"] / 1024
    objects = call["objects"]
    collections = call["collections"]

    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    total_queries = await get_queries()
    blocked = len(BANNED_USERS)
    sudoers = len(await get_sudoers())
    text = f"""<u><b>📊 𝗘𝘀𝘁𝗮𝘁𝗶́𝘀𝘁𝗶𝗰𝗮𝘀 𝗲 𝗜𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗼 𝗕𝗼𝘁:</b></u>

<b>📦 𝗠ó𝗱𝘂𝗹𝗼𝘀 𝗜𝗺𝗽𝗼𝗿𝘁𝗮𝗱𝗼𝘀:</b> {mod}
<b>🖥️ 𝗣𝗹𝗮𝘁𝗮𝗳𝗼𝗿𝗺𝗮:</b> {sc}
<b>💾 𝗥𝗔𝗠:</b> {ram}
<b>🧩 𝗡ú𝗰𝗹𝗲𝗼𝘀 𝗙𝗶́𝘀𝗶𝗰𝗼𝘀:</b> {p_core}
<b>🧩 𝗧𝗼𝘁𝗮𝗹 𝗱𝗲 𝗡ú𝗰𝗹𝗲𝗼𝘀:</b> {t_core}
<b>⚙️ 𝗙𝗿𝗲𝗾𝘂ê𝗻𝗰𝗶𝗮 𝗱𝗮 𝗖𝗣𝗨:</b> {cpu_freq}

<b>🐍 𝗣𝘆𝘁𝗵𝗼𝗻:</b> {pyver.split()[0]}
<b>🌐 𝗣𝘆𝗿𝗼𝗴𝗿𝗮𝗺:</b> {pyrover}
<b>📞 𝗣𝘆-𝗧𝗴𝗖𝗮𝗹𝗹𝘀:</b> {pytgver}
<b>📞 𝗡-𝗧𝗴𝗖𝗮𝗹𝗹𝘀:</b> {ngtgver}
<b>💽 𝗗𝗶𝘀𝗽𝗼𝗻𝗶́𝘃𝗲𝗹:</b> {total[:5]} GiB
<b>💽 𝗨𝘀𝗮𝗱𝗼:</b> {used[:4]} GiB
<b>💽 𝗥𝗲𝘀𝘁𝗮𝗻𝘁𝗲:</b> {free[:4]} GiB
<b>🗄️ 𝗗𝗮𝗱𝗼𝘀:</b> {datasize[:5]} MB

<b>💬 𝗖𝗵𝗮𝘁𝘀 𝗦𝗲𝗿𝘃𝗶𝗱𝗼𝘀:</b> {served_chats} 
<b>👥 𝗨𝘀𝘂á𝗿𝗶𝗼𝘀 𝗦𝗲𝗿𝘃𝗶𝗱𝗼𝘀:</b> {served_users} 
<b>🚫 𝗨𝘀𝘂á𝗿𝗶𝗼𝘀 𝗕𝗹𝗼𝗾𝘂𝗲𝗮𝗱𝗼𝘀:</b> {blocked} 
<b>🔧 𝗨𝘀𝘂á𝗿𝗶𝗼𝘀 𝗦𝘂𝗱𝗼:</b> {sudoers} 

<b>🗄️ 𝗔𝗿𝗺𝗮𝘇𝗲𝗻𝗮𝗺𝗲𝗻𝘁𝗼 𝗱𝗼 𝗕𝗗:</b> {storage} MB
<b>📂 𝗖𝗼𝗹𝗲çõ𝗲𝘀 𝗻𝗼 𝗕𝗗:</b> {collections}
<b>🔑 𝗖𝗵𝗮𝘃𝗲𝘀 𝗻𝗼 𝗕𝗗:</b> {objects}
<b>🔍 𝗖𝗼𝗻𝘀𝘂𝗹𝘁𝗮𝘀 𝗱𝗼 𝗕𝗼𝘁:</b> <code>{total_queries}</code>
"""

    med = InputMediaPhoto(media=config.STATS_IMG_URL, caption=text)
    try:
        await callback_query.edit_message_media(media=med, reply_markup=upl)
    except MessageIdInvalid:
        await callback_query.message.reply_photo(
            photo=config.STATS_IMG_URL, caption=text, reply_markup=upl
        )


@app.on_callback_query(
    filters.regex(pattern=r"^(TOPMARKUPGET|GETSTATS|GlobalStats)$") & ~BANNED_USERS
)
@language_cb
async def back_buttons(_client: app, callback_query: CallbackQuery, _):
    try:
        await callback_query.answer()
    except FloodWait:
        pass
    command = callback_query.matches[0].group(1)
    if command == "TOPMARKUPGET":
        upl = top_ten_stats_markup(_)
        med = InputMediaPhoto(
            media=config.GLOBAL_IMG_URL,
            caption=_["gstats_9"],
        )
        try:
            await callback_query.edit_message_media(media=med, reply_markup=upl)
        except MessageIdInvalid:
            await callback_query.message.reply_photo(
                photo=config.GLOBAL_IMG_URL,
                caption=_["gstats_9"],
                reply_markup=upl,
            )
    if command == "GlobalStats":
        upl = get_stats_markup(
            _,
            True if callback_query.from_user.id in SUDOERS else False,
        )
        med = InputMediaPhoto(
            media=config.GLOBAL_IMG_URL,
            caption=_["gstats_10"].format(app.mention),
        )
        try:
            await callback_query.edit_message_media(media=med, reply_markup=upl)
        except MessageIdInvalid:
            await callback_query.message.reply_photo(
                photo=config.GLOBAL_IMG_URL,
                caption=_["gstats_10"].format(app.mention),
                reply_markup=upl,
            )
    if command == "GETSTATS":
        upl = stats_buttons(
            _,
            True if callback_query.from_user.id in SUDOERS else False,
        )
        med = InputMediaPhoto(
            media=config.STATS_IMG_URL,
            caption=_["gstats_11"].format(app.mention),
        )
        try:
            await callback_query.edit_message_media(media=med, reply_markup=upl)
        except MessageIdInvalid:
            await callback_query.message.reply_photo(
                photo=config.STATS_IMG_URL,
                caption=_["gstats_11"].format(app.mention),
                reply_markup=upl,
            )
