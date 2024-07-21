import os
import shutil

from pyrogram import filters

from CineWinx import app
from CineWinx.misc import SUDOERS


@app.on_message(filters.command("clean") & SUDOERS)
async def clean(_, message):
    msg = await message.reply_text("🧹 𝗟𝗶𝗺𝗽𝗮𝗻𝗱𝗼...")
    dir = "downloads"
    dir1 = "cache"
    shutil.rmtree(dir)
    shutil.rmtree(dir1)
    os.mkdir(dir)
    os.mkdir(dir1)
    await msg.edit("✅ 𝗟𝗶𝗺𝗽𝗼 𝗰𝗼𝗺 𝘀𝘂𝗰𝗲𝘀𝘀𝗼!")
