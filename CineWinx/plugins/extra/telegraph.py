import logging
import os

from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from CineWinx import app
from config import PREFIXES, BANNED_USERS
from strings import get_command
from telegraph import Telegraph

TELEGRAPH_COMMAND = get_command("TELEGRAPH_COMMAND")


@app.on_message(filters.command(TELEGRAPH_COMMAND, PREFIXES) & ~BANNED_USERS)
async def get_link_group(_client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text(
            "𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗿𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗮 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗰𝗼𝗺 𝗺𝗲́𝗱𝗶𝗮 𝗽𝗮𝗿𝗮 𝗳𝗮𝘇𝗲𝗿 𝘂𝗽𝗹𝗼𝗮𝗱 𝗻𝗼 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗽𝗵."
        )
    try:
        text = await message.reply("🔄 𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗮𝗻𝗱𝗼...")

        async def progress(current, total):
            await text.edit_text(f"📥 𝗕𝗮𝗶𝘅𝗮𝗻𝗱𝗼... {current * 100 / total:.1f}%")

        try:
            location = "cache"
            local_path = await message.reply_to_message.download(
                location, progress=progress
            )
            await text.edit_text("📤 𝗙𝗮𝘇𝗲𝗻𝗱𝗼 𝘂𝗽𝗹𝗼𝗮𝗱 𝗻𝗼 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗽𝗵...")
            graph = Telegraph()
            upload_path = graph.upload_file(local_path)
            await text.edit_text(
                f"🌐 | <a href='https://telegra.ph{upload_path[0]['src']}'>𝗟𝗶𝗻𝗸 𝗻𝗼 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗽𝗵</a>",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "𝗟𝗶𝗻𝗸 𝗻𝗼 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗽𝗵",
                                url=f"https://telegra.ph{upload_path[0]['src']}",
                            )
                        ]
                    ]
                ),
            )
            os.remove(local_path)
        except Exception as e:
            await text.edit_text(
                f"❌ | 𝗙𝗮𝗹𝗵𝗮 𝗻𝗼 𝘂𝗽𝗹𝗼𝗮𝗱 𝗱𝗼 𝗮𝗿𝗾𝘂𝗶𝘃𝗼 \n\n𝗥𝗮𝘇𝗮̃𝗼: <i>{e}</i>"
            )
            os.remove(local_path)
            return
    except Exception as e:
        logging.warning(str(e))


__MODULE__ = "🌐 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗽𝗵"
__HELP__ = """
🛠️ 𝗠𝗼́𝗱𝘂𝗹𝗼 𝗱𝗲 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗽𝗵

<b>📝 𝗗𝗲𝘀𝗰𝗿𝗶𝗰̧𝗮̃𝗼:</b>

𝗘𝘀𝘁𝗲 𝗺𝗼́𝗱𝘂𝗹𝗼 𝗽𝗿𝗼𝘃𝗲 𝗰𝗼𝗺𝗮𝗻𝗱𝗼𝘀 𝗽𝗮𝗿𝗮 𝗳𝗮𝘇𝗲𝗿 𝘂𝗽𝗹𝗼𝗮𝗱 𝗱𝗲 𝗺𝗲́𝗱𝗶𝗮 𝗻𝗼 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗽𝗵.

📋 𝗖𝗼𝗺𝗮𝗻𝗱𝗼:

<code>/tgm</code>, <code>/tgt</code>, <code>/telegraph</code>, <code>/tl</code>: 𝗙𝗮𝘇𝗲𝗿 𝘂𝗽𝗹𝗼𝗮𝗱 𝗱𝗲 𝗺𝗲́𝗱𝗶𝗮 𝗻𝗼 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗽𝗵.
"""
