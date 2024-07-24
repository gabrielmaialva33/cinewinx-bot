import random

from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from CineWinx import app


@app.on_message(filters.command(["genpassword", 'genpw']))
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
    txt = f"<b>🔢 𝗟𝗶𝗺𝗶𝘁𝗲:</b> {str(limit)} \n<b>🔐 𝗦𝗲𝗻𝗵𝗮:</b> <code>{random_value}</code>"
    me = await app.get_me()
    btn = InlineKeyboardMarkup([[InlineKeyboardButton('➕ 𝗔𝗗𝗜𝗖𝗜𝗢𝗡𝗔𝗥', url=f'https://t.me/{me.username}?startgroup=true')]])
    await reply_message.edit_text(text=txt, reply_markup=btn, parse_mode=enums.ParseMode.HTML)
