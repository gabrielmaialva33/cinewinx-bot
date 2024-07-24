import random

from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from CineWinx import app


@app.on_message(filters.command(["genpassword", "genpw"]))
async def password(_client: Client, message: Message):
    reply_message = await message.reply_text(text="⏳ 𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗮𝗻𝗱𝗼..")
    password = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+".lower()

    try:
        qw = message.text.split(" ", 1)[1]
    except IndexError:
        st = ["5", "7", "6", "9", "10", "12", "14", "8", "13"]
        qw = random.choice(st)

    limit = int(qw)
    random_value = "".join(random.sample(password, limit))
    txt = (
        f"<b>🔢 𝗟𝗶𝗺𝗶𝘁𝗲:</b> {str(limit)} \n<b>🔐 𝗦𝗲𝗻𝗵𝗮:</b> <code>{random_value}</code>"
    )
    me = await app.get_me()
    btn = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "➕ 𝗔𝗗𝗜𝗖𝗜𝗢𝗡𝗔𝗥", url=f"https://t.me/{me.username}?startgroup=true"
                )
            ]
        ]
    )
    await reply_message.edit_text(
        text=txt, reply_markup=btn, parse_mode=enums.ParseMode.HTML
    )

__MODULE__ = "🔐 𝗦𝗲𝗻𝗵𝗮𝘀"
__HELP__ = """
<b>🔐 𝗚𝗲𝗿𝗮𝗱𝗼𝗿 𝗱𝗲 𝗦𝗲𝗻𝗵𝗮𝘀:</b>

𝗘𝘀𝘁𝗲 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 𝗽𝗮𝗿𝗮 𝗴𝗲𝗿𝗮𝗿 𝘂𝗺𝗮 𝘀𝗲𝗻𝗵𝗮 𝗮𝗹𝗲𝗮𝘁𝗼́𝗿𝗶𝗮 𝗱𝗲 𝗰𝗼𝗺𝗽𝗿𝗶𝗺𝗲𝗻𝘁𝗼𝘀 𝗮𝗹𝗲𝗮𝘁𝗼́𝗿𝗶𝗼𝘀.

<b>📋 𝗙𝗲𝗿𝗿𝗮𝗺𝗲𝗻𝘁𝗮𝘀:</b>
• /genpassword <𝗻𝘂𝗺𝗲𝗿𝗼>: 𝗚𝗲𝗿𝗮𝗿 𝘂𝗺𝗮 𝘀𝗲𝗻𝗵𝗮 𝗱𝗲 𝗻𝗼 𝘁𝗮𝗺𝗮𝗻𝗵𝗼 𝗱𝗲 𝗰𝗮𝗿𝗮𝗰𝘁𝗲𝗿𝗲𝘀.
• /genpw <𝗻𝘂𝗺𝗲𝗿𝗼>: 𝗚𝗲𝗿𝗮𝗿 𝘂𝗺𝗮 𝘀𝗲𝗻𝗵𝗮 𝗱𝗲 𝗻𝗼 𝘁𝗮𝗺𝗮𝗻𝗵𝗼 𝗱𝗲 𝗰𝗮𝗿𝗮𝗰𝘁𝗲𝗿𝗲𝘀.
• /genpassword: 𝗚𝗲𝗿𝗮𝗿 𝘂𝗺𝗮 𝘀𝗲𝗻𝗵𝗮.
"""