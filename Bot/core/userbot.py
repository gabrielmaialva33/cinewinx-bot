from pyrogram import Client, errors

from config import API_HASH, API_ID, LANGUAGE, LOGGER_GROUP_ID, STRING_SESSION_1
from strings import get_string

from ..logger import log

assistants = []
assistant_ids = []

_ = get_string(LANGUAGE)


class UserBot(Client):
    def __init__(self):
        if STRING_SESSION_1:
            self.one = Client(
                f"{__name__}Assistant1",
                api_id=API_ID,
                api_hash=API_HASH,
                session_string=STRING_SESSION_1,
                no_updates=True,
            )

            self.one.id = None
            self.one.username = None
            self.one.mention = None
        else:
            self.one = None

    async def start(self):
        log(__name__).info("Starting assistants.")

        if STRING_SESSION_1:
            await self.one.start()

            self.one.id = self.one.me.id
            self.name = self.one.me.first_name + " " + (self.one.me.last_name or "")
            self.one.username = self.one.me.username
            self.one.mention = self.one.me.mention

            assistants.append(1)
            assistant_ids.append(self.one.id)

            try:
                text = _["assistant_1"].format(
                    self.one.mention, self.one.id, self.name, self.one.username
                )
                await self.one.send_message(chat_id=LOGGER_GROUP_ID, text=text)
            except (errors.ChannelInvalid, errors.PeerIdInvalid):
                log(__name__).error("LOGGER_GROUP_ID is invalid.")
            except errors.FloodWait as e:
                log(__name__).error(f"FloodWait: {e.value} seconds.")
            except errors.RPCError as e:
                log(__name__).error(f"RPCError: {e}")
            except Exception as e:
                log(__name__).error(f"An error occurred: {e}")

            log(__name__).info(f"{self.name} assistant {assistants[-1]} has started.")

    async def stop(self):
        log(__name__).info("Stopping assistants.")

        try:
            if STRING_SESSION_1:
                text = _["assistant_2"].format(self.one.mention)
                await self.one.send_message(chat_id=LOGGER_GROUP_ID, text=text)
                await self.one.stop()
        except Exception as e:
            log(__name__).error(f"An error occurred: {e}")
