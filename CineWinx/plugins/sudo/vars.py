import asyncio

from pyrogram import filters

import config
from CineWinx import app
from CineWinx.misc import SUDOERS
from CineWinx.utils.database.memorydatabase import get_video_limit
from CineWinx.utils.formatters import convert_bytes
from strings import get_command

VARS_COMMAND = get_command("VARS_COMMAND")


@app.on_message(filters.command(VARS_COMMAND) & SUDOERS)
async def varsFunc(_client: app, message):
    mystic = await message.reply_text("Buscando informações...")
    v_limit = await get_video_limit()
    up_r = f"[Repo]({config.UPSTREAM_REPO})"
    up_b = config.UPSTREAM_BRANCH
    auto_leave = config.AUTO_LEAVE_ASSISTANT_TIME
    yt_sleep = config.YOUTUBE_DOWNLOAD_EDIT_SLEEP
    tg_sleep = config.TELEGRAM_DOWNLOAD_EDIT_SLEEP
    playlist_limit = config.SERVER_PLAYLIST_LIMIT
    fetch_playlist = config.PLAYLIST_FETCH_LIMIT
    song = config.SONG_DOWNLOAD_DURATION
    play_duration = config.DURATION_LIMIT_MIN
    if config.AUTO_LEAVING_ASSISTANT == str(True):
        ass = "Yes"
    else:
        ass = "No"
    if config.PRIVATE_BOT_MODE == str(True):
        pvt = "Yes"
    else:
        pvt = "No"
    if not config.GITHUB_REPO:
        git = "No"
    else:
        git = f"[Repo]({config.GITHUB_REPO})"
    if not config.START_IMG_URL:
        start = "No"
    else:
        start = f"[Image]({config.START_IMG_URL})"
    if not config.SUPPORT_CHANNEL:
        s_c = "No"
    else:
        s_c = f"[Channel]({config.SUPPORT_CHANNEL})"
    if not config.SUPPORT_GROUP:
        s_g = "No"
    else:
        s_g = f"[Group]({config.SUPPORT_GROUP})"
    if not config.GIT_TOKEN:
        token = "No"
    else:
        token = "Yes"
    if not config.SPOTIFY_CLIENT_ID and not config.SPOTIFY_CLIENT_SECRET:
        sotify = "No"
    else:
        sotify = "Yes"
    owners = [str(ids) for ids in config.OWNER_ID]
    owner_id = " ,".join(owners)
    tg_aud = convert_bytes(config.TG_AUDIO_FILESIZE_LIMIT)
    tg_vid = convert_bytes(config.TG_VIDEO_FILESIZE_LIMIT)
    text = f"""<b>MUSIC BOT CONFIG:</b>

<b><u>Basic Vars:</u></b>
<code>DURATION_LIMIT</code> : <b>{play_duration} min</b>
<code>SONG_DOWNLOAD_DURATION_LIMIT</code> :<b> {song} min</b>
<code>OWNER_ID</code> : <b>{owner_id}</b>

<b><u>Custom Repo Vars:</u></b>
<code>UPSTREAM_REPO</code> : <b>{up_r}</b>
<code>UPSTREAM_BRANCH</code> : <b>{up_b}</b>
<code>GITHUB_REPO</code> :<b> {git}</b>
<code>GIT_TOKEN</code> :<b> {token}</b>


<b><u>Bot Vars:</u></b>
<code>AUTO_LEAVING_ASSISTANT</code> : <b>{ass}</b>
<code>ASSISTANT_LEAVE_TIME</code> : <b>{auto_leave} seconds</b>
<code>PRIVATE_BOT_MODE</code> : <b>{pvt}</b>
<code>YOUTUBE_EDIT_SLEEP</code> : <b>{yt_sleep} seconds</b>
<code>TELEGRAM_EDIT_SLEEP</code> :<b> {tg_sleep} seconds</b>
<code>VIDEO_STREAM_LIMIT</code> : <b>{v_limit} chats</b>
<code>SERVER_PLAYLIST_LIMIT</code> :<b> {playlist_limit}</b>
<code>PLAYLIST_FETCH_LIMIT</code> :<b> {fetch_playlist}</b>

<b><u>Spotify Vars:</u></b>
<code>SPOTIFY_CLIENT_ID</code> :<b> {sotify}</b>
<code>SPOTIFY_CLIENT_SECRET</code> : <b>{sotify}</b>

<b><u>Playsize Vars:</u></b>
<code>TG_AUDIO_FILESIZE_LIMIT</code> :<b> {tg_aud}</b>
<code>TG_VIDEO_FILESIZE_LIMIT</code> :<b> {tg_vid}</b>

<b><u>URL Vars:</u></b>
<code>SUPPORT_CHANNEL</code> : <b>{s_c}</b>
<code>SUPPORT_GROUP</code> : <b>{s_g}</b>
<code>START_IMG_URL</code> : <b>{start}</b>
"""
    await asyncio.sleep(1)

    await mystic.edit_text(text)
