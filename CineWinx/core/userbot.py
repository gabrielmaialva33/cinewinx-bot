import logging

from pyrogram import Client, errors

import config
from strings import get_string

from ..logging import LOGGER

assistants = []
assistant_ids = []

_ = get_string(config.LANGUAGE)


class Userbot(Client):
    def __init__(self):
        if config.STRING1:
            self.one = Client(
                "WinxString1",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                session_string=str(config.STRING1),
            )
            self.one.id = None
            self.one.name = None
            self.one.username = None
            self.one.mention = None
        else:
            self.one = None

        if config.STRING2:
            self.two = Client(
                "WinxString2",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                session_string=str(config.STRING2),
            )
            self.two.id = None
            self.two.name = None
            self.two.username = None
            self.two.mention = None
        else:
            self.two = None

        if config.STRING3:
            self.three = Client(
                "WinxString3",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                session_string=str(config.STRING3),
            )
            self.three.id = None
            self.three.name = None
            self.three.username = None
            self.three.mention = None
        else:
            self.three = None

        if config.STRING4:
            self.four = Client(
                "WinxString4",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                session_string=str(config.STRING4),
            )
            self.four.id = None
            self.four.name = None
            self.four.username = None
            self.four.mention = None
        else:
            self.four = None

        if config.STRING5:
            self.five = Client(
                "WinxString5",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                session_string=str(config.STRING5),
            )
            self.five.id = None
            self.five.name = None
            self.five.username = None
            self.five.mention = None
        else:
            self.five = None

    async def start(self):
        LOGGER(__name__).info(f"Starting Assistant Clients")

        if config.STRING1:
            await self.one.start()

            self.one.id = self.one.me.id
            self.one.name = self.one.me.first_name + " " + (self.one.me.last_name or "")
            self.one.username = self.one.me.username
            self.one.mention = self.one.me.mention

            try:
                await self.one.join_chat("@winxbotx")
                await self.one.join_chat("@winxmusicsupport")
                await self.one.join_chat("@cinewinx")
                await self.one.join_chat("@canalclubdaswinx")
                await self.one.join_chat("@cinewinxcoments")
            except Exception as e:
                logging.error(f"An error occurred: {e}")

            try:
                text = _["assistant_1"].format(
                    self.one.mention, self.one.id, self.one.name, self.one.username
                )
                #img = await self.one.download_media(self.one.me.photo.big_file_id)
                #await self.one.send_photo(chat_id=config.LOG_GROUP_ID, photo=img, caption=text)
                await self.one.send_message(chat_id=config.LOG_GROUP_ID, text=text)
            except (errors.ChannelInvalid, errors.PeerIdInvalid):
                LOGGER(__name__).error("LOGGER_GROUP_ID is invalid.")
            except errors.FloodWait as e:
                LOGGER(__name__).error(f"FloodWait: {e.value} seconds.")
            except errors.RPCError as e:
                LOGGER(__name__).error(f"RPCError: {e}")
            except Exception as e:
                LOGGER(__name__).error(f"An error occurred: {e}")

            assistants.append(1)
            assistant_ids.append(self.one.id)

            LOGGER(__name__).info(
                f"{self.one.name} assistant {assistants[-1]} has started."
            )

        if config.STRING2:
            await self.two.start()

            self.two.id = self.two.me.id
            self.two.name = self.two.me.first_name + " " + (self.two.me.last_name or "")
            self.two.username = self.two.me.username
            self.two.mention = self.two.me.mention

            try:
                await self.two.join_chat("@winxbotx")
                await self.two.join_chat("@winxmusicsupport")
                await self.two.join_chat("@cinewinx")
                await self.two.join_chat("@canalclubdaswinx")
                await self.two.join_chat("@cinewinxcoments")
            except Exception as e:
                logging.error(f"An error occurred: {e}")

            try:
                text = _["assistant_1"].format(
                    self.two.mention, self.two.id, self.two.name, self.two.username
                )
                await self.two.send_message(chat_id=config.LOG_GROUP_ID, text=text)
            except (errors.ChannelInvalid, errors.PeerIdInvalid):
                LOGGER(__name__).error("LOGGER_GROUP_ID is invalid.")
            except errors.FloodWait as e:
                LOGGER(__name__).error(f"FloodWait: {e.value} seconds.")
            except errors.RPCError as e:
                LOGGER(__name__).error(f"RPCError: {e}")
            except Exception as e:
                LOGGER(__name__).error(f"An error occurred: {e}")

            assistants.append(2)
            assistant_ids.append(self.two.id)

            LOGGER(__name__).info(
                f"{self.two.name} assistant {assistants[-1]} has started."
            )

        if config.STRING3:
            await self.three.start()

            self.three.id = self.three.me.id
            self.three.name = (
                self.three.me.first_name + " " + (self.three.me.last_name or "")
            )
            self.three.username = self.three.me.username
            self.three.mention = self.three.me.mention

            try:
                await self.three.join_chat("@winxbotx")
                await self.three.join_chat("@winxmusicsupport")
                await self.three.join_chat("@cinewinx")
                await self.three.join_chat("@canalclubdaswinx")
                await self.three.join_chat("@cinewinxcoments")
            except Exception as e:
                logging.error(f"An error occurred: {e}")

            try:
                text = _["assistant_1"].format(
                    self.three.mention,
                    self.three.id,
                    self.three.name,
                    self.three.username,
                )
                await self.three.send_message(chat_id=config.LOG_GROUP_ID, text=text)
            except (errors.ChannelInvalid, errors.PeerIdInvalid):
                LOGGER(__name__).error("LOGGER_GROUP_ID is invalid.")
            except errors.FloodWait as e:
                LOGGER(__name__).error(f"FloodWait: {e.value} seconds.")
            except errors.RPCError as e:
                LOGGER(__name__).error(f"RPCError: {e}")
            except Exception as e:
                LOGGER(__name__).error(f"An error occurred: {e}")

            assistants.append(3)
            assistant_ids.append(self.three.id)

            LOGGER(__name__).info(
                f"{self.three.name} assistant {assistants[-1]} has started."
            )

        if config.STRING4:
            await self.four.start()

            self.four.id = self.four.me.id
            self.four.name = (
                self.four.me.first_name + " " + (self.four.me.last_name or "")
            )
            self.four.username = self.four.me.username
            self.four.mention = self.four.me.mention

            try:
                await self.four.join_chat("@winxbotx")
                await self.four.join_chat("@winxmusicsupport")
                await self.four.join_chat("@cinewinx")
                await self.four.join_chat("@canalclubdaswinx")
                await self.four.join_chat("@cinewinxcoments")
            except Exception as e:
                logging.error(f"An error occurred: {e}")

            try:
                text = _["assistant_1"].format(
                    self.four.mention, self.four.id, self.four.name, self.four.username
                )
                await self.four.send_message(chat_id=config.LOG_GROUP_ID, text=text)
            except (errors.ChannelInvalid, errors.PeerIdInvalid):
                LOGGER(__name__).error("LOGGER_GROUP_ID is invalid.")
            except errors.FloodWait as e:
                LOGGER(__name__).error(f"FloodWait: {e.value} seconds.")
            except errors.RPCError as e:
                LOGGER(__name__).error(f"RPCError: {e}")
            except Exception as e:
                LOGGER(__name__).error(f"An error occurred: {e}")

            assistants.append(4)
            assistant_ids.append(self.four.id)

            LOGGER(__name__).info(
                f"{self.four.name} assistant {assistants[-1]} has started."
            )

        if config.STRING5:
            await self.five.start()

            self.five.id = self.five.me.id
            self.five.name = (
                self.five.me.first_name + " " + (self.five.me.last_name or "")
            )
            self.five.username = self.five.me.username
            self.five.mention = self.five.me.mention

            try:
                await self.five.join_chat("@winxbotx")
                await self.five.join_chat("@winxmusicsupport")
                await self.five.join_chat("@cinewinx")
                await self.five.join_chat("@canalclubdaswinx")
                await self.five.join_chat("@cinewinxcoments")
            except Exception as e:
                logging.error(f"An error occurred: {e}")

            try:
                text = _["assistant_1"].format(
                    self.five.mention, self.five.id, self.five.name, self.five.username
                )
                await self.five.send_message(chat_id=config.LOG_GROUP_ID, text=text)
            except (errors.ChannelInvalid, errors.PeerIdInvalid):
                LOGGER(__name__).error("LOGGER_GROUP_ID is invalid.")
            except errors.FloodWait as e:
                LOGGER(__name__).error(f"FloodWait: {e.value} seconds.")
            except errors.RPCError as e:
                LOGGER(__name__).error(f"RPCError: {e}")
            except Exception as e:
                LOGGER(__name__).error(f"An error occurred: {e}")

            assistants.append(5)
            assistant_ids.append(self.five.id)

            LOGGER(__name__).info(
                f"{self.five.name} assistant {assistants[-1]} has started."
            )

    async def stop(self, *args):
        LOGGER(__name__).info("Stopping assistants.")

        try:
            if config.STRING1:
                text = _["assistant_2"].format(self.one.mention)
                await self.one.send_message(chat_id=config.LOG_GROUP_ID, text=text)
                await self.one.stop()
                LOGGER(__name__).info(f"Assistant One Stopped")
            if config.STRING2:
                text = _["assistant_2"].format(self.two.mention)
                await self.two.send_message(chat_id=config.LOG_GROUP_ID, text=text)
                await self.two.stop()
                LOGGER(__name__).info(f"Assistant Two Stopped")
            if config.STRING3:
                text = _["assistant_2"].format(self.three.mention)
                await self.three.send_message(chat_id=config.LOG_GROUP_ID, text=text)
                await self.three.stop()
                LOGGER(__name__).info(f"Assistant Three Stopped")
            if config.STRING4:
                text = _["assistant_2"].format(self.four.mention)
                await self.four.send_message(chat_id=config.LOG_GROUP_ID, text=text)
                await self.four.stop()
                LOGGER(__name__).info(f"Assistant Four Stopped")
            if config.STRING5:
                text = _["assistant_2"].format(self.five.mention)
                await self.five.send_message(chat_id=config.LOG_GROUP_ID, text=text)
                await self.five.stop()
                LOGGER(__name__).info(f"Assistant Five Stopped")
        except Exception as e:
            LOGGER(__name__).error(f"An error occurred: {e}")
