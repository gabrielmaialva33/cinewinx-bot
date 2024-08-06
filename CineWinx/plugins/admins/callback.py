import logging
import random

from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, CallbackQuery

from CineWinx import YouTube, app
from CineWinx.core.call import CineWinx
from CineWinx.misc import SUDOERS, db
from CineWinx.utils.database import (
    is_active_chat,
    is_music_playing,
    is_muted,
    is_nonadmin_chat,
    music_off,
    music_on,
    mute_off,
    mute_on,
    set_loop,
)
from CineWinx.utils.decorators.language import language_cb
from CineWinx.utils.formatters import seconds_to_min
from CineWinx.utils.inline.play import stream_markup, telegram_markup
from CineWinx.utils.stream.autoclear import auto_clean
from CineWinx.utils.thumbnails import gen_thumb
from config import (
    BANNED_USERS,
    SOUNCLOUD_IMG_URL,
    STREAM_IMG_URL,
    TELEGRAM_AUDIO_URL,
    TELEGRAM_VIDEO_URL,
    adminlist,
    SUPPORT_GROUP,
)

wrong = {}
down_vote = {}
down_voters = {}


@app.on_callback_query(filters.regex("ADMIN") & ~BANNED_USERS)
@language_cb
async def del_back_playlist(_client: Client, callback_query: CallbackQuery, _):
    callback_data = callback_query.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    command, chat = callback_request.split("|")
    chat_id = int(chat)
    if not await is_active_chat(chat_id):
        return await callback_query.answer(_["general_6"], show_alert=True)
    mention = callback_query.from_user.mention
    is_non_admin = await is_nonadmin_chat(callback_query.message.chat.id)
    if not is_non_admin:
        if callback_query.from_user.id not in SUDOERS:
            admins = adminlist.get(callback_query.message.chat.id)
            if not admins:
                return await callback_query.answer(_["admin_18"], show_alert=True)
            else:
                if callback_query.from_user.id not in admins:
                    return await callback_query.answer(_["admin_19"], show_alert=True)
    if command == "Pause":
        if not await is_music_playing(chat_id):
            return await callback_query.answer(_["admin_1"], show_alert=True)
        await callback_query.answer()
        await music_off(chat_id)
        await CineWinx.pause_stream(chat_id)
        await callback_query.message.reply_text(
            _["admin_2"].format(mention), disable_web_page_preview=True
        )
    elif command == "Resume":
        if await is_music_playing(chat_id):
            return await callback_query.answer(_["admin_3"], show_alert=True)
        await callback_query.answer()
        await music_on(chat_id)
        await CineWinx.resume_stream(chat_id)
        await callback_query.message.reply_text(
            _["admin_4"].format(mention), disable_web_page_preview=True
        )
    elif command == "Stop" or command == "End":
        await callback_query.answer()
        await CineWinx.stop_stream(chat_id)
        await set_loop(chat_id, 0)
        await callback_query.message.reply_text(
            _["admin_9"].format(mention), disable_web_page_preview=True
        )
    elif command == "Mute":
        if await is_muted(chat_id):
            return await callback_query.answer(_["admin_5"], show_alert=True)
        await callback_query.answer()
        await mute_on(chat_id)
        await CineWinx.mute_stream(chat_id)
        await callback_query.message.reply_text(
            _["admin_6"].format(mention), disable_web_page_preview=True
        )
    elif command == "Unmute":
        if not await is_muted(chat_id):
            return await callback_query.answer(_["admin_7"], show_alert=True)
        await callback_query.answer()
        await mute_off(chat_id)
        await CineWinx.unmute_stream(chat_id)
        await callback_query.message.reply_text(
            _["admin_8"].format(mention), disable_web_page_preview=True
        )
    elif command == "Loop":
        await callback_query.answer()
        await set_loop(chat_id, 3)
        await callback_query.message.reply_text(_["admin_25"].format(mention, 3))

    elif command == "Shuffle":
        check = db.get(chat_id)
        if not check:
            return await callback_query.answer(_["admin_21"], show_alert=True)
        try:
            popped = check.pop(0)
        except IndexError as e:
            logging.error(e)
            return await callback_query.answer(_["admin_22"], show_alert=True)
        check = db.get(chat_id)
        if not check:
            check.insert(0, popped)
            return await callback_query.answer(_["admin_22"], show_alert=True)
        await callback_query.answer()
        random.shuffle(check)
        check.insert(0, popped)
        await callback_query.message.reply_text(
            _["admin_23"].format(mention), disable_web_page_preview=True
        )

    elif command == "Skip":
        check = db.get(chat_id)
        txt = f"música pulada por {mention} !"
        popped = None
        try:
            popped = check.pop(0)
            if popped:
                await auto_clean(popped)
            if not check:
                await callback_query.edit_message_text(f"música pulada por {mention} !")
                await callback_query.message.reply_text(
                    _["admin_10"].format(mention), disable_web_page_preview=True
                )
                try:
                    return await CineWinx.stop_stream(chat_id)
                except Exception as e:
                    logging.error(e)
                    return
        except Exception as e:
            logging.error(e)
            try:
                await callback_query.edit_message_text(f"música pulada por {mention} !")
                await callback_query.message.reply_text(
                    _["admin_10"].format(mention), disable_web_page_preview=True
                )
                return await CineWinx.stop_stream(chat_id)
            except Exception as e:
                logging.error(e)
                return
        await callback_query.answer()
        queued = check[0]["file"]
        title = (check[0]["title"]).title()
        user = check[0]["by"]
        streamtype = check[0]["streamtype"]
        videoid = check[0]["vidid"]
        duration_min = check[0]["dur"]
        callback_query.message.from_user.id
        status = True if str(streamtype) == "video" else None
        db[chat_id][0]["played"] = 0
        if "live_" in queued:
            n, link = await YouTube.video(videoid, True)
            if n == 0:
                return await callback_query.message.reply_text(
                    _["admin_11"].format(title)
                )
            try:
                await CineWinx.skip_stream(chat_id, link, video=status)
            except Exception as e:
                logging.error(e)
                return await callback_query.message.reply_text(_["call_7"])
            button = telegram_markup(_, chat_id)
            img = await gen_thumb(videoid)
            run = await callback_query.message.reply_photo(
                photo=img,
                caption=_["stream_1"].format(
                    user,
                    f"https://t.me/{app.username}?start=info_{videoid}",
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
            await callback_query.edit_message_text(txt)
        elif "vid_" in queued:
            mystic = await callback_query.message.reply_text(
                _["call_8"], disable_web_page_preview=True
            )
            try:
                file_path, direct = await YouTube.download(
                    videoid,
                    mystic,
                    videoid=True,
                    video=status,
                )
            except:
                return await mystic.edit_text(_["call_7"])
            try:
                await CineWinx.skip_stream(chat_id, file_path, video=status)
            except Exception:
                return await mystic.edit_text(_["call_7"])
            button = stream_markup(_, videoid, chat_id)
            img = await gen_thumb(videoid)
            run = await callback_query.message.reply_photo(
                photo=img,
                caption=_["stream_1"].format(
                    title[:27],
                    f"https://t.me/{app.username}?start=info_{videoid}",
                    duration_min,
                    user,
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"
            await callback_query.edit_message_text(txt)
            await mystic.delete()
        elif "index_" in queued:
            try:
                await CineWinx.skip_stream(chat_id, videoid, video=status)
            except Exception:
                return await callback_query.message.reply_text(_["call_7"])
            button = telegram_markup(_, chat_id)
            run = await callback_query.message.reply_photo(
                photo=STREAM_IMG_URL,
                caption=_["stream_2"].format(user),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
            await callback_query.edit_message_text(txt)
        else:
            try:
                await CineWinx.skip_stream(chat_id, queued, video=status)
            except Exception:
                return await callback_query.message.reply_text(_["call_7"])
            if videoid == "telegram":
                button = telegram_markup(_, chat_id)
                run = await callback_query.message.reply_photo(
                    photo=(
                        TELEGRAM_AUDIO_URL
                        if str(streamtype) == "audio"
                        else TELEGRAM_VIDEO_URL
                    ),
                    caption=_["stream_1"].format(
                        title, SUPPORT_GROUP, check[0]["dur"], user
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            elif videoid == "soundcloud":
                button = telegram_markup(_, chat_id)
                run = await callback_query.message.reply_photo(
                    photo=(
                        SOUNCLOUD_IMG_URL
                        if str(streamtype) == "audio"
                        else TELEGRAM_VIDEO_URL
                    ),
                    caption=_["stream_1"].format(
                        title, SUPPORT_GROUP, check[0]["dur"], user
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            else:
                button = stream_markup(_, videoid, chat_id)
                img = await gen_thumb(videoid)
                run = await callback_query.message.reply_photo(
                    photo=img,
                    caption=_["stream_1"].format(
                        title[:27],
                        f"https://t.me/{app.username}?start=info_{videoid}",
                        duration_min,
                        user,
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"
            await callback_query.edit_message_text(txt)
    else:
        playing = db.get(chat_id)
        if not playing:
            return await callback_query.answer(_["queue_2"], show_alert=True)
        duration_seconds = int(playing[0]["seconds"])
        if duration_seconds == 0:
            return await callback_query.answer(_["admin_30"], show_alert=True)
        file_path = playing[0]["file"]
        if "index_" in file_path or "live_" in file_path:
            return await callback_query.answer(_["admin_30"], show_alert=True)
        duration_played = int(playing[0]["played"])
        if int(command) in [1, 2]:
            duration_to_skip = 10
        else:
            duration_to_skip = 30
        duration = playing[0]["dur"]
        if int(command) in [1, 3]:
            if (duration_played - duration_to_skip) <= 10:
                bet = seconds_to_min(duration_played)
                return await callback_query.answer(
                    f"O bot não pode buscar porque a duração excede.\n\nAtualmente tocando: <b>{bet}</b> minutos de <b>{duration}</b> minutos.",
                    show_alert=True,
                )
            to_seek = duration_played - duration_to_skip + 1
        else:
            if (duration_seconds - (duration_played + duration_to_skip)) <= 10:
                bet = seconds_to_min(duration_played)
                return await callback_query.answer(
                    f"O bot não pode buscar porque a duração excede.\n\nAtualmente tocando: <b>{bet}</b> minutos de <b>{duration}</b> minutos.",
                    show_alert=True,
                )
            to_seek = duration_played + duration_to_skip + 1
        await callback_query.answer()
        mystic = await callback_query.message.reply_text(_["admin_32"])
        if "vid_" in file_path:
            n, file_path = await YouTube.video(playing[0]["vidid"], True)
            if n == 0:
                return await mystic.edit_text(_["admin_30"])
        try:
            await CineWinx.seek_stream(
                chat_id,
                file_path,
                seconds_to_min(to_seek),
                duration,
                playing[0]["streamtype"],
            )
        except:
            return await mystic.edit_text(_["admin_34"])
        if int(command) in [1, 3]:
            db[chat_id][0]["played"] -= duration_to_skip
        else:
            db[chat_id][0]["played"] += duration_to_skip
        string = _["admin_33"].format(seconds_to_min(to_seek))
        await mystic.edit_text(f"{string}\n\nAlterações feitas por: {mention} !")


__MODULE__ = "𝗔𝗱𝗺𝗶𝗻 👮‍"
__HELP__ = """<b>👮‍♂️ 𝗖𝗼𝗺𝗮𝗻𝗱𝗼𝘀 𝗱𝗲 𝗔𝗱𝗺𝗶𝗻 </b>

🔄 c significa tocar no canal.

⏸️ <code>/pause</code> ou <code>/cpause</code> - 𝗣𝗮𝘂𝘀𝗮 𝗮 𝗺𝘂́𝘀𝗶𝗰𝗮 𝗾𝘂𝗲 𝗲𝘀𝘁𝗮́ 𝘁𝗼𝗰𝗮𝗻𝗱𝗼.

▶️ <code>/resume</code> ou <code>/cresume</code> - 𝗥𝗲𝘁𝗼𝗺𝗮 𝗮 𝗺𝘂́𝘀𝗶𝗰𝗮 𝗾𝘂𝗲 𝗲𝘀𝘁𝗮𝘃𝗮 𝗽𝗮𝘂𝘀𝗮𝗱𝗮.

🔇 <code>/mute</code> ou <code>/cmute</code> - 𝗦𝗶𝗹𝗲𝗻𝗰𝗶𝗮 𝗮 𝗺𝘂́𝘀𝗶𝗰𝗮 𝗾𝘂𝗲 𝗲𝘀𝘁𝗮́ 𝘁𝗼𝗰𝗮𝗻𝗱𝗼.

🔊 <code>/unmute</code> ou <code>/cunmute</code> - 𝗔𝘁𝗶𝘃𝗮 𝗼 𝘀𝗼𝗺 𝗱𝗮 𝗺𝘂́𝘀𝗶𝗰𝗮 𝗾𝘂𝗲 𝗲𝘀𝘁𝗮𝘃𝗮 𝘀𝗶𝗹𝗲𝗻𝗰𝗶𝗮𝗱𝗮.

⏭️ <code>/skip</code> ou <code>/cskip</code> - 𝗣𝘂𝗹𝗮 𝗮 𝗺𝘂́𝘀𝗶𝗰𝗮 𝗾𝘂𝗲 𝗲𝘀𝘁𝗮́ 𝘁𝗼𝗰𝗮𝗻𝗱𝗼 𝗮𝘁𝘂𝗮𝗹𝗺𝗲𝗻𝘁𝗲.

⏹️ <code>/stop</code> ou <code>/cstop</code> - 𝗣𝗮𝗿𝗮 𝗮 𝗺𝘂́𝘀𝗶𝗰𝗮 𝗾𝘂𝗲 𝗲𝘀𝘁𝗮́ 𝘁𝗼𝗰𝗮𝗻𝗱𝗼.

🔀 <code>/shuffle</code> ou <code>/cshuffle</code> - 𝗘𝗺𝗯𝗮𝗿𝗮𝗹𝗵𝗮 𝗮𝗹𝗲𝗮𝘁𝗼𝗿𝗶𝗮𝗺𝗲𝗻𝘁𝗲 𝗮 𝗽𝗹𝗮𝘆𝗹𝗶𝘀𝘁 𝗻𝗮 𝗳𝗶𝗹𝗮.

⏩ <code>/seek</code> ou <code>/cseek</code> - 𝗔𝘃𝗮𝗻𝗰̧𝗮 𝗮 𝗺𝘂́𝘀𝗶𝗰𝗮 𝗽𝗮𝗿𝗮 𝗮 𝗱𝘂𝗿𝗮𝗰̧𝗮̃𝗼 𝗲𝘀𝗽𝗲𝗰𝗶𝗳𝗶𝗰𝗮𝗱𝗮.

⏪ <code>/seekback</code> ou <code>/cseekback</code> - 𝗥𝗲𝘁𝗿𝗼𝗰𝗲𝗱𝗲 𝗮 𝗺𝘂́𝘀𝗶𝗰𝗮 𝗽𝗮𝗿𝗮 𝗮 𝗱𝘂𝗿𝗮𝗰̧𝗮̃𝗼 𝗲𝘀𝗽𝗲𝗰𝗶𝗳𝗶𝗰𝗮𝗱𝗮.

🔄 <code>/reboot</code> - 𝗥𝗲𝗶𝗻𝗶𝗰𝗶𝗮 𝗼 𝗯𝗼𝘁 𝗽𝗮𝗿𝗮 𝗼 𝘀𝗲𝘂 𝗰𝗵𝗮𝘁.

<b><u>⏭️ 𝗣𝘂𝗹𝗮𝗿 𝗘𝘀𝗽𝗲𝗰𝗶́𝗳𝗶𝗰𝗼:</u></b>
<code>/skip</code> ou <code>/cskip</code> [𝗻𝘂́𝗺𝗲𝗿𝗼 (𝗲𝘅𝗲𝗺𝗽𝗹𝗼: 3)] 
    - ⏩ 𝗣𝘂𝗹𝗮 𝗮 𝗺𝘂́𝘀𝗶𝗰𝗮 𝗽𝗮𝗿𝗮 𝗼 𝗻𝘂́𝗺𝗲𝗿𝗼 𝗲𝘀𝗽𝗲𝗰𝗶𝗳𝗶𝗰𝗮𝗱𝗼 𝗻𝗮 𝗳𝗶𝗹𝗮. 𝗘𝘅𝗲𝗺𝗽𝗹𝗼: <code>/skip</code> 3 𝗶𝗿𝗮́ 𝗽𝘂𝗹𝗮𝗿 𝗽𝗮𝗿𝗮 𝗮 𝘁𝗲𝗿𝗰𝗲𝗶𝗿𝗮 𝗺𝘂́𝘀𝗶𝗰𝗮 𝗻𝗮 𝗳𝗶𝗹𝗮 𝗲 𝗶𝗴𝗻𝗼𝗿𝗮𝗿𝗮́ 𝗮𝘀 𝗺𝘂́𝘀𝗶𝗰𝗮𝘀 1 𝗲 2 𝗻𝗮 𝗳𝗶𝗹𝗮.

<b><u>🔁 𝗥𝗲𝗽𝗲𝘁𝗶𝗿 𝗥𝗲𝗽𝗿𝗼𝗱𝘂𝗰̧𝗮̃𝗼:</u></b>
<code>/loop</code> ou <code>/cloop</code> [𝗲𝗻𝗮𝗯𝗹𝗲/𝗱𝗶𝘀𝗮𝗯𝗹𝗲] 𝗼𝘂 [𝗻𝘂́𝗺𝗲𝗿𝗼𝘀 𝗲𝗻𝘁𝗿𝗲 1-10] 
    - 🔁 𝗤𝘂𝗮𝗻𝗱𝗼 𝗮𝘁𝗶𝘃𝗮𝗱𝗼, 𝗼 𝗯𝗼𝘁 𝗿𝗲𝗽𝗲𝘁𝗲 𝗮 𝗺𝘂́𝘀𝗶𝗰𝗮 𝗮𝘁𝘂𝗮𝗹 𝗲𝗻𝘁𝗿𝗲 1-10 𝘃𝗲𝘇𝗲𝘀 𝗻𝗼 𝗰𝗵𝗮𝘁 𝗱𝗲 𝘃𝗼𝘇. 𝗣𝗮𝗱𝗿𝗮̃𝗼 𝗲́ 10 𝘃𝗲𝘇𝗲𝘀.
"""
