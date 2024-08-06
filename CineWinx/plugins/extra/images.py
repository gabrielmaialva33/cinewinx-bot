import os
import shutil
from re import findall

from bing_image_downloader import downloader
from pyrogram import Client, filters
from pyrogram.types import InputMediaPhoto, Message

from CineWinx import app
from config import PREFIXES, BANNED_USERS
from strings import get_command

IMAGE_COMMAND = get_command("IMAGE_COMMAND")


@app.on_message(filters.command(IMAGE_COMMAND, PREFIXES) & ~BANNED_USERS)
async def google_img_search(_client: Client, message: Message):
    chat_id = message.chat.id

    try:
        query = message.text.split(None, 1)[1]
    except IndexError:
        try:
            if message.reply_to_message:
                query = message.reply_to_message.text
            else:
                return await message.reply(
                    "🖼️ 𝗣𝗿𝗲𝗰𝗶𝘀𝗼 𝗱𝗲 𝘂𝗺 𝘁𝗲𝘅𝘁𝗼 𝗽𝗮𝗿𝗮 𝗯𝘂𝘀𝗰𝗮𝗿 𝗮 𝗶𝗺𝗮𝗴𝗲𝗺! 🔍"
                )
        except AttributeError:
            return await message.reply(
                "🖼️ 𝗣𝗿𝗲𝗰𝗶𝘀𝗼 𝗱𝗲 𝘂𝗺 𝘁𝗲𝘅𝘁𝗼 𝗽𝗮𝗿𝗮 𝗯𝘂𝘀𝗰𝗮𝗿 𝗮 𝗶𝗺𝗮𝗴𝗲𝗺! 🔍")

    lim = findall(r"lim=\d+", query)
    try:
        lim = int(lim[0].replace("lim=", ""))
        query = query.replace(f"lim={lim}", "")
    except IndexError:
        lim = 5  # limit to 5 images

    download_dir = "downloads"

    try:
        downloader.download(
            query,
            limit=lim,
            output_dir=download_dir,
            adult_filter_off=True,
            force_replace=False,
            timeout=60,
        )
        images_dir = os.path.join(download_dir, query)
        if not os.listdir(images_dir):
            raise Exception("🚫 𝗡𝗲𝗻𝗵𝘂𝗺𝗮 𝗶𝗺𝗮𝗴𝗲𝗺 𝗳𝗼𝗶 𝗯𝗮𝗶𝘅𝗮𝗱𝗮.")
        lst = [os.path.join(images_dir, img) for img in os.listdir(images_dir)][
              :lim
              ]  # ensure we only take the number of images specified by lim
    except Exception as e:
        return await message.reply(f"⚠️ 𝗘𝗿𝗿𝗼 𝗮𝗼 𝗯𝗮𝗶𝘅𝗮𝗿 𝗶𝗺𝗮𝗴𝗲𝗻𝘀: {e} ❗")

    msg = await message.reply("🔄 𝗖𝗼𝗹𝗲𝘁𝗮𝗻𝗱𝗼 𝗶𝗺𝗮𝗴𝗲𝗻𝘀...")

    count = 0
    for _ in lst:
        count += 1
        await msg.edit(f"🎉 𝗖𝗼𝗹𝗲𝘁𝗲𝗶 𝗮𝘀 𝗶𝗺𝗮𝗴𝗲𝗻𝘀 <b>{count}!</b> 📸")

    try:
        await app.send_media_group(
            chat_id=chat_id,
            media=[InputMediaPhoto(media=img) for img in lst],
            reply_to_message_id=message.id,
        )
        shutil.rmtree(images_dir)
        await msg.delete()
    except Exception as e:
        await msg.delete()
        return await message.reply(f"⚠️ 𝗘𝗿𝗿𝗼 𝗮𝗼 𝗲𝗻𝘃𝗶𝗮𝗿 𝗮𝘀 𝗶𝗺𝗮𝗴𝗲𝗻𝘀: {e} ❗")


__MODULE__ = "🖼️ 𝗜𝗺𝗮𝗴𝗲𝗻𝘀"
__HELP__ = """
<b>🖼️ 𝗕𝘂𝘀𝗰𝗮𝗿 𝗶𝗺𝗮𝗴𝗲𝗻𝘀:</b>

• <code>/img [𝗧𝗲𝘅𝘁𝗼]</code>: 𝗕𝘂𝘀𝗰𝗮𝗿 𝗶𝗺𝗮𝗴𝗲𝗻𝘀.
• <code>/image [𝗧𝗲𝘅𝘁𝗼]</code>: 𝗕𝘂𝘀𝗰𝗮𝗿 𝗶𝗺𝗮𝗴𝗲𝗻𝘀.
"""
