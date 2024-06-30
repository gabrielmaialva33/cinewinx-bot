import os
import sys

from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

from config import API_HASH, API_ID, BOT_TOKEN, LANGUAGE, LOGGER_GROUP_ID
from strings import get_string
from ..logger import log

_ = get_string(LANGUAGE)


class Bot(Client):
    def __init__(self):
        super().__init__(
            f"{__name__}",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=8,
            in_memory=True,
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
            text = _["bot_1"].format(self.mention, self.id, self.name, self.username)
            await self.send_message(chat_id=LOGGER_GROUP_ID, text=text)
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            log(__name__).error("LOGGER_GROUP_ID is invalid.")
            sys.exit()
        except errors.FloodWait as e:
            log(__name__).error(f"FloodWait: {e.value} seconds.")
            sys.exit()
        except errors.RPCError as e:
            log(__name__).error(f"RPCError: {e}")
            sys.exit()
        except Exception as e:
            log(__name__).error(f"An error occurred: {e}")
            sys.exit()

        bot = await self.get_chat_member(chat_id=LOGGER_GROUP_ID, user_id=self.id)
        group = await self.get_chat(LOGGER_GROUP_ID)
        if bot.status != ChatMemberStatus.ADMINISTRATOR:
            await self.send_message(
                chat_id=LOGGER_GROUP_ID,
                text=_["bot_3"].format(self.mention, group.title),
            )
            log(__name__).error(f"{self.name} is not an admin in {group.title}.")
            return await self.stop()

        log(__name__).info(f"{self.name} has started.")

    async def stop(self, *args):
        await self.send_message(
            chat_id=LOGGER_GROUP_ID, text=_["bot_2"].format(self.mention)
        )
        await super().stop()
        log(__name__).info(f"{self.name} has stopped.")
        os.kill(os.getpid(), 9)
