import logging
import re

import requests
from pyrogram import filters, Client
from pyrogram.types import Message

from CineWinx import app
from config import LOG_GROUP_ID, PREFIXES, BANNED_USERS
from strings import get_command

IG_COMMAND = get_command("IG_COMMAND")


@app.on_message(filters.command(IG_COMMAND, PREFIXES) & ~BANNED_USERS)
async def download_instagram_video(_client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text(
            "📎 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝗮 𝗨𝗥𝗟 𝗱𝗼 𝗥𝗲𝗲𝗹 𝗱𝗼 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺 𝗮𝗽𝗼́𝘀 𝗼 𝗰𝗼𝗺𝗮𝗻𝗱𝗼."
        )
        return
    url = message.text.split()[1]
    if not re.match(
            re.compile(r"^(https?://)?(www\.)?(instagram\.com|instagr\.am)/.*$"), url
    ):
        return await message.reply_text(
            "⚠️ 𝗔 𝗨𝗥𝗟 𝗽𝗿𝗼𝘃𝗶𝗱𝗮 𝗻𝗮̃𝗼 𝗲́ 𝘂𝗺𝗮 𝗨𝗥𝗟 𝘃𝗮́𝗹𝗶𝗱𝗮 𝗱𝗼 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺. 😅"
        )
    a = await message.reply_text("⏳ 𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗮𝗻𝗱𝗼...")
    api_url = f"https://insta-dl.hazex.workers.dev/?url={url}"

    response = requests.get(api_url)
    try:
        result = response.json()
        data = result["result"]
    except Exception as e:
        f = f"❌ 𝗘𝗿𝗿𝗼𝗿:\n{e}"
        try:
            await a.edit(f)
        except Exception as e:
            logging.error(str(e))
            await message.reply_text(f)
            return await app.send_message(LOG_GROUP_ID, f)
        return await app.send_message(LOG_GROUP_ID, f)
    if not result["error"]:
        video_url = data["url"]
        duration = data["duration"]
        quality = data["quality"]
        type = data["extension"]
        size = data["formattedSize"]
        caption = (
            f"<b>⏱️ 𝗗𝘂𝗿𝗮𝗰̧𝗮̃𝗼:</b> {duration}\n"
            f"<b>📺 𝗤𝘂𝗮𝗹𝗶𝗱𝗮𝗱𝗲:</b> {quality}\n<b>📂 "
            f"𝗧𝗶𝗽𝗼:</b> {type}\n"
            f"<b>📦 𝗧𝗮𝗺𝗮𝗻𝗵𝗼:</b> {size}"
        )
        await a.delete()
        await message.reply_video(video_url, caption=caption)
    else:
        try:
            return await a.edit("❌ 𝗙𝗮𝗹𝗵𝗮 𝗻𝗮 𝗯𝗮𝗶𝘅𝗮𝗱𝗮 𝗱𝗼 𝗥𝗲𝗲𝗹.")
        except Exception as e:
            logging.error(str(e))
            return await message.reply_text("❌ 𝗙𝗮𝗹𝗵𝗮 𝗻𝗮 𝗯𝗮𝗶𝘅𝗮𝗱𝗮 𝗱𝗼 𝗥𝗲𝗲𝗹.")


__MODULE__ = "📽️ 𝗥𝗲𝗲𝗹"
__HELP__ = """
<b>📽️ 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗲𝗿 𝗱𝗲 𝗥𝗲𝗲𝗹 𝗱𝗼 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺:</b>

• <code>/ig [URL]</code>: 𝗕𝗮𝗶𝘅𝗮𝗿 𝗥𝗲𝗲𝗹𝘀 𝗱𝗼 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺. 📎 𝗣𝗿𝗼𝘃𝗶𝗱𝗲 𝗮 𝗨𝗥𝗟 𝗱𝗼 𝗥𝗲𝗲𝗹 𝗱𝗼 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺 𝗮𝗽𝗼́𝘀 𝗼 𝗰𝗼𝗺𝗮𝗻𝗱𝗼.
• <code>/instagram [URL]</code>: 𝗕𝗮𝗶𝘅𝗮𝗿 𝗥𝗲𝗲𝗹𝘀 𝗱𝗼 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺. 📎 𝗣𝗿𝗼𝘃𝗶𝗱𝗲 𝗮 𝗨𝗥𝗟 𝗱𝗼 𝗥𝗲𝗲𝗹 𝗱𝗼 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺 𝗮𝗽𝗼́𝘀 𝗼 𝗰𝗼𝗺𝗮𝗻𝗱𝗼.
• <code>/reel [URL]</code>: 𝗕𝗮𝗶𝘅𝗮𝗿 𝗥𝗲𝗲𝗹𝘀 𝗱𝗼 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺. 📎 𝗣𝗿𝗼𝘃𝗶𝗱𝗲 𝗮 𝗨𝗥𝗟 𝗱𝗼 𝗥𝗲𝗲𝗹 𝗱𝗼 𝗜𝗻𝘀𝘁𝗮𝗴𝗿𝗮𝗺 𝗮𝗽𝗼́𝘀 𝗼 𝗰𝗼𝗺𝗮𝗻𝗱𝗼.
"""
