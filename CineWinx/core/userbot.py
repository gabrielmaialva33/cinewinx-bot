import logging

from pyrogram import Client, errors

import config
from config import WINX_ECOSYSTEM_IDS, IN_DEV_MODE
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

        if config.STRING6:
            self.six = Client(
                "WinxString6",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                session_string=str(config.STRING6),
            )
            self.six.id = None
            self.six.name = None
            self.six.username = None
            self.six.mention = None
        else:
            self.six = None

        if config.STRING7:
            self.seven = Client(
                "WinxString7",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                session_string=str(config.STRING7),
            )
            self.seven.id = None
            self.seven.name = None
            self.seven.username = None
            self.seven.mention = None
        else:
            self.seven = None

        if config.STRING8:
            self.eight = Client(
                "WinxString8",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                session_string=str(config.STRING8),
            )
            self.eight.id = None
            self.eight.name = None
            self.eight.username = None
            self.eight.mention = None
        else:
            self.eight = None

        if config.STRING9:
            self.nine = Client(
                "WinxString9",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                session_string=str(config.STRING9),
            )
            self.nine.id = None
            self.nine.name = None
            self.nine.username = None
            self.nine.mention = None
        else:
            self.nine = None

        if config.STRING10:
            self.ten = Client(
                "WinxString10",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                session_string=str(config.STRING10),
            )
            self.ten.id = None
            self.ten.name = None
            self.ten.username = None
            self.ten.mention = None
        else:
            self.ten = None

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
                await self.one.send_message(chat_id=config.LOG_GROUP_ID, text=text)

                if WINX_ECOSYSTEM_IDS and IN_DEV_MODE == str(False):
                    me = await self.one.get_me()
                    pic = (
                        await self.two.download_media(me.photo.big_file_id)
                        if me.photo
                        else None
                    )

                    for chat in WINX_ECOSYSTEM_IDS:
                        await self.one.join_chat(chat)

                        if pic:
                            await self.one.send_photo(
                                chat_id=chat, photo=pic, caption=text
                            )

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

                if WINX_ECOSYSTEM_IDS and IN_DEV_MODE == str(False):
                    me = await self.two.get_me()
                    pic = (
                        await self.two.download_media(me.photo.big_file_id)
                        if me.photo
                        else None
                    )

                    for chat in WINX_ECOSYSTEM_IDS:
                        await self.two.join_chat(chat)

                        if pic:
                            await self.one.send_photo(
                                chat_id=chat, photo=pic, caption=text
                            )
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

                if WINX_ECOSYSTEM_IDS and IN_DEV_MODE == str(False):
                    me = await self.three.get_me()
                    pic = (
                        await self.three.download_media(me.photo.big_file_id)
                        if me.photo
                        else None
                    )

                    for chat in WINX_ECOSYSTEM_IDS:
                        await self.three.join_chat(chat)

                        if pic:
                            await self.three.send_photo(
                                chat_id=chat, photo=pic, caption=text
                            )
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

                if WINX_ECOSYSTEM_IDS and IN_DEV_MODE == str(False):
                    me = await self.four.get_me()
                    pic = (
                        await self.four.download_media(me.photo.big_file_id)
                        if me.photo
                        else None
                    )

                    for chat in WINX_ECOSYSTEM_IDS:
                        await self.four.join_chat(chat)

                        if pic:
                            await self.four.send_photo(
                                chat_id=chat, photo=pic, caption=text
                            )
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

                if WINX_ECOSYSTEM_IDS and IN_DEV_MODE == str(False):
                    me = await self.five.get_me()
                    pic = (
                        await self.five.download_media(me.photo.big_file_id)
                        if me.photo
                        else None
                    )

                    for chat in WINX_ECOSYSTEM_IDS:
                        await self.five.join_chat(chat)

                        if pic:
                            await self.five.send_photo(
                                chat_id=chat, photo=pic, caption=text
                            )
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

        if config.STRING6:
            await self.six.start()

            self.six.id = self.six.me.id
            self.six.name = self.six.me.first_name + " " + (self.six.me.last_name or "")
            self.six.username = self.six.me.username
            self.six.mention = self.six.me.mention

            try:
                await self.six.join_chat("@winxbotx")
                await self.six.join_chat("@winxmusicsupport")
                await self.six.join_chat("@cinewinx")
                await self.six.join_chat("@canalclubdaswinx")
                await self.six.join_chat("@cinewinxcoments")
            except Exception as e:
                logging.error(f"An error occurred: {e}")

            try:
                text = _["assistant_1"].format(
                    self.six.mention, self.six.id, self.six.name, self.six.username
                )
                await self.six.send_message(chat_id=config.LOG_GROUP_ID, text=text)

                if WINX_ECOSYSTEM_IDS and IN_DEV_MODE == str(False):
                    me = await self.six.get_me()
                    pic = (
                        await self.six.download_media(me.photo.big_file_id)
                        if me.photo
                        else None
                    )

                    for chat in WINX_ECOSYSTEM_IDS:
                        await self.six.join_chat(chat)

                        if pic:
                            await self.six.send_photo(
                                chat_id=chat, photo=pic, caption=text
                            )
            except (errors.ChannelInvalid, errors.PeerIdInvalid):
                LOGGER(__name__).error("LOGGER_GROUP_ID is invalid.")
            except errors.FloodWait as e:
                LOGGER(__name__).error(f"FloodWait: {e.value} seconds.")
            except errors.RPCError as e:
                LOGGER(__name__).error(f"RPCError: {e}")
            except Exception as e:
                LOGGER(__name__).error(f"An error occurred: {e}")

            assistants.append(6)
            assistant_ids.append(self.six.id)

            LOGGER(__name__).info(
                f"{self.six.name} assistant {assistants[-1]} has started."
            )

        if config.STRING7:
            await self.seven.start()

            self.seven.id = self.seven.me.id
            self.seven.name = (
                self.seven.me.first_name + " " + (self.seven.me.last_name or "")
            )
            self.seven.username = self.seven.me.username
            self.seven.mention = self.seven.me.mention

            try:
                await self.seven.join_chat("@winxbotx")
                await self.seven.join_chat("@winxmusicsupport")
                await self.seven.join_chat("@cinewinx")
                await self.seven.join_chat("@canalclubdaswinx")
                await self.seven.join_chat("@cinewinxcoments")
            except Exception as e:
                logging.error(f"An error occurred: {e}")

            try:
                text = _["assistant_1"].format(
                    self.seven.mention,
                    self.seven.id,
                    self.seven.name,
                    self.seven.username,
                )
                await self.seven.send_message(chat_id=config.LOG_GROUP_ID, text=text)

                if WINX_ECOSYSTEM_IDS and IN_DEV_MODE == str(False):
                    me = await self.seven.get_me()
                    pic = (
                        await self.seven.download_media(me.photo.big_file_id)
                        if me.photo
                        else None
                    )

                    for chat in WINX_ECOSYSTEM_IDS:
                        await self.seven.join_chat(chat)

                        if pic:
                            await self.seven.send_photo(
                                chat_id=chat, photo=pic, caption=text
                            )
            except (errors.ChannelInvalid, errors.PeerIdInvalid):
                LOGGER(__name__).error("LOGGER_GROUP_ID is invalid.")
            except errors.FloodWait as e:
                LOGGER(__name__).error(f"FloodWait: {e.value} seconds.")
            except errors.RPCError as e:
                LOGGER(__name__).error(f"RPCError: {e}")
            except Exception as e:
                LOGGER(__name__).error(f"An error occurred: {e}")

            assistants.append(7)
            assistant_ids.append(self.seven.id)

            LOGGER(__name__).info(
                f"{self.seven.name} assistant {assistants[-1]} has started."
            )

        if config.STRING8:
            await self.eight.start()

            self.eight.id = self.eight.me.id
            self.eight.name = (
                self.eight.me.first_name + " " + (self.eight.me.last_name or "")
            )
            self.eight.username = self.eight.me.username
            self.eight.mention = self.eight.me.mention

            try:
                await self.eight.join_chat("@winxbotx")
                await self.eight.join_chat("@winxmusicsupport")
                await self.eight.join_chat("@cinewinx")
                await self.eight.join_chat("@canalclubdaswinx")
                await self.eight.join_chat("@cinewinxcoments")
            except Exception as e:
                logging.error(f"An error occurred: {e}")

            try:
                text = _["assistant_1"].format(
                    self.eight.mention,
                    self.eight.id,
                    self.eight.name,
                    self.eight.username,
                )
                await self.eight.send_message(chat_id=config.LOG_GROUP_ID, text=text)

                if WINX_ECOSYSTEM_IDS and IN_DEV_MODE == str(False):
                    me = await self.eight.get_me()
                    pic = (
                        await self.eight.download_media(me.photo.big_file_id)
                        if me.photo
                        else None
                    )

                    for chat in WINX_ECOSYSTEM_IDS:
                        await self.eight.join_chat(chat)

                        if pic:
                            await self.eight.send_photo(
                                chat_id=chat, photo=pic, caption=text
                            )
            except (errors.ChannelInvalid, errors.PeerIdInvalid):
                LOGGER(__name__).error("LOGGER_GROUP_ID is invalid.")
            except errors.FloodWait as e:
                LOGGER(__name__).error(f"FloodWait: {e.value} seconds.")
            except errors.RPCError as e:
                LOGGER(__name__).error(f"RPCError: {e}")
            except Exception as e:
                LOGGER(__name__).error(f"An error occurred: {e}")

            assistants.append(8)
            assistant_ids.append(self.eight.id)

            LOGGER(__name__).info(
                f"{self.eight.name} assistant {assistants[-1]} has started."
            )

        if config.STRING9:
            await self.nine.start()

            self.nine.id = self.nine.me.id
            self.nine.name = (
                self.nine.me.first_name + " " + (self.nine.me.last_name or "")
            )
            self.nine.username = self.nine.me.username
            self.nine.mention = self.nine.me.mention

            try:
                await self.nine.join_chat("@winxbotx")
                await self.nine.join_chat("@winxmusicsupport")
                await self.nine.join_chat("@cinewinx")
                await self.nine.join_chat("@canalclubdaswinx")
                await self.nine.join_chat("@cinewinxcoments")
            except Exception as e:
                logging.error(f"An error occurred: {e}")

            try:
                text = _["assistant_1"].format(
                    self.nine.mention, self.nine.id, self.nine.name, self.nine.username
                )
                await self.nine.send_message(chat_id=config.LOG_GROUP_ID, text=text)

                if WINX_ECOSYSTEM_IDS and IN_DEV_MODE == str(False):
                    me = await self.nine.get_me()
                    pic = (
                        await self.nine.download_media(me.photo.big_file_id)
                        if me.photo
                        else None
                    )

                    for chat in WINX_ECOSYSTEM_IDS:
                        await self.nine.join_chat(chat)

                        if pic:
                            await self.nine.send_photo(
                                chat_id=chat, photo=pic, caption=text
                            )
            except (errors.ChannelInvalid, errors.PeerIdInvalid):
                LOGGER(__name__).error("LOGGER_GROUP_ID is invalid.")
            except errors.FloodWait as e:
                LOGGER(__name__).error(f"FloodWait: {e.value} seconds.")
            except errors.RPCError as e:
                LOGGER(__name__).error(f"RPCError: {e}")
            except Exception as e:
                LOGGER(__name__).error(f"An error occurred: {e}")

            assistants.append(9)
            assistant_ids.append(self.nine.id)

            LOGGER(__name__).info(
                f"{self.nine.name} assistant {assistants[-1]} has started."
            )

        if config.STRING10:
            await self.ten.start()

            self.ten.id = self.ten.me.id
            self.ten.name = self.ten.me.first_name + " " + (self.ten.me.last_name or "")
            self.ten.username = self.ten.me.username
            self.ten.mention = self.ten.me.mention

            try:
                await self.ten.join_chat("@winxbotx")
                await self.ten.join_chat("@winxmusicsupport")
                await self.ten.join_chat("@cinewinx")
                await self.ten.join_chat("@canalclubdaswinx")
                await self.ten.join_chat("@cinewinxcoments")
            except Exception as e:
                logging.error(f"An error occurred: {e}")

            try:
                text = _["assistant_1"].format(
                    self.ten.mention, self.ten.id, self.ten.name, self.ten.username
                )
                await self.ten.send_message(chat_id=config.LOG_GROUP_ID, text=text)

                if WINX_ECOSYSTEM_IDS and IN_DEV_MODE == str(False):
                    me = await self.ten.get_me()
                    pic = (
                        await self.ten.download_media(me.photo.big_file_id)
                        if me.photo
                        else None
                    )

                    for chat in WINX_ECOSYSTEM_IDS:
                        await self.ten.join_chat(chat)

                        if pic:
                            await self.ten.send_photo(
                                chat_id=chat, photo=pic, caption=text
                            )
            except (errors.ChannelInvalid, errors.PeerIdInvalid):
                LOGGER(__name__).error("LOGGER_GROUP_ID is invalid.")
            except errors.FloodWait as e:
                LOGGER(__name__).error(f"FloodWait: {e.value} seconds.")
            except errors.RPCError as e:
                LOGGER(__name__).error(f"RPCError: {e}")
            except Exception as e:
                LOGGER(__name__).error(f"An error occurred: {e}")

            assistants.append(10)
            assistant_ids.append(self.ten.id)

            LOGGER(__name__).info(
                f"{self.ten.name} assistant {assistants[-1]} has started."
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

            if config.STRING6:
                text = _["assistant_2"].format(self.six.mention)
                await self.six.send_message(chat_id=config.LOG_GROUP_ID, text=text)
                await self.six.stop()
                LOGGER(__name__).info(f"Assistant Six Stopped")

            if config.STRING7:
                text = _["assistant_2"].format(self.seven.mention)
                await self.seven.send_message(chat_id=config.LOG_GROUP_ID, text=text)
                await self.seven.stop()
                LOGGER(__name__).info(f"Assistant Seven Stopped")

            if config.STRING8:
                text = _["assistant_2"].format(self.eight.mention)
                await self.eight.send_message(chat_id=config.LOG_GROUP_ID, text=text)
                await self.eight.stop()
                LOGGER(__name__).info(f"Assistant Eight Stopped")

            if config.STRING9:
                text = _["assistant_2"].format(self.nine.mention)
                await self.nine.send_message(chat_id=config.LOG_GROUP_ID, text=text)
                await self.nine.stop()
                LOGGER(__name__).info(f"Assistant Nine Stopped")

            if config.STRING10:
                text = _["assistant_2"].format(self.ten.mention)
                await self.ten.send_message(chat_id=config.LOG_GROUP_ID, text=text)
                await self.ten.stop()
                LOGGER(__name__).info(f"Assistant Ten Stopped")
        except Exception as e:
            LOGGER(__name__).error(f"An error occurred: {e}")
