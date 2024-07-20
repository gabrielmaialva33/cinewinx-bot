from pyrogram import filters
from pyrogram.types import Message

from CineWinx import app
from CineWinx.misc import SUDOERS
from CineWinx.utils.database import autoend_off, autoend_on
from config import PREFIXES
from strings import get_command

AUTOEND_COMMAND = get_command("AUTOEND_COMMAND")


@app.on_message(filters.command(AUTOEND_COMMAND, PREFIXES) & SUDOERS)
async def auto_end_stream(_client: app, message: Message):
    usage = "<b>📋 𝗨𝘀𝗼:</b>\n\n<code>/autoend</code> [enable|disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        await autoend_on()
        await message.reply_text(
            "✅ 𝗘𝗻𝗰𝗲𝗿𝗿𝗮𝗺𝗲𝗻𝘁𝗼 𝗮𝘂𝘁𝗼𝗺𝗮́𝘁𝗶𝗰𝗼 𝗱𝗲 𝘁𝗿𝗮𝗻𝘀𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗮𝘁𝗶𝘃𝗮𝗱𝗼.\n\n"
            "🕒 𝗢 𝗯𝗼𝘁 𝘀𝗮𝗶𝗿𝗮́ 𝗱𝗼 𝗰𝗵𝗮𝘁 𝗱𝗲 𝘃𝗼𝘇 𝗮𝘂𝘁𝗼𝗺𝗮𝘁𝗶𝗰𝗮𝗺𝗲𝗻𝘁𝗲 𝗮𝗽𝗼́𝘀 3 𝗺𝗶𝗻𝘂𝘁𝗼𝘀 𝘀𝗲 𝗻𝗶𝗻𝗴𝘂𝗲́𝗺 𝗲𝘀𝘁𝗶𝘃𝗲𝗿 𝗼𝘂𝘃𝗶𝗻𝗱𝗼, "
            "𝗰𝗼𝗺 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝗮𝘃𝗶𝘀𝗼."
        )
    elif state == "disable":
        await autoend_off()
        await message.reply_text("❌ 𝗘𝗻𝗰𝗲𝗿𝗿𝗮𝗺𝗲𝗻𝘁𝗼 𝗮𝘂𝘁𝗼𝗺𝗮́𝘁𝗶𝗰𝗼 𝗱𝗲𝘀𝗮𝘁𝗶𝘃𝗮𝗱𝗼.")
    else:
        await message.reply_text(usage)
