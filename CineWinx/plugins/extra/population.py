import logging

from pyrogram import Client, filters
from pyrogram.types import Message
import requests
from CineWinx import app
from config import PREFIXES, BANNED_USERS
from strings import get_command

POPULATION_COMMAND = get_command("POPULATION_COMMAND")


@app.on_message(filters.command(POPULATION_COMMAND, PREFIXES) & ~BANNED_USERS)
def country_command_handler(_client: Client, message: Message):
    try:
        country_code = message.text.split(maxsplit=1)[1].strip()
    except IndexError:
        message.reply_text("⚠️ 𝗩𝗼𝗰𝗲̂ 𝗻𝗮̃𝗼 𝗳𝗼𝗿𝗻𝗲𝗰𝗲𝘂 𝗼 𝗰𝗼́𝗱𝗶𝗴𝗼 𝗱𝗼 𝗣𝗮𝗶́𝘀. ❗")
        return

    api_url = f"https://restcountries.com/v3.1/alpha/{country_code}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()

        country_info = response.json()
        if country_info:
            country_name = country_info[0].get("name", {}).get("common", "𝗡/𝗔")
            capital = country_info[0].get("capital", ["𝗡/𝗔"])[0]
            population = country_info[0].get("population", "𝗡/𝗔")

            response_text = (
                f"🌍 𝗜𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗼 𝗣𝗮𝗶́𝘀\n\n"
                f"📛 𝗡𝗼𝗺𝗲: {country_name}\n"
                f"🏛️ 𝗖𝗮𝗽𝗶𝘁𝗮𝗹: {capital}\n"
                f"👥 𝗣𝗼𝗽𝘂𝗹𝗮𝗰̧𝗮̃𝗼: {population}"
            )
        else:
            response_text = "⚠️ 𝗘𝗿𝗿𝗼 𝗮𝗼 𝗼𝗯𝘁𝗲𝗿 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗼 𝗽𝗮𝗶́𝘀 𝗮𝗽𝗮𝗿𝘁𝗶𝗿 𝗱𝗮 𝗔𝗣𝗜. ❗"
    except requests.exceptions.HTTPError as http_err:
        response_text = f"⚠️ 𝗢𝗰𝗼𝗿𝗿𝗲𝘂 𝘂𝗺 𝗲𝗿𝗿𝗼 𝗛𝗧𝗧𝗣. 𝗜𝗻𝘀𝗶𝗿𝗮 𝗼 𝗰ó𝗱𝗶𝗴𝗼 𝗱𝗼 𝗽𝗮𝗶́𝘀 𝗰𝗼𝗿𝗿𝗲𝘁𝗼. ❗"
    except Exception as err:
        logging.error(err, exc_info=True)
        response_text = f"⚠️ 𝗢𝗰𝗼𝗿𝗿𝗲𝘂 𝘂𝗺 𝗲𝗿𝗿𝗼 𝗮𝗼 𝗼𝗯𝘁𝗲𝗿 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗼 𝗽𝗮𝗶́𝘀. ❗"

    message.reply_text(response_text)


__MODULE__ = "🌍 𝗣𝗼𝗽𝘂𝗹𝗮𝗰̧𝗮̃𝗼"
__HELP__ = """
<b> 🌍 𝗜𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗼 𝗣𝗮𝗶́𝘀:</b>

• /population <𝗰𝗼́𝗱𝗶𝗴𝗼 𝗱𝗼 𝗣𝗮𝗶́𝘀>: 𝗢𝗯𝘁é𝗺 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗼 𝗽𝗮𝗶́𝘀 𝗰𝗼𝗿𝗿𝗲𝘁𝗼. 🌍
• /population br: 𝗢𝗯𝘁𝗲́𝗺 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗼 𝗽𝗮𝗶́𝘀 𝗱𝗼 𝗕𝗿𝗮𝘀𝗶𝗹. 🇧🇷
"""
