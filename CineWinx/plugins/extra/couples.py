import logging
import os
import random
from datetime import datetime, timedelta

from PIL import Image, ImageDraw
from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegraph.aio import Telegraph

from CineWinx import app
from CineWinx.utils import save_couple, get_lovers_date
from CineWinx.utils.database.couples_db import get_image, save_pin, get_pin
from config import BANNED_USERS, PREFIXES
from strings import get_command

POLICE = [
    [
        InlineKeyboardButton(
            text="𝐂𝐈𝐍𝐄𝐖𝐈𝐍𝐗™",
            url="https://t.me/cinewinx",
        ),
    ],
]


def get_current_date():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M").split(" ")


def get_tomorrow_date():
    today = get_current_date()[0]
    day, month, year = map(int, today.split("/"))
    tomorrow = datetime(year, month, day) + timedelta(days=1)
    return tomorrow.strftime("%d/%m/%Y")


COUPLE_COMMAND = get_command("COUPLE_COMMAND")


@app.on_message(filters.command(COUPLE_COMMAND, PREFIXES) & ~BANNED_USERS)
async def couples_command(client: Client, message: Message):
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("🚫 𝗘𝘀𝘁𝗲 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 𝘀𝗼́ 𝗳𝘂𝗻𝗰𝗶𝗼𝗻𝗮 𝗲𝗺 𝗴𝗿𝘂𝗽𝗼𝘀.")

    chat_id = message.chat.id
    today = get_current_date()[0]
    tomorrow = get_tomorrow_date()

    try:
        is_selected = await get_lovers_date(chat_id, today)
        if not is_selected:
            msg = await message.reply_text("🖼️ 𝗚𝗲𝗿𝗮𝗻𝗱𝗼 𝗶𝗺𝗮𝗴𝗲𝗺 𝗱𝗼 𝗰𝗮𝘀𝗮𝗹 ...")
            list_of_users = []

            async for i in app.get_chat_members(message.chat.id, limit=50):
                if not i.user.is_bot:
                    list_of_users.append(i.user.id)

            c1_id, c2_id = random.sample(list_of_users, 2)

            photo1, photo2 = (await app.get_chat(c1_id)).photo, (
                await app.get_chat(c2_id)
            ).photo
            n1, n2 = (await app.get_users(c1_id)).mention, (
                await app.get_users(c2_id)
            ).mention

            p1 = (
                await app.download_media(photo1.big_file_id, file_name="pfp1.png")
                if photo1
                else "assets/u_pic.png"
            )
            p2 = (
                await app.download_media(photo2.big_file_id, file_name="pfp2.png")
                if photo2
                else "assets/u_pic.png"
            )

            create_couple_image(p1, p2, chat_id)

            t_graph = Telegraph()
            upload_path = await t_graph.upload_file(f"cache/couple_{chat_id}.png")
            image_url = "https://graph.org" + upload_path[0]["src"]

            pin_id = await send_couple_image(
                client, message, chat_id, n1, n2, today, tomorrow, msg
            )
            await save_couple(
                chat_id, today, {"c1_id": c1_id, "c2_id": c2_id}, image_url, pin_id
            )
        else:
            await send_existing_couple_image(client, message, chat_id, today, tomorrow)
    except Exception as e:
        logging.error(str(e))
    finally:
        cleanup_files(chat_id)


def create_couple_image(p1: str, p2: str, chat_id: int):
    img1, img2 = Image.open(p1), Image.open(p2)
    img1, img2 = img1.resize((380, 388)), img2.resize((380, 388))

    mask = Image.new("L", img1.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + img1.size, fill=255)
    img1.putalpha(mask)

    mask = Image.new("L", img2.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + img2.size, fill=255)
    img2.putalpha(mask)

    img = Image.open("assets/cppic.png")
    img.paste(img1, (120, 195), img1)
    img.paste(img2, (510, 195), img2)

    img.save(f"cache/couple_{chat_id}.png")


async def send_couple_image(
    client: Client,
    message: Message,
    chat_id: int,
    n1: str,
    n2: str,
    today: str,
    tomorrow: str,
    msg: Message,
):
    txt = f"""
💑 <b>𝗖𝗮𝘀𝗮𝗹 𝗱𝗼 𝗗𝗶𝗮 𝗱𝗲 𝗛𝗼𝗷𝗲:</b>

{n1} + {n2} = 💚💘

📅 <b>𝗢𝘀 𝗽𝗿𝗼́𝘅𝗶𝗺𝗼𝘀 𝗰𝗮𝘀𝗮𝗶𝘀 𝘀𝗲𝗿𝗮̃𝗼 𝘀𝗲𝗹𝗲𝗰𝗶𝗼𝗻𝗮𝗱𝗼𝘀 𝗲𝗺 {tomorrow} !</b>
"""
    await message.delete()
    await msg.delete()

    pin = await client.send_photo(
        chat_id=chat_id,
        photo=f"cache/couple_{chat_id}.png",
        caption=txt,
        reply_markup=InlineKeyboardMarkup(POLICE),
    )
    old_pin = await get_pin(chat_id)
    if old_pin is not None:
        try:
            await client.unpin_chat_message(chat_id, old_pin)
        except Exception as e:
            logging.error(str(e))

    await client.pin_chat_message(chat_id, pin.id)
    await save_pin(chat_id, pin.id)
    return pin.id


async def send_existing_couple_image(
    _client: Client, message: Message, chat_id: int, today: str, tomorrow: str
):
    msg = await message.reply_text("🖼️ 𝗚𝗲𝗿𝗮𝗻𝗱𝗼 𝗶𝗺𝗮𝗴𝗲𝗺 𝗱𝗼 𝗰𝗮𝘀𝗮𝗹 ...")
    image_url = await get_image(chat_id)
    couple_data = await get_lovers_date(chat_id, today)
    c1_id, c2_id = couple_data["c1_id"], couple_data["c2_id"]
    user_1, user_2 = await app.get_users(c1_id), await app.get_users(c2_id)
    n1, n2 = user_1.mention, user_2.mention

    txt = f"""
💑 <b>𝗖𝗮𝘀𝗮𝗹 𝗱𝗼 𝗗𝗶𝗮 𝗱𝗲 𝗛𝗼𝗷𝗲:</b>

{n1} + {n2} = 💚💘

📅 <b>𝗢𝘀 𝗽𝗿𝗼́𝘅𝗶𝗺𝗼𝘀 𝗰𝗮𝘀𝗮𝗶𝘀 𝘀𝗲𝗿𝗮̃𝗼 𝘀𝗲𝗹𝗲𝗰𝗶𝗼𝗻𝗮𝗱𝗼𝘀 𝗲𝗺 {tomorrow} !</b>
"""
    await message.reply_photo(
        image_url, caption=txt, reply_markup=InlineKeyboardMarkup(POLICE)
    )
    await msg.delete()


def cleanup_files(chat_id):
    try:
        if os.path.exists("./downloads/pfp1.png"):
            os.remove("./downloads/pfp1.png")
        if os.path.exists("./downloads/pfp2.png"):
            os.remove("./downloads/pfp2.png")
        if os.path.exists(f"cache/couple_{chat_id}.png"):
            os.remove(f"cache/couple_{chat_id}.png")
    except Exception as e:
        logging.warning(str(e))


__MODULE__ = "💑 𝗖𝗮𝘀𝗮𝗹"
__HELP__ = """📌 𝗘𝘀𝘁𝗲 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 𝗽𝗲𝗿𝗺𝗶𝘁𝗲 𝗮𝗼𝘀 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗰𝗿𝗶𝗮𝗿 𝘂𝗺𝗮 𝗶𝗺𝗮𝗴𝗲𝗺 𝗱𝗲 
𝗰𝗮𝘀𝗮𝗹 𝗱𝗲 𝗵𝗼𝗷𝗲 𝗮 𝗽𝗮𝗿𝘁𝗶𝗿 𝗱𝗲 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝘁𝗲𝘅𝘁𝗼. 𝗖𝗮𝘀𝗮𝗹 𝗱𝗲 𝗵𝗼𝗷𝗲 𝗲́ 
𝘂𝗺𝗮 𝗳𝗲𝗿𝗿𝗮𝗺𝗲𝗻𝘁𝗮 𝗽𝗮𝗿𝗮 𝗰𝗿𝗶𝗮𝗿 𝗶𝗺𝗮𝗴𝗲𝗻𝘀 𝗯𝗲𝗹𝗮𝘀 𝗱𝗲 𝗰𝗼́𝗱𝗶𝗴𝗼 𝗳𝗼𝗻𝘁𝗲.

• /couples: 𝗥𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗮 𝘂𝗺𝗮 𝗰𝗮𝘀𝗮𝗹 𝗱𝗲 𝗵𝗼𝗷𝗲 𝗮𝗼 𝗴𝗿𝘂𝗽𝗼 𝗱𝗲 𝗰𝗵𝗮𝘁 𝗲 𝗽𝗮𝗿𝘁𝗶𝗿 𝗱𝗼 𝗰𝗼𝗻𝘁𝗲𝘂́𝗱𝗼 𝗱𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺.
"""
