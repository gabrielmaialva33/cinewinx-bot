import asyncio
import logging
import random
import string

from pyrogram import filters, Client
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardMarkup, InputMediaPhoto, Message, CallbackQuery
from pytgcalls.exceptions import NoActiveGroupCall

import config
from CineWinx import Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app
from CineWinx.core.call import CineWinx
from CineWinx.utils import seconds_to_min, time_to_seconds
from CineWinx.utils.channelplay import get_channeplay_cb
from CineWinx.utils.database import is_video_allowed
from CineWinx.utils.decorators.language import language_cb
from CineWinx.utils.decorators.play import play_wrapper
from CineWinx.utils.formatters import formats
from CineWinx.utils.inline.play import (
    livestream_markup,
    playlist_markup,
    slider_markup,
    track_markup,
)
from CineWinx.utils.inline.playlist import botplaylist_markup
from CineWinx.utils.logger import play_logs
from CineWinx.utils.stream.stream import stream
from config import BANNED_USERS, lyrical, PREFIXES
from strings import get_command, get_string

PLAY_COMMAND = get_command("PLAY_COMMAND")

_ = get_string(config.LANGUAGE)


@app.on_message(filters.command(PLAY_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS)
@play_wrapper
async def play_command(
    _client: app,
    message: Message,
    _,
    chat_id: int,
    video,
    channel,
    playmode,
    url,
    fplay,
):
    mystic = await message.reply_text(
        _["play_2"].format(channel) if channel else _["play_1"]
    )
    plist_id = None
    slider = None
    plist_type = None
    spotify = None
    user_id = message.from_user.id
    user_name = message.from_user.first_name
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
    if audio_telegram:
        if audio_telegram.file_size > config.TG_AUDIO_FILESIZE_LIMIT:
            return await mystic.edit_text(_["play_5"])
        duration_min = seconds_to_min(audio_telegram.duration)
        if audio_telegram.duration > config.DURATION_LIMIT:
            return await mystic.edit_text(
                _["play_6"].format(config.DURATION_LIMIT_MIN, duration_min)
            )
        file_path = await Telegram.get_filepath(audio=audio_telegram)
        if await Telegram.download(_, message, mystic, file_path):
            message_link = await Telegram.get_link(message)
            file_name = await Telegram.get_filename(audio_telegram, audio=True)
            dur = await Telegram.get_duration(audio_telegram)
            details = {
                "title": file_name,
                "link": message_link,
                "path": file_path,
                "dur": dur,
            }

            try:
                await stream(
                    _,
                    mystic,
                    user_id,
                    details,
                    chat_id,
                    user_name,
                    message.chat.id,
                    stream_type="telegram",
                    force_play=fplay,
                )
            except Exception as e:
                logging.error(e)
                ex_type = type(e).__name__
                err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
                return await mystic.edit_text(err)
            return await mystic.delete()
        return
    elif video_telegram:
        if not await is_video_allowed(message.chat.id):
            return await mystic.edit_text(_["play_3"])
        if message.reply_to_message.document:
            try:
                ext = video_telegram.file_name.split(".")[-1]
                if ext.lower() not in formats:
                    return await mystic.edit_text(
                        _["play_8"].format(f"{' | '.join(formats)}")
                    )
            except:
                return await mystic.edit_text(
                    _["play_8"].format(f"{' | '.join(formats)}")
                )
        if video_telegram.file_size > config.TG_VIDEO_FILESIZE_LIMIT:
            return await mystic.edit_text(_["play_9"])
        file_path = await Telegram.get_filepath(video=video_telegram)
        if await Telegram.download(_, message, mystic, file_path):
            message_link = await Telegram.get_link(message)
            file_name = await Telegram.get_filename(video_telegram)
            dur = await Telegram.get_duration(video_telegram)
            details = {
                "title": file_name,
                "link": message_link,
                "path": file_path,
                "dur": dur,
            }
            try:
                await stream(
                    _,
                    mystic,
                    user_id,
                    details,
                    chat_id,
                    user_name,
                    message.chat.id,
                    video=True,
                    stream_type="telegram",
                    force_play=fplay,
                )
            except Exception as e:
                logging.error(e)
                ex_type = type(e).__name__
                err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
                return await mystic.edit_text(err)
            return await mystic.delete()
        return
    elif url:
        if await YouTube.exists(url):
            if "playlist" in url:
                try:
                    details = await YouTube.playlist(
                        url,
                        config.PLAYLIST_FETCH_LIMIT,
                        message.from_user.id,
                    )
                except Exception as e:
                    print(e)
                    return await mystic.edit_text(_["play_3"])
                streamtype = "playlist"
                plist_type = "yt"
                if "&" in url:
                    plist_id = (url.split("=")[1]).split("&")[0]
                else:
                    plist_id = url.split("=")[1]
                img = config.PLAYLIST_IMG_URL
                cap = _["play_10"]
            elif "https://youtu.be" in url:
                videoid = url.split("/")[-1].split("?")[0]
                details, track_id = await YouTube.track(
                    f"https://www.youtube.com/watch?v={videoid}"
                )
                streamtype = "youtube"
                img = details["thumb"]
                cap = _["play_11"].format(
                    details["title"],
                    details["duration_min"],
                )
            else:
                try:
                    details, track_id = await YouTube.track(url)
                except Exception as e:
                    print(e)
                    return await mystic.edit_text(_["play_3"])
                streamtype = "youtube"
                img = details["thumb"]
                cap = _["play_11"].format(
                    details["title"],
                    details["duration_min"],
                )
        elif await Spotify.valid(url):
            spotify = True
            if not config.SPOTIFY_CLIENT_ID and not config.SPOTIFY_CLIENT_SECRET:
                return await mystic.edit_text(
                    "Este bot não pode reproduzir músicas e playlists do Spotify. "
                    "Por favor, entre em contato com meu dono e peça a ele para adicionar o reprodutor do Spotify."
                )
            if "track" in url:
                try:
                    details, track_id = await Spotify.track(url)
                except Exception:
                    return await mystic.edit_text(_["play_3"])
                streamtype = "youtube"
                img = details["thumb"]
                cap = _["play_11"].format(details["title"], details["duration_min"])
            elif "playlist" in url:
                try:
                    details, plist_id = await Spotify.playlist(url)
                except Exception:
                    return await mystic.edit_text(_["play_3"])
                streamtype = "playlist"
                plist_type = "spplay"
                img = config.SPOTIFY_PLAYLIST_IMG_URL
                cap = _["play_12"].format(message.from_user.first_name)
            elif "album" in url:
                try:
                    details, plist_id = await Spotify.album(url)
                except Exception:
                    return await mystic.edit_text(_["play_3"])
                streamtype = "playlist"
                plist_type = "spalbum"
                img = config.SPOTIFY_ALBUM_IMG_URL
                cap = _["play_12"].format(message.from_user.first_name)
            elif "artist" in url:
                try:
                    details, plist_id = await Spotify.artist(url)
                except Exception:
                    return await mystic.edit_text(_["play_3"])
                streamtype = "playlist"
                plist_type = "spartist"
                img = config.SPOTIFY_ARTIST_IMG_URL
                cap = _["play_12"].format(message.from_user.first_name)
            else:
                return await mystic.edit_text(_["play_17"])
        elif await Apple.valid(url):
            if "album" in url:
                try:
                    details, track_id = await Apple.track(url)
                except Exception:
                    return await mystic.edit_text(_["play_3"])
                streamtype = "youtube"
                img = details["thumb"]
                cap = _["play_11"].format(details["title"], details["duration_min"])
            elif "playlist" in url:
                spotify = True
                try:
                    details, plist_id = await Apple.playlist(url)
                except Exception:
                    return await mystic.edit_text(_["play_3"])
                streamtype = "playlist"
                plist_type = "apple"
                cap = _["play_13"].format(message.from_user.first_name)
                img = url
            else:
                return await mystic.edit_text(_["play_16"])
        elif await Resso.valid(url):
            try:
                details, track_id = await Resso.track(url)
            except Exception:
                return await mystic.edit_text(_["play_3"])
            streamtype = "youtube"
            img = details["thumb"]
            cap = _["play_11"].format(details["title"], details["duration_min"])
        elif await SoundCloud.valid(url):
            try:
                details, track_path = await SoundCloud.download(url)
            except Exception:
                return await mystic.edit_text(_["play_3"])
            duration_sec = details["duration_sec"]
            if duration_sec > config.DURATION_LIMIT:
                return await mystic.edit_text(
                    _["play_6"].format(
                        config.DURATION_LIMIT_MIN,
                        details["duration_min"],
                    )
                )
            try:
                await stream(
                    _,
                    mystic,
                    user_id,
                    details,
                    chat_id,
                    user_name,
                    message.chat.id,
                    stream_type="soundcloud",
                    force_play=fplay,
                )
            except Exception as e:
                logging.error(e)
                ex_type = type(e).__name__
                err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
                return await mystic.edit_text(err)
            return await mystic.delete()
        else:
            try:
                await CineWinx.stream_call(url)
            except NoActiveGroupCall:
                await mystic.edit_text(
                    "Ocorreu um erro no bot. Por favor, relate-o ao chat de suporte o mais breve possível."
                )
                return await app.send_message(
                    config.LOG_GROUP_ID,
                    "Por favor, ative o chat de vídeo para transmitir a URL.",
                )
            except Exception as e:
                logging.error(e)
                return await mystic.edit_text(_["general_3"].format(type(e).__name__))
            await mystic.edit_text(_["str_2"])
            try:
                await stream(
                    _,
                    mystic,
                    message.from_user.id,
                    url,
                    chat_id,
                    message.from_user.first_name,
                    message.chat.id,
                    video=video,
                    stream_type="index",
                    force_play=fplay,
                )
            except Exception as e:
                logging.error(e)
                ex_type = type(e).__name__
                err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
                return await mystic.edit_text(err)
            return await play_logs(message, stream_type="M3u8 or Index Link")
    else:
        if len(message.command) < 2:
            buttons = botplaylist_markup(_)
            return await mystic.edit_text(
                _["playlist_1"],
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        slider = True
        query = message.text.split(None, 1)[1]
        if "-v" in query:
            query = query.replace("-v", "")
        try:
            details, track_id = await YouTube.track(query)
        except Exception:
            return await mystic.edit_text(_["play_3"])
        streamtype = "youtube"
    if str(playmode) == "Direct":
        if not plist_type:
            if details["duration_min"]:
                duration_sec = time_to_seconds(details["duration_min"])
                if duration_sec > config.DURATION_LIMIT:
                    return await mystic.edit_text(
                        _["play_6"].format(
                            config.DURATION_LIMIT_MIN,
                            details["duration_min"],
                        )
                    )
            else:
                buttons = livestream_markup(
                    _,
                    track_id,
                    user_id,
                    "v" if video else "a",
                    "c" if channel else "g",
                    "f" if fplay else "d",
                )
                return await mystic.edit_text(
                    _["play_15"],
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
        try:
            await stream(
                _,
                mystic,
                user_id,
                details,
                chat_id,
                user_name,
                message.chat.id,
                video=video,
                stream_type=streamtype,
                spotify=spotify,
                force_play=fplay,
            )
        except Exception as e:
            logging.error(e)
            ex_type = type(e).__name__
            err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
            try:
                return await mystic.edit_text(err)
            except FloodWait as e:
                await asyncio.sleep(e.value)
        await mystic.delete()
        return await play_logs(message, stream_type=streamtype)
    else:
        if plist_type:
            ran_hash = "".join(
                random.choices(string.ascii_uppercase + string.digits, k=10)
            )
            lyrical[ran_hash] = plist_id
            buttons = playlist_markup(
                _,
                ran_hash,
                message.from_user.id,
                plist_type,
                "c" if channel else "g",
                "f" if fplay else "d",
            )
            await mystic.delete()
            await message.reply_photo(
                photo=img,
                caption=cap,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            return await play_logs(message, stream_type=f"Playlist : {plist_type}")
        else:
            if slider:
                buttons = slider_markup(
                    _,
                    track_id,
                    message.from_user.id,
                    query,
                    0,
                    "c" if channel else "g",
                    "f" if fplay else "d",
                )
                await mystic.delete()
                await message.reply_photo(
                    photo=details["thumb"],
                    caption=_["play_11"].format(
                        details["title"].title(),
                        details["duration_min"],
                    ),
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
                return await play_logs(message, stream_type=f"Searched on Youtube")
            else:
                buttons = track_markup(
                    _,
                    track_id,
                    message.from_user.id,
                    "c" if channel else "g",
                    "f" if fplay else "d",
                )
                await mystic.delete()
                await message.reply_photo(
                    photo=img,
                    caption=cap,
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
                return await play_logs(message, stream_type=f"URL Searched Inline")


@app.on_callback_query(filters.regex("MusicStream") & ~BANNED_USERS)
@language_cb
async def play_music(_client: Client, callback_query: CallbackQuery, _):
    callback_data = callback_query.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    vidid, user_id, mode, cplay, fplay = callback_request.split("|")
    if callback_query.from_user.id != int(user_id):
        try:
            return await callback_query.answer(_["playcb_1"], show_alert=True)
        except:
            return
    try:
        chat_id, channel = await get_channeplay_cb(_, cplay, callback_query)
    except:
        return
    user_name = callback_query.from_user.first_name
    try:
        await callback_query.message.delete()
        await callback_query.answer()
    except:
        pass
    mystic = await callback_query.message.reply_text(
        _["play_2"].format(channel) if channel else _["play_1"]
    )
    try:
        details, track_id = await YouTube.track(vidid, True)
    except Exception:
        return await mystic.edit_text(_["play_3"])
    if details["duration_min"]:
        duration_sec = time_to_seconds(details["duration_min"])
        if duration_sec > config.DURATION_LIMIT:
            return await mystic.edit_text(
                _["play_6"].format(config.DURATION_LIMIT_MIN, details["duration_min"])
            )
    else:
        buttons = livestream_markup(
            _,
            track_id,
            callback_query.from_user.id,
            mode,
            "c" if cplay == "c" else "g",
            "f" if fplay else "d",
        )
        return await mystic.edit_text(
            _["play_15"],
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    video = True if mode == "v" else None
    ffplay = True if fplay == "f" else None
    try:
        await stream(
            _,
            mystic,
            callback_query.from_user.id,
            details,
            chat_id,
            user_name,
            callback_query.message.chat.id,
            video,
            stream_type="youtube",
            force_play=ffplay,
        )
    except Exception as e:
        logging.error(e)
        ex_type = type(e).__name__
        err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
        return await mystic.edit_text(err)
    return await mystic.delete()


@app.on_callback_query(filters.regex("AnonymousAdmin") & ~BANNED_USERS)
async def anonymous_check(_client: Client, callback_query: CallbackQuery):
    try:
        await callback_query.answer(
            "Você é um administrador anônimo.\n\nVolte para sua conta de usuário para me usar.",
            show_alert=True,
        )
    except:
        return


@app.on_callback_query(filters.regex("WinxPlaylists") & ~BANNED_USERS)
@language_cb
async def play_playlists_command(_client: Client, callback_query: CallbackQuery, _):
    callback_data = callback_query.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    (
        videoid,
        user_id,
        ptype,
        mode,
        cplay,
        fplay,
    ) = callback_request.split("|")
    if callback_query.from_user.id != int(user_id):
        try:
            return await callback_query.answer(_["playcb_1"], show_alert=True)
        except:
            return
    try:
        chat_id, channel = await get_channeplay_cb(_, cplay, callback_query)
    except:
        return
    user_name = callback_query.from_user.first_name
    await callback_query.message.delete()
    try:
        await callback_query.answer()
    except:
        pass
    mystic = await callback_query.message.reply_text(
        _["play_2"].format(channel) if channel else _["play_1"]
    )
    videoid = lyrical.get(videoid)
    video = True if mode == "v" else None
    ffplay = True if fplay == "f" else None
    spotify = True
    if ptype == "yt":
        spotify = False
        try:
            result = await YouTube.playlist(
                videoid,
                config.PLAYLIST_FETCH_LIMIT,
                callback_query.from_user.id,
                True,
            )
        except Exception:
            return await mystic.edit_text(_["play_3"])
    if ptype == "spplay":
        try:
            result, spotify_id = await Spotify.playlist(videoid)
        except Exception:
            return await mystic.edit_text(_["play_3"])
    if ptype == "spalbum":
        try:
            result, spotify_id = await Spotify.album(videoid)
        except Exception:
            return await mystic.edit_text(_["play_3"])
    if ptype == "spartist":
        try:
            result, spotify_id = await Spotify.artist(videoid)
        except Exception:
            return await mystic.edit_text(_["play_3"])
    if ptype == "apple":
        try:
            result, apple_id = await Apple.playlist(videoid, True)
        except Exception:
            return await mystic.edit_text(_["play_3"])
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
            spotify=spotify,
            force_play=ffplay,
        )
    except Exception as e:
        logging.error(e)
        ex_type = type(e).__name__
        err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
        return await mystic.edit_text(err)
    return await mystic.delete()


@app.on_callback_query(filters.regex("slider") & ~BANNED_USERS)
@language_cb
async def slider_queries(_client: Client, callback_query: CallbackQuery, _):
    callback_data = callback_query.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    (
        what,
        rtype,
        query,
        user_id,
        cplay,
        fplay,
    ) = callback_request.split("|")
    if callback_query.from_user.id != int(user_id):
        try:
            return await callback_query.answer(_["playcb_1"], show_alert=True)
        except:
            return
    what = str(what)
    rtype = int(rtype)
    if what == "F":
        if rtype == 9:
            query_type = 0
        else:
            query_type = int(rtype + 1)
        try:
            await callback_query.answer(_["playcb_2"])
        except:
            pass
        title, duration_min, thumbnail, vidid = await YouTube.slider(query, query_type)
        buttons = slider_markup(_, vidid, user_id, query, query_type, cplay, fplay)
        med = InputMediaPhoto(
            media=thumbnail,
            caption=_["play_11"].format(
                title.title(),
                duration_min,
            ),
        )
        return await callback_query.edit_message_media(
            media=med, reply_markup=InlineKeyboardMarkup(buttons)
        )
    if what == "B":
        if rtype == 0:
            query_type = 9
        else:
            query_type = int(rtype - 1)
        try:
            await callback_query.answer(_["playcb_2"])
        except:
            pass
        title, duration_min, thumbnail, vidid = await YouTube.slider(query, query_type)
        buttons = slider_markup(_, vidid, user_id, query, query_type, cplay, fplay)
        med = InputMediaPhoto(
            media=thumbnail,
            caption=_["play_11"].format(
                title.title(),
                duration_min,
            ),
        )
        return await callback_query.edit_message_media(
            media=med, reply_markup=InlineKeyboardMarkup(buttons)
        )


__MODULE__ = "𝗣𝗹𝗮𝘆 ▶️"
__HELP__ = """
✅ <u>𝗖𝗼𝗺𝗮𝗻𝗱𝗼𝘀 𝗱𝗲 𝗥𝗲𝗽𝗿𝗼𝗱𝘂𝗰̧𝗮̃𝗼:</u>\n

🎵 𝗖𝗼𝗺𝗮𝗻𝗱𝗼𝘀 𝗗𝗶𝘀𝗽𝗼𝗻𝗶́𝘃𝗲𝗶𝘀 = <code>play</code>, <code>vplay</code>, <code>cplay</code>

🔥 𝗖𝗼𝗺𝗮𝗻𝗱𝗼𝘀 𝗱𝗲 𝗥𝗲𝗽𝗿𝗼𝗱𝘂𝗰̧𝗮̃𝗼 𝗙𝗼𝗿𝗰̧𝗮𝗱𝗮 = <code>playforce</code>, <code>vplayforce</code>, <code>cplayforce</code>

🔄 c significa tocar no canal.
🎥 v significa tocar vídeo.
🚀 force significa reprodução forçada.

▶️ <code>/play</code> ou <code>/vplay</code> ou <code>/cplay</code> - 𝗢 𝗯𝗼𝘁 𝗰𝗼𝗺𝗲𝗰̧𝗮𝗿𝗮́ 𝗮 𝘁𝗼𝗰𝗮𝗿 𝘀𝘂𝗮 𝗰𝗼𝗻𝘀𝘂𝗹𝘁𝗮 𝗻𝗼 𝗰𝗵𝗮𝘁 𝗱𝗲 𝘃𝗼𝘇 𝗼𝘂 𝘁𝗿𝗮𝗻𝘀𝗺𝗶𝘁𝗶𝗿𝗮́ 𝗹𝗶𝗻𝗸𝘀 𝗮𝗼 𝘃𝗶𝘃𝗼 𝗻𝗼𝘀 𝗰𝗵𝗮𝘁𝘀 𝗱𝗲 𝘃𝗼𝘇.
🔊 <code>/playforce</code> ou <code>/vplayforce</code> ou <code>/cplayforce</code> - 𝗔 𝗥𝗲𝗽𝗿𝗼𝗱𝘂𝗰̧𝗮̃𝗼 𝗙𝗼𝗿𝗰𝗮𝗱𝗮 𝗶𝗻𝘁𝗲𝗿𝗿𝗼𝗺𝗽𝗲 𝗮 𝗳𝗮𝗶𝘅𝗮 𝗾𝘂𝗲 𝗲𝘀𝘁𝗮́ 𝘁𝗼𝗰𝗮𝗻𝗱𝗼 𝗻𝗼 𝗰𝗵𝗮𝘁 𝗱𝗲 𝘃𝗼𝘇 𝗲 𝗰𝗼𝗺𝗲𝗰̧𝗮 𝗮 𝘁𝗼𝗰𝗮𝗿 𝗮 𝗳𝗮𝗶𝘅𝗮 𝗽𝗲𝘀𝗾𝘂𝗶𝘀𝗮𝗱𝗮 𝗶𝗻𝘀𝘁𝗮𝗻𝘁𝗮𝗻𝗲𝗮𝗺𝗲𝗻𝘁𝗲, 𝘀𝗲𝗺 𝗽𝗲𝗿𝘁𝘂𝗿𝗯𝗮𝗿/𝗹𝗶𝗺𝗽𝗮𝗿 𝗮 𝗳𝗶𝗹𝗮.
🔗 <code>/channelplay</code> [𝗡𝗼𝗺𝗲 𝗱𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗼𝘂 𝗜𝗗 𝗱𝗼 𝗰𝗵𝗮𝘁] ou [𝗗𝗲𝘀𝗮𝘁𝗶𝘃𝗮𝗿] - 𝗖𝗼𝗻𝗲𝗰𝘁𝗲 𝗼 𝗰𝗮𝗻𝗮𝗹 𝗮 𝘂𝗺 𝗴𝗿𝘂𝗽𝗼 𝗲 𝘁𝗿𝗮𝗻𝘀𝗺𝗶𝘁𝗮 𝗺𝘂́𝘀𝗶𝗰𝗮 𝗻𝗼 𝗰𝗵𝗮𝘁 𝗱𝗲 𝘃𝗼𝘇 𝗱𝗼 𝗰𝗮𝗻𝗮𝗹 𝗮 𝗽𝗮𝗿𝘁𝗶𝗿 𝗱𝗼 𝘀𝗲𝘂 𝗴𝗿𝘂𝗽𝗼.
"""
