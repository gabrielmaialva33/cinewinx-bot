import os

from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode
from pyrogram.types import BotCommand

import config
from strings import get_string
from ..logging import LOGGER

_ = get_string(config.LANGUAGE)


class WinxBot(Client):
    """
    Bot client. Inherits from pyrogram.Client.
    """

    def __init__(self):
        LOGGER(__name__).info(f"Starting {config.BOT_NAME}.")

        super().__init__(
            config.BOT_NAME,
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=8,
            in_memory=True,
        )

        self.id = None
        self.username = None
        self.mention = None

    async def start(self):
        await super().start()

        get_me = await self.get_me()

        self.id = get_me.id
        self.username = get_me.username
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.mention = self.me.mention

        try:
            text = _["bot_1"].format(self.mention, self.id, self.name, self.username)
            img = await self.download_media(get_me.photo.big_file_id)
            await self.send_photo(chat_id=config.LOG_GROUP_ID, photo=img, caption=text)
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error("LOGGER_GROUP_ID is invalid.")
            await self.stop()
        except errors.FloodWait as e:
            LOGGER(__name__).error(f"FloodWait: {e.value} seconds.")
            await self.stop()
        except errors.RPCError as e:
            LOGGER(__name__).error(f"RPCError: {e}")
            await self.stop()
        except Exception as e:
            LOGGER(__name__).error(f"An error occurred: {e}")
            await self.stop()

        if config.SET_CMDS == str(True):
            try:
                await self.set_bot_commands(
                    [
                        BotCommand("start", "iniciar o bot"),
                        BotCommand("help", "obter o menu de ajuda"),
                        BotCommand("ping", "verificar se o bot está vivo ou morto"),
                        BotCommand("play", "começar a tocar a música solicitada"),
                        BotCommand("skip", "ir para a próxima faixa na fila"),
                        BotCommand("pause", "pausar a música que está tocando"),
                        BotCommand("resume", "retomar a música pausada"),
                        BotCommand("end", "limpar a fila e sair do chat de voz"),
                        BotCommand(
                            "shuffle", "embaralhar aleatoriamente a playlist na fila."
                        ),
                        BotCommand(
                            "playmode",
                            "permite alterar o modo de reprodução padrão para o seu chat",
                        ),
                        BotCommand(
                            "settings",
                            "abrir as configurações do bot de música para o seu chat.",
                        ),
                    ]
                )
            except:
                pass
        else:
            pass
        try:
            member = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
            if member.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error("Please promote Bot as Admin in Logger Group")
                return await self.stop()
        except Exception as e:
            LOGGER(__name__).error(f"An error occurred: {e}")

        LOGGER(__name__).info(f"Bot Started as {self.name}")

    async def stop(self, *args):
        await self.send_message(
            chat_id=config.LOG_GROUP_ID, text=_["bot_2"].format(self.mention)
        )
        await super().stop()

        LOGGER(__name__).info(f"{self.name} has stopped.")
        os.kill(os.getpid(), 9)

    async def get_history(self, chat_id: int, limit: int = 1):
        """
        Get the history of a chat.
        """
        try:
            return await self.get_history(chat_id, limit=limit)
        except errors.FloodWait as e:
            LOGGER(__name__).error(f"FloodWait: {e}")
            return []
        except errors.RPCError as e:
            LOGGER(__name__).error(f"RPCError: {e}")
            return []
        except Exception as e:
            LOGGER(__name__).error(f"An error occurred: {e}")
            return []
