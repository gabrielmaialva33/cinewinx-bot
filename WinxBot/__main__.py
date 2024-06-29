import asyncio

from pyrogram import idle

from WinxBot import app


async def init():
    await app.start()

    await idle()

    await app.stop()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
