from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus

from config import API_ID, API_HASH, BOT_TOKEN, LOGGER_GROUP_ID
from ..log import log


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

        try:
            await self.send_message(chat_id=LOGGER_GROUP_ID, text="WinxBot has started.")
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            log(__name__).error("LOGGER_GROUP_ID is invalid.")
        except errors.FloodWait as e:
            log(__name__).error(f"FloodWait: {e.value} seconds.")
        except errors.RPCError as e:
            log(__name__).error(f"RPCError: {e}")
        except Exception as e:
            log(__name__).error(f"An error occurred: {e}")

        bot = await self.get_chat_member(chat_id=LOGGER_GROUP_ID, user_id=self.id)
        group = await self.get_chat(LOGGER_GROUP_ID)
        if bot.status != ChatMemberStatus.ADMINISTRATOR:
            log(__name__).error(f"WinxBot is not an admin in {group.title}.")
            return await self.stop()

        log(__name__).info("WinxBot has started.")

    async def stop(self, *args):
        await super().stop()
        log(__name__).info("WinxBot has stopped.")
