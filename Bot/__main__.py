import asyncio
import importlib

from pyrogram import idle

from Bot import app, telethn, userbot
from Bot.core.call import call
from Bot.database import get_banned, get_blocked_users
from Bot.plugins import ALL_MODULES
from config import (
    BANNED_USERS,
    BOT_TOKEN,
    STRING_SESSION_1,
    STRING_SESSION_2,
    STRING_SESSION_3,
    STRING_SESSION_4,
    STRING_SESSION_5,
)
from .logger import log

loop = asyncio.get_event_loop_policy().get_event_loop()
MODULES = []


async def init():
    if (
            not STRING_SESSION_1
            and not STRING_SESSION_2
            and not STRING_SESSION_3
            and not STRING_SESSION_4
            and not STRING_SESSION_5
    ):
        log(__name__).error("No string sessions found. Exiting...")
        return

    # load banned and blocked users
    try:
        users = await get_banned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_blocked_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        log(__name__).error(f"An error occurred: {e}")

    # start bot and import modules
    await app.start()
    for all_module in ALL_MODULES:
        imported_module = importlib.import_module("Bot.plugins" + all_module)
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            imported_module.__MODULE__ = imported_module.__MODULE__
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                MODULES[imported_module.__MODULE__.lower()] = imported_module
    log("Bot.plugins").info("Successfully Imported Modules ")

    await userbot.start()
    await call.start()

    await idle()

    await userbot.stop()
    await app.stop()


if __name__ == "__main__":
    telethn.start(bot_token=BOT_TOKEN)
    loop.run_until_complete(init())
