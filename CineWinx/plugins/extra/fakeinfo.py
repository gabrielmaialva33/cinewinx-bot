from datetime import datetime

import requests
from pyrogram import filters
from pyrogram.types import Message

from CineWinx import app
from config import PREFIXES, BANNED_USERS
from strings import get_command

FAKE_COMMAND = get_command("FAKE_COMMAND")


@app.on_message(filters.command(FAKE_COMMAND, PREFIXES) & ~BANNED_USERS)
async def address(_, message: Message):
    try:
        query = message.text.split(maxsplit=1)[1].strip()
    except IndexError:
        query = "br"
    url = f"https://randomuser.me/api/?nat={query}"
    response = requests.get(url)
    data = response.json()

    if "results" in data:
        user_data = data["results"][0]

        name = f"{user_data['name']['title']} {user_data['name']['first']} {user_data['name']['last']}"
        age = user_data["dob"]["age"]
        birthdate = user_data["dob"]["date"]
        address = f"{user_data['location']['street']['number']} {user_data['location']['street']['name']}"
        city = user_data["location"]["city"]
        state = user_data["location"]["state"]
        country = user_data["location"]["country"]
        postal = user_data["location"]["postcode"]
        email = user_data["email"]
        username = user_data["login"]["username"]
        password = user_data["login"]["password"]
        phone = user_data["phone"]
        cell_phone = user_data["cell"]
        id_name = user_data["id"]["name"]
        id_value = user_data["id"]["value"]
        picture_url = user_data["picture"]["large"]

        caption = f"""
📛 <b>𝗡𝗼𝗺𝗲</b>: {name}
🎂 <b>𝗜𝗱𝗮𝗱𝗲</b>: {datetime.fromisoformat(birthdate).date()} ({age} 𝗮𝗻𝗼𝘀)
🏠 <b>𝗘𝗻𝗱𝗲𝗿𝗲𝗰̧𝗼</b>: {address}
🌍 <b>𝗣𝗮𝗶́𝘀</b>: {country}
🏙️ <b>𝗖𝗶𝗱𝗮𝗱𝗲</b>: {city}
🗺️ <b>𝗘𝘀𝘁𝗮𝗱𝗼</b>: {state}
📮 <b>𝗖𝗼́𝗱𝗶𝗴𝗼 𝗣𝗼𝘀𝘁𝗮𝗹</b>: {postal}
📧 <b>𝗘𝗺𝗮𝗶𝗹</b>: {email}
🔑 <b>𝗨𝘀𝘂𝗮́𝗿𝗶𝗼</b>: {username}
🔒 <b>𝗦𝗲𝗻𝗵𝗮</b>: {password}
📞 <b>𝗧𝗲𝗹𝗲𝗳𝗼𝗻𝗲</b>: {phone}
📱 <b>𝗖𝗲𝗹𝘂𝗹𝗮𝗿</b>: {cell_phone}
🆔 <b>𝗡𝗼𝗺𝗲 𝗱𝗼 𝗗𝗼𝗰𝘂𝗺𝗲𝗻𝘁𝗼</b>: {id_name}
🆔 <b>𝗩𝗮𝗹𝗼𝗿</b>: {id_value}
"""
        await message.reply_photo(photo=picture_url, caption=caption)
    else:
        await message.reply_text("⚠️ 𝗢𝗼𝗽𝘀, 𝗻𝗮̃𝗼 𝗳𝗼𝗶 𝗲𝗻𝗰𝗼𝗻𝘁𝗿𝗮𝗱𝗼 𝗻𝗲𝗻𝗵𝘂𝗺 𝗲𝗻𝗱𝗲𝗿𝗲𝗰̧𝗼. ❗")


__MODULE__ = "👤 𝗙𝗮𝗸𝗲"
__HELP__ = """
<b>👤 𝗣𝗲𝗿𝘀𝗼𝗻𝗮𝗴𝗲𝗺 𝗙𝗮𝗸𝗲:</b>

𝗘𝘀𝘁𝗲 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 𝗽𝗮𝗿𝗮 𝗴𝗲𝗿𝗮𝗿 𝘂𝗺 𝗳𝗮𝗸𝗲 𝗱𝗲 𝗽𝗲𝗿𝘀𝗼𝗻𝗮𝗴𝗲𝗺 𝗲𝗻𝗱𝗲𝗿𝗲𝗰̧𝗼.

<b>📋 𝗙𝗲𝗿𝗿𝗮𝗺𝗲𝗻𝘁𝗮𝘀:</b>

• /fake <𝗰𝗼́𝗱𝗶𝗴𝗼>: 𝗣𝗲𝗿𝘀𝗼𝗻𝗮𝗴𝗲𝗺 𝘂𝗺 𝗳𝗮𝗸𝗲 𝗱𝗲 𝗽𝗲𝗿𝘀𝗼𝗻𝗮𝗴𝗲𝗺 𝗲𝗻𝗱𝗲𝗿𝗲𝗰̧𝗼.
• /fake br: 𝗣𝗲𝗿𝘀𝗼𝗻𝗮𝗴𝗲𝗺 𝘂𝗺 𝗳𝗮𝗸𝗲 𝗱𝗲 𝗽𝗲𝗿𝘀𝗼𝗻𝗮𝗴𝗲𝗺 𝗲𝗻𝗱𝗲𝗿𝗲𝗰̧𝗼 𝗱𝗼 𝗕𝗿𝗮𝘀𝗶𝗹. 🇧🇷
"""
