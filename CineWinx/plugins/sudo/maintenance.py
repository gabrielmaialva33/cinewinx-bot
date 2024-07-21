from pyrogram import filters
from pyrogram.types import Message

from CineWinx import app
from CineWinx.misc import SUDOERS
from CineWinx.utils.database import (
    get_lang,
    is_maintenance,
    maintenance_off,
    maintenance_on,
)
from config import PREFIXES
from strings import get_command, get_string

MAINTENANCE_COMMAND = get_command("MAINTENANCE_COMMAND")


@app.on_message(filters.command(MAINTENANCE_COMMAND, PREFIXES) & SUDOERS)
async def maintenance(_client: app, message: Message):
    try:
        language = await get_lang(message.chat.id)
        _ = get_string(language)
    except Exception as e:
        _ = get_string("pt")
    usage = _["maint_1"]
    if len(message.command) != 2:
        return await message.reply_text(usage)
    message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        if await is_maintenance() is False:
            await message.reply_text("⚠️ 𝗢 𝗺𝗼𝗱𝗼 𝗱𝗲 𝗺𝗮𝗻𝘂𝘁𝗲𝗻𝗰̧𝗮̃𝗼 𝗷𝗮́ 𝗲𝘀𝘁𝗮́ 𝗮𝘁𝗶𝘃𝗮𝗱𝗼")
        else:
            await maintenance_on()
            await message.reply_text(_["maint_2"])
    elif state == "disable":
        if await is_maintenance() is False:
            await maintenance_off()
            await message.reply_text(_["maint_3"])
        else:
            await message.reply_text("⚠️ 𝗢 𝗺𝗼𝗱𝗼 𝗱𝗲 𝗺𝗮𝗻𝘂𝘁𝗲𝗻𝗰̧𝗮̃𝗼 𝗷𝗮́ 𝗲𝘀𝘁𝗮́ 𝗱𝗲𝘀𝗮𝘁𝗶𝘃𝗮𝗱𝗼")
    else:
        await message.reply_text(usage)
