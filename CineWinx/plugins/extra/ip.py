import asyncio

from aiohttp import ClientSession
from pyrogram import Client, filters
from pyrogram.types import Message

from CineWinx import app
from config import PREFIXES, BANNED_USERS
from strings import get_command

IP_COMMAND = get_command("IP_COMMAND")

loop = asyncio.get_event_loop()


@app.on_message(filters.command(IP_COMMAND, PREFIXES) & ~BANNED_USERS)
async def ip_info(_: Client, message: Message):
    if len(message.command) != 2:
        await message.reply_text(
            "📄 𝗙𝗼𝗿𝗻𝗲𝗰̧𝗮 𝘂𝗺 𝗲𝗻𝗱𝗲𝗿𝗲𝗰̧𝗼 𝗜𝗣. 𝗘𝘅𝗲𝗺𝗽𝗹𝗼: <code>/ip 8.8.8.8</code>"
        )
        return

    ip_address = message.command[1]
    info = await get_ip_info(ip_address)

    if info:
        await message.reply_text(info)
    else:
        await message.reply_text(
            "❌ 𝗡𝗮̃𝗼 𝗳𝗼𝗶 𝗽𝗼𝘀𝘀𝗶́𝘃𝗲𝗹 𝗼𝗯𝘁𝗲𝗿 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝘀𝗼𝗯𝗿𝗲 𝗼 𝗲𝗻𝗱𝗲𝗿𝗲𝗰̧𝗼 𝗜𝗣 𝗳𝗼𝗿𝗻𝗲𝗰𝗶𝗱𝗼."
        )


async def get_ip_info(ip_address: str) -> str or None:
    api_url = f"http://ip-api.com/json/{ip_address}"

    try:
        async with ClientSession(loop=loop) as client:
            response = await client.get(api_url)
            data = await response.json()
            if data["status"] == "success":
                info = (
                    f"🌐 𝗜𝗣: {data['query']}\n"
                    f"🌍 𝗣𝗮𝗶́𝘀: {data['country']}\n"
                    f"🏴 𝗖𝗼́𝗱𝗶𝗴𝗼 𝗱𝗼 𝗣𝗮𝗶́s: {data['countryCode']}\n"
                    f"🏙️ 𝗥𝗲𝗴𝗶𝗮̃𝗼: {data['region']}\n"
                    f"🗺️ 𝗡𝗼𝗺𝗲 𝗱𝗮 𝗥𝗲𝗴𝗶𝗮̃𝗼: {data['regionName']}\n"
                    f"🏘️ 𝗖𝗶𝗱𝗮𝗱𝗲: {data['city']}\n"
                    f"🔢 𝗖𝗼́𝗱𝗶𝗴𝗼 𝗣𝗼𝘀𝘁𝗮𝗹: {data['zip']}\n"
                    f"📍 𝗟𝗮𝘁𝗶𝘁𝘂𝗱𝗲: {data['lat']}\n"
                    f"📍 𝗟𝗼𝗻𝗴𝗶𝘁𝘂𝗱𝗲: {data['lon']}\n"
                    f"📡 𝗜𝗦𝗣: {data['isp']}\n"
                    f"🏢 𝗢𝗿𝗴𝗮𝗻𝗶𝘇𝗮𝗰̧𝗮̃𝗼: {data['org']}\n"
                    f"🏢 𝗔𝗦: {data['as']}"
                )
                return info
            else:
                return None

    except Exception as e:
        print(f"❌ 𝗘𝗿𝗿𝗼 𝗮𝗼 𝗯𝘂𝘀𝗰𝗮𝗿 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗼 𝗜𝗣: {e}")
    finally:
        await client.close()


__MODULE__ = "🌐 𝗜𝗣"
__HELP__ = """
<b>🌐 𝗜𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗲 𝗨𝗺 𝗜𝗣:</b>

𝗘𝘀𝘁𝗲 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 𝗽𝗮𝗿𝗮 𝗼𝗯𝘁𝗲𝗿 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝘀𝗼𝗯𝗿𝗲 𝗼 𝗲𝗻𝗱𝗲𝗿𝗲𝗰̧𝗼 𝗱𝗲 𝘂𝗺 𝗜𝗣.

📋 𝗖𝗼𝗺𝗮𝗻𝗱𝗼:

• <code>/ip</code> <𝗜𝗣>: 𝗢𝗯𝘁𝗲́𝗺 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝘀𝗼𝗯𝗿𝗲 𝗼 𝗲𝗻𝗱𝗲𝗿𝗲𝗰̧𝗼 𝗱𝗲 𝘂𝗺 𝗜𝗣.
"""
