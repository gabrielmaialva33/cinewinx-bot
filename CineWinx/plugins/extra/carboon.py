from io import BytesIO

import aiohttp
from pyrogram import filters, Client
from pyrogram.types import Message

from CineWinx import app
from config import PREFIXES, BANNED_USERS
from strings import get_command


async def make_carbon(code):
    url = "https://carbonara.solopov.dev/api/cook"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"code": code}) as resp:
            image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image


CARBON_COMMAND = get_command("CARBON_COMMAND")


@app.on_message(filters.command(CARBON_COMMAND, PREFIXES) & ~BANNED_USERS)
async def _carbon(_client: Client, message: Message):
    replied = message.reply_to_message
    if not replied:
        await message.reply_text(
            "𝗥𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗮 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝘁𝗲𝘅𝘁𝗼 𝗽𝗮𝗿𝗮 𝗰𝗿𝗶𝗮𝗿 𝘂𝗺 𝗖𝗮𝗿𝗯𝗼𝗻."
        )
        return
    if not (replied.text or replied.caption):
        return await message.reply_text(
            "𝗥𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗮 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝘁𝗲𝘅𝘁𝗼 𝗽𝗮𝗿𝗮 𝗰𝗿𝗶𝗮𝗿 𝘂𝗺 𝗖𝗮𝗿𝗯𝗼𝗻."
        )
    text = await message.reply("📋 𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗮𝗻𝗱𝗼...")
    carbon = await make_carbon(replied.text or replied.caption)
    await text.edit("📤 𝗙𝗮𝘇𝗲𝗻𝗱𝗼 𝘂𝗽𝗹𝗼𝗮𝗱...")
    await message.reply_photo(carbon)
    await text.delete()
    carbon.close()


__MODULE__ = "🖼️ 𝗖𝗮𝗿𝗯𝗼𝗻"
__HELP__ = """
<b>🖼️ 𝗖𝗼𝗺𝗮𝗻𝗱𝗼 𝗖𝗮𝗿𝗯𝗼𝗻:</b>

𝗘𝘀𝘁𝗲 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 𝗽𝗲𝗿𝗺𝗶𝘁𝗲 𝗮𝗼𝘀 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗰𝗿𝗶𝗮𝗿 𝘂𝗺𝗮 𝗶𝗺𝗮𝗴𝗲𝗺 𝗖𝗮𝗿𝗯𝗼𝗻 𝗮 𝗽𝗮𝗿𝘁𝗶𝗿 𝗱𝗲 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝘁𝗲𝘅𝘁𝗼. 𝗖𝗮𝗿𝗯𝗼𝗻 𝗲́ 𝘂𝗺𝗮 𝗳𝗲𝗿𝗿𝗮𝗺𝗲𝗻𝘁𝗮 𝗽𝗮𝗿𝗮 𝗰𝗿𝗶𝗮𝗿 𝗶𝗺𝗮𝗴𝗲𝗻𝘀 𝗯𝗲𝗹𝗮𝘀 𝗱𝗲 𝗰𝗼́𝗱𝗶𝗴𝗼 𝗳𝗼𝗻𝘁𝗲.

<b>📋 𝗙𝗲𝗿𝗿𝗮𝗺𝗲𝗻𝘁𝗮𝘀:</b>
- 𝗥𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗮 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝘁𝗲𝘅𝘁𝗼 𝗽𝗮𝗿𝗮 𝗴𝗲𝗿𝗮𝗿 𝘂𝗺𝗮 𝗶𝗺𝗮𝗴𝗲𝗺 𝗖𝗮𝗿𝗯𝗼𝗻 𝗮 𝗽𝗮𝗿𝘁𝗶𝗿 𝗱𝗼 𝗰𝗼𝗻𝘁𝗲𝘂́𝗱𝗼 𝗱𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺.
- 𝗦𝘂𝗽𝗼𝗿𝘁𝗮 𝘁𝗮𝗻𝘁𝗼 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗻𝘀 𝗲𝗺 𝘁𝗲𝘅𝘁𝗼 𝗾𝘂𝗮𝗻𝘁𝗼 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗻𝘀 𝗰𝗼𝗺 𝗹𝗲𝗴𝗲𝗻𝗱𝗮𝘀.
- 𝗘𝘅𝗶𝗯𝗲 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗽𝗿𝗼𝗰𝗲𝘀𝘀𝗮𝗺𝗲𝗻𝘁𝗼 𝗲𝗻𝗾𝘂𝗮𝗻𝘁𝗼 𝗴𝗲𝗿𝗮 𝗮 𝗶𝗺𝗮𝗴𝗲𝗺 𝗖𝗮𝗿𝗯𝗼𝗻.
- 𝗙𝗮𝘇 𝘂𝗽𝗹𝗼𝗮𝗱 𝗱𝗮 𝗶𝗺𝗮𝗴𝗲𝗺 𝗖𝗮𝗿𝗯𝗼𝗻 𝗴𝗲𝗿𝗮𝗱𝗮 𝗲𝗺 𝗿𝗲𝘀𝗽𝗼𝘀𝘁𝗮 𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗼𝗿𝗶𝗴𝗶𝗻𝗮𝗹.

<b>📋 𝗖𝗼𝗺𝗮𝗻𝗱𝗼𝘀:</b>
• /carbon: 𝗥𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗮 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝘁𝗲𝘅𝘁𝗼 𝗽𝗮𝗿𝗮 𝗴𝗲𝗿𝗮𝗿 𝘂𝗺𝗮 𝗶𝗺𝗮𝗴𝗲𝗺 𝗖𝗮𝗿𝗯𝗼𝗻 𝗮 𝗽𝗮𝗿𝘁𝗶𝗿 𝗱𝗼 𝗰𝗼𝗻𝘁𝗲𝘂́𝗱𝗼 𝗱𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺.

📌 𝗡𝗼𝘁𝗮: 𝗖𝗲𝗿𝘁𝗶𝗳𝗶𝗾𝘂𝗲-𝘀𝗲 𝗱𝗲 𝗿𝗲𝘀𝗽𝗼𝗻𝗱𝗲𝗿 𝗮 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝘁𝗲𝘅𝘁𝗼 𝗽𝗮𝗿𝗮 𝗴𝗲𝗿𝗮𝗿 𝗮 𝗶𝗺𝗮𝗴𝗲𝗺 𝗖𝗮𝗿𝗯𝗼𝗻 𝗰𝗼𝗺 𝘀𝘂𝗰𝗲𝘀𝘀𝗼.
"""
