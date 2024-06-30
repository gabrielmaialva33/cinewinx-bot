import asyncio

from pyrogram import idle

from Bot import app, userbot


async def init():
    await app.start()
    await userbot.start()

    await idle()

    await userbot.stop()
    await app.stop()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
