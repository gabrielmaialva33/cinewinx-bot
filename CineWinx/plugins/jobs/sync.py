import random

from pyrogram import Client, filters
from pyrogram.types import Message

import config
from CineWinx import LOGGER, app
from CineWinx.core.userbot import assistants
from CineWinx.utils import get_client


@app.on_message(filters.command("sync"))
async def sync_job(client: Client, message: Message):
    """
    Syncs the database with the latest data.
    """
    LOGGER(__name__).info("Syncing channel posts...")
    if not config.INDEX_CHANNEL_ID:
        LOGGER(__name__).error("No Channel ID set! Exiting Sync Job.")
        return

    try:
        winx = random.choice(assistants)
        ubot: Client = await get_client(winx)

        channel = await ubot.get_chat(config.INDEX_CHANNEL_ID)
        # search post in channel with hashtag #2016y
        async for post in ubot.search_messages(channel.id, "#2016y", limit=1):
            p = await ubot.get_messages(channel.id, post.id + 1)
            print(p)
            await message.reply(f"Syncing post: {p.link}")

    except Exception as e:
        LOGGER(__name__).error(str(e))
        await message.reply("Failed to sync data.")
