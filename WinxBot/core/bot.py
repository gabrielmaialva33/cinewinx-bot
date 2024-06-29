from pyrogram import Client

from config import API_ID, API_HASH, BOT_TOKEN


class Winx(Client):
    def __init__(self):
        super().__init__(
            "WinxBot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
        )

        self.id = None
        self.username = None
        self.mention = None

    async def start(self):
        await super().start()

        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        print("WinxBot has started.")

    async def stop(self, *args):
        await super().stop()
        print("WinxBot has stopped.")
