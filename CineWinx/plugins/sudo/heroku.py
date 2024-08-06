import asyncio
import logging
import math
import os
import shutil
import socket
from datetime import datetime

import dotenv
import heroku3
import requests
import urllib3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from pyrogram import filters
from pyrogram.types import Message

import config
from CineWinx import app
from CineWinx.misc import HAPP, SUDOERS, XCB
from CineWinx.utils.database import (
    get_active_chats,
    remove_active_chat,
    remove_active_video_chat,
)
from CineWinx.utils.decorators.language import language
from CineWinx.utils.pastebin import winx_bin
from config import PREFIXES
from strings import get_command

GETLOG_COMMAND = get_command("GETLOG_COMMAND")
GETVAR_COMMAND = get_command("GETVAR_COMMAND")
DELVAR_COMMAND = get_command("DELVAR_COMMAND")
SETVAR_COMMAND = get_command("SETVAR_COMMAND")
USAGE_COMMAND = get_command("USAGE_COMMAND")
UPDATE_COMMAND = get_command("UPDATE_COMMAND")
RESTART_COMMAND = get_command("RESTART_COMMAND")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


async def is_heroku():
    return "heroku" in socket.getfqdn()


@app.on_message(filters.command(GETLOG_COMMAND, PREFIXES) & SUDOERS)
@language
async def log_(_client: app, message: Message, _):
    try:
        if await is_heroku():
            if HAPP is None:
                return await message.reply_text(_["heroku_1"])
            data = HAPP.get_log()
            link = await winx_bin(data)
            return await message.reply_text(link)
        else:
            if os.path.exists(config.LOG_FILE_NAME):
                log = open(config.LOG_FILE_NAME)
                lines = log.readlines()
                data = ""
                try:
                    numb = int(message.text.split(None, 1)[1])
                except IndexError:
                    numb = 100
                for x in lines[-numb:]:
                    data += x
                link = await winx_bin(data)
                return await message.reply_text(link)
            else:
                return await message.reply_text(_["heroku_2"])
    except Exception as e:
        print(e)
        await message.reply_text(_["heroku_2"])


@app.on_message(filters.command(GETVAR_COMMAND, PREFIXES) & SUDOERS)
@language
async def varget_(_client: app, message: Message, _):
    usage = _["heroku_3"]
    if len(message.command) != 2:
        return await message.reply_text(usage)
    check_var = message.text.split(None, 2)[1]
    if await is_heroku():
        if HAPP is None:
            return await message.reply_text(_["heroku_1"])
        heroku_config = HAPP.config()
        if check_var in heroku_config:
            return await message.reply_text(
                f"<b>{check_var}:</b> `{heroku_config[check_var]}`"
            )
        else:
            return await message.reply_text(_["heroku_4"])
    else:
        path = dotenv.find_dotenv()
        if not path:
            return await message.reply_text(_["heroku_5"])
        output = dotenv.get_key(path, check_var)
        if not output:
            await message.reply_text(_["heroku_4"])
        else:
            return await message.reply_text(f"<b>{check_var}:</b> `{str(output)}`")


@app.on_message(filters.command(DELVAR_COMMAND, PREFIXES) & SUDOERS)
@language
async def vardel_(_client: app, message: Message, _):
    usage = _["heroku_6"]
    if len(message.command) != 2:
        return await message.reply_text(usage)
    check_var = message.text.split(None, 2)[1]
    if await is_heroku():
        if HAPP is None:
            return await message.reply_text(_["heroku_1"])
        heroku_config = HAPP.config()
        if check_var in heroku_config:
            await message.reply_text(_["heroku_7"].format(check_var))
            del heroku_config[check_var]
        else:
            return await message.reply_text(_["heroku_4"])
    else:
        path = dotenv.find_dotenv()
        if not path:
            return await message.reply_text(_["heroku_5"])
        output = dotenv.unset_key(path, check_var)
        if not output[0]:
            return await message.reply_text(_["heroku_4"])
        else:
            await message.reply_text(_["heroku_7"].format(check_var))
            os.system(f"kill -9 {os.getpid()} && python3 -m CineWinx")


@app.on_message(filters.command(SETVAR_COMMAND, PREFIXES) & SUDOERS)
@language
async def set_var(_client: app, message: Message, _):
    usage = _["heroku_8"]
    if len(message.command) < 3:
        return await message.reply_text(usage)
    to_set = message.text.split(None, 2)[1].strip()
    value = message.text.split(None, 2)[2].strip()
    if await is_heroku():
        if HAPP is None:
            return await message.reply_text(_["heroku_1"])
        heroku_config = HAPP.config()
        if to_set in heroku_config:
            await message.reply_text(_["heroku_9"].format(to_set))
        else:
            await message.reply_text(_["heroku_10"].format(to_set))
        heroku_config[to_set] = value
    else:
        path = dotenv.find_dotenv()
        if not path:
            return await message.reply_text(_["heroku_5"])
        dotenv.set_key(path, to_set, value)
        if dotenv.get_key(path, to_set):
            await message.reply_text(_["heroku_9"].format(to_set))
        else:
            await message.reply_text(_["heroku_10"].format(to_set))
        os.system(f"kill -9 {os.getpid()} && python3 -m CineWinx")


@app.on_message(filters.command(USAGE_COMMAND, PREFIXES) & SUDOERS)
@language
async def usage_dynos(_client: app, message: Message, _):
    if await is_heroku():
        if HAPP is None:
            return await message.reply_text(_["heroku_1"])
    else:
        return await message.reply_text(_["heroku_11"])
    dyno = await message.reply_text(_["heroku_12"])
    Heroku = heroku3.from_key(config.HEROKU_API_KEY)
    account_id = Heroku.account().id
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Mobile Safari/537.36"
    )
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {config.HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + account_id + "/actions/get-quota"
    r = requests.get("https://api.heroku.com" + path, headers=headers)
    if r.status_code != 200:
        return await dyno.edit("Unable to fetch.")
    result = r.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)
    await asyncio.sleep(1.5)
    text = f"""
<b>📊 Dyno Usage 📊</b>

<b><u>⚙️ Usage:</u></b>
<b>Total used:</b> <code>{AppHours}</code>h <code>{AppMinutes}</code>m [<code>{AppPercentage}</code>%]

<b><u>🕒 Remaining quota:</u></b>
<b>Total left:</b> <code>{hours}</code>h <code>{minutes}</code>m [<code>{percentage}</code>%]
    """
    return await dyno.edit(text)


@app.on_message(filters.command(UPDATE_COMMAND, PREFIXES) & SUDOERS)
@language
async def update_(_client: app, message: Message, _):
    if await is_heroku():
        if HAPP is None:
            return await message.reply_text(_["heroku_1"])
    response = await message.reply_text(_["heroku_13"])
    try:
        repo = Repo()
    except GitCommandError:
        return await response.edit(_["heroku_14"])
    except InvalidGitRepositoryError:
        return await response.edit(_["heroku_15"])
    to_exc = f"git fetch origin {config.UPSTREAM_BRANCH} &> /dev/null"
    os.system(to_exc)
    await asyncio.sleep(7)
    verification = ""
    REPO_ = repo.remotes.origin.url.split(".git")[0]
    for checks in repo.iter_commits(f"HEAD..origin/{config.UPSTREAM_BRANCH}"):
        verification = str(checks.count())
    if verification == "":
        return await response.edit("✅ <b>𝗕𝗼𝘁 𝗶𝘀 𝘂𝗽-𝘁𝗼-𝗱𝗮𝘁𝗲.</b>")
    ordinal = lambda format: "%d%s" % (
        format,
        "tsnrhtdd"[(format // 10 % 10 != 1) * (format % 10 < 4) * format % 10 :: 4],
    )
    updates = "".join(
        f"<b>#{info.count()}: <a href={REPO_}/commit/{info}>{info.summary}</a> por -> {info.author}</b>\n\t\t\t\t<b>"
        f"commited on :</b> "
        f"{ordinal(int(datetime.fromtimestamp(info.committed_date).strftime('%d')))} "
        f"{datetime.fromtimestamp(info.committed_date).strftime('%b')}, "
        f"{datetime.fromtimestamp(info.committed_date).strftime('%Y')}\n\n"
        for info in repo.iter_commits(f"HEAD..origin/{config.UPSTREAM_BRANCH}")
    )
    _update_response_ = (
        "<b>🔔 A new update is available for the bot!</b>\n\n"
        "Pushing updates now\n\n<b><u>📦 Updates:</u></b>\n"
    )
    _final_updates_ = f"{_update_response_} {updates}"

    if len(_final_updates_) > 4096:
        url = await winx_bin(updates)
        nrs = await response.edit(
            f"<b>🔔 A new update is available for the bot!</b>\n\n"
            f"Pushing updates now\n\n<b><u>📦 Updates:</u></b>\n\n<a href='{url}'>Check updates</a>",
            disable_web_page_preview=True,
        )
    else:
        nrs = await response.edit(_final_updates_, disable_web_page_preview=True)
    os.system("git stash &> /dev/null && git pull")

    try:
        served_chats = await get_active_chats()
        for x in served_chats:
            try:
                await app.send_message(
                    chat_id=int(x),
                    text="{0} is updated herself\n\nYou can start playing again after 15-20 seconds.".format(
                        app.mention
                    ),
                )
                await remove_active_chat(x)
                await remove_active_video_chat(x)
            except:
                pass
        await response.edit(
            _final_updates_
            + "<b>🤖 Bot updated successfully!</b> Now wait for a few minutes until the bot restarts.",
            disable_web_page_preview=True,
        )
    except:
        pass

    if await is_heroku():
        try:
            os.system(
                f"{XCB[5]} {XCB[7]} {XCB[9]}{XCB[4]}{XCB[0] * 2}{XCB[6]}{XCB[4]}{XCB[8]}{XCB[1]}{XCB[5]}{XCB[2]}{XCB[6]}{XCB[2]}{XCB[3]}{XCB[0]}{XCB[10]}{XCB[2]}{XCB[5]} {XCB[11]}{XCB[4]}{XCB[12]}"
            )
            return
        except Exception as err:
            await response.edit(
                f"{nrs.text}\n\n<b>⚠️ Something went wrong, please check logs.</b>"
            )
            return await app.send_message(
                chat_id=config.LOG_GROUP_ID,
                text=f"⚠️ Uma exceção ocorreu no #atualizador devido a: <code>{err}</code>",
            )
    else:
        os.system("pip3 install --no-cache-dir -U -r requirements.txt")
        os.system(f"kill -9 {os.getpid()} && python3 -m CineWinx")
        exit()


@app.on_message(filters.command(RESTART_COMMAND, PREFIXES) & SUDOERS)
async def restart_(_, message: Message):
    response = await message.reply_text("🔄 𝗥𝗲𝗶𝗻𝗶𝗰𝗶𝗮𝗻𝗱𝗼...")
    ac_chats = await get_active_chats()
    for x in ac_chats:
        try:
            await app.send_message(
                chat_id=int(x),
                text=f"🔄 {app.mention} 𝗲𝘀𝘁𝗮́ 𝗿𝗲𝗶𝗻𝗶𝗰𝗶𝗮𝗻𝗱𝗼...\n\n𝗩𝗼𝗰𝗲̂ 𝗽𝗼𝗱𝗲𝗿𝗮́ "
                f"𝗿𝗲𝗽𝗿𝗼𝗱𝘂𝘇𝗶𝗿 𝗺𝘂́𝘀𝗶𝗰𝗮𝘀 𝗻𝗼𝘃𝗮𝗺𝗲𝗻𝘁𝗲 𝗲𝗺 𝟭𝟱-𝟮𝟬 𝘀𝗲𝗴𝘂𝗻𝗱𝗼𝘀.",
            )
            await remove_active_chat(x)
            await remove_active_video_chat(x)
        except Exception as e:
            logging.error(str(e))

    try:
        shutil.rmtree("downloads")
        shutil.rmtree("raw_files")
        shutil.rmtree("cache")
    except Exception as e:
        logging.error(str(e))
    await response.edit_text(
        "🔄 𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗼 𝗱𝗲 𝗿𝗲𝗶𝗻𝗶𝗰𝗶𝗮𝗹𝗶𝘇𝗮𝗰̧𝗮̃𝗼 𝗶𝗻𝗶𝗰𝗶𝗮𝗱𝗼, 𝗮𝗴𝘂𝗮𝗿𝗱𝗲 𝗮𝗹𝗴𝘂𝗻𝘀 𝘀𝗲𝗴𝘂𝗻𝗱𝗼𝘀 𝗮𝘁𝗲́ 𝗾𝘂𝗲 𝗼 𝗯𝗼𝘁 𝘀𝗲𝗷𝗮 𝗶𝗻𝗶𝗰𝗶𝗮𝗱𝗼..."
    )
    os.system(f"kill -9 {os.getpid()} && python3 -m CineWinx")


__MODULE__ = "𝗗𝗲𝘃 💻"
__HELP__ = """
🔰<u>𝗔𝗱𝗶𝗰𝗶𝗼𝗻𝗮𝗿 𝗲 𝗥𝗲𝗺𝗼𝘃𝗲𝗿 𝗨𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗦𝘂𝗱𝗼:</u>

• /addsudo [𝗻𝗼𝗺𝗲 𝗱𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗼𝘂 𝗿𝗲𝘀𝗽𝗼𝗻𝗱𝗲𝗿 𝗮 𝘂𝗺 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼]

• /delsudo [𝗻𝗼𝗺𝗲 𝗱𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗼𝘂 𝗿𝗲𝘀𝗽𝗼𝗻𝗱𝗲𝗿 𝗮 𝘂𝗺 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼]

🛃<u>𝗛𝗲𝗿𝗼𝗸𝘂:</u>

• /usage - 𝗨𝘀𝗼 𝗱𝗼 𝗗𝘆𝗻𝗼.

• /get_var - 𝗢𝗯𝘁𝗲𝗿 𝘂𝗺𝗮 𝘃𝗮𝗿𝗶𝗮́𝘃𝗲𝗹 𝗱𝗲 𝗰𝗼𝗻𝗳𝗶𝗴𝘂𝗿𝗮𝗰̧𝗮̃𝗼 𝗱𝗼 𝗛𝗲𝗿𝗼𝗸𝘂 𝗼𝘂 .env

• /del_var - 𝗘𝘅𝗰𝗹𝘂𝗶𝗿 𝗾𝘂𝗮𝗹𝗾𝘂𝗲𝗿 𝘃𝗮𝗿𝗶𝗮́𝘃𝗲𝗹 𝗻𝗼 𝗛𝗲𝗿𝗼𝗸𝘂 𝗼𝘂 .env.

• /set_var [𝗻𝗼𝗺𝗲 𝗱𝗮 𝘃𝗮𝗿𝗶𝗮́𝘃𝗲𝗹] [𝘃𝗮𝗹𝗼𝗿] - 𝗗𝗲𝗳𝗶𝗻𝗶𝗿 𝗼𝘂 𝗮𝘁𝘂𝗮𝗹𝗶𝘇𝗮𝗿 𝘂𝗺𝗮 𝘃𝗮𝗿𝗶𝗮́𝘃𝗲𝗹 𝗻𝗼 𝗛𝗲𝗿𝗼𝗸𝘂 𝗼𝘂 .env. 𝗦𝗲𝗽𝗮𝗿𝗲 𝗮 𝘃𝗮𝗿𝗶𝗮́𝘃𝗲𝗹 𝗲 𝘀𝗲𝘂 𝘃𝗮𝗹𝗼𝗿 𝗰𝗼𝗺 𝘂𝗺 𝗲𝘀𝗽𝗮𝗰̧𝗼.

🤖<u>𝗖𝗼𝗺𝗮𝗻𝗱𝗼𝘀 𝗱𝗼 𝗕𝗼𝘁:</u>

• /restart - 𝗥𝗲𝗶𝗻𝗶𝗰𝗶𝗮𝗿 𝘀𝗲𝘂 𝗕𝗼𝘁.

• /update, /gitpull - 𝗔𝘁𝘂𝗮𝗹𝗶𝘇𝗮𝗿 𝗼 𝗕𝗼𝘁.

• /speedtest - 𝗩𝗲𝗿𝗶𝗳𝗶𝗰𝗮𝗿 𝗮 𝘃𝗲𝗹𝗼𝗰𝗶𝗱𝗮𝗱𝗲 𝗱𝗼 𝘀𝗲𝗿𝘃𝗶𝗱𝗼𝗿.

• /maintenance [enable|disable] - 𝗠𝗼𝗱𝗼 𝗺𝗮𝗻𝘂𝘁𝗲𝗻𝗰̧𝗮̃𝗼.

• /logger [ativar|desativar] - 𝗢 𝗯𝗼𝘁 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗮 𝗮𝘀 𝗽𝗲𝘀𝗾𝘂𝗶𝘀𝗮𝘀 𝗻𝗼 𝗴𝗿𝘂𝗽𝗼 𝗱𝗲 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗼𝘀.

• /get_log [número de linhas] - 𝗢𝗯𝘁𝗲𝗿 𝗼 𝗿𝗲𝗴𝗶𝘀𝘁𝗿𝗼 𝗱𝗼 𝘀𝗲𝘂 𝗯𝗼𝘁 𝗱𝗼 𝗛𝗲𝗿𝗼𝗸𝘂 𝗼𝘂 𝗩𝗣𝗦. 𝗙𝘂𝗻𝗰𝗶𝗼𝗻𝗮 𝗽𝗮𝗿𝗮 𝗮𝗺𝗯𝗼𝘀.

• /autoend [enable|disable] - 𝗔𝘁𝗶𝘃𝗮𝗿 𝗼 𝗳𝗶𝗺 𝗮𝘂𝘁𝗼𝗺𝗮́𝘁𝗶𝗰𝗼 𝗱𝗮 𝘁𝗿𝗮𝗻𝘀𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗮𝗽𝗼́𝘀 𝟯 𝗺𝗶𝗻𝘂𝘁𝗼𝘀 𝘀𝗲 𝗻𝗶𝗻𝗴𝘂𝗲́𝗺 𝗲𝘀𝘁𝗶𝘃𝗲𝗿 𝗼𝘂𝘃𝗶𝗻𝗱𝗼.
"""
