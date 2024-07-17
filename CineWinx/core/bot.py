import os
import sys

from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import BotCommand

import config
from strings import get_string

from ..logging import LOGGER

_ = get_string(config.LANGUAGE)


class WinxBot(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot")
        super().__init__(
            "CineWinx",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
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
            await self.send_message(chat_id=config.LOG_GROUP_ID, text=text)
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error("LOGGER_GROUP_ID is invalid.")
            sys.exit()
        except errors.FloodWait as e:
            LOGGER(__name__).error(f"FloodWait: {e.value} seconds.")
            sys.exit()
        except errors.RPCError as e:
            LOGGER(__name__).error(f"RPCError: {e}")
            sys.exit()
        except Exception as e:
            LOGGER(__name__).error(f"An error occurred: {e}")
            sys.exit()

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
            a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
            if a.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error("Please promote Bot as Admin in Logger Group")
                return await self.stop()
        except Exception:
            pass

        if get_me.last_name:
            self.name = get_me.first_name + " " + get_me.last_name
        else:
            self.name = get_me.first_name
        LOGGER(__name__).info(f"CineWinx Started as {self.name}")

    async def stop(self, *args):
        await self.send_message(
            chat_id=config.LOG_GROUP_ID, text=_["bot_2"].format(self.mention)
        )
        await super().stop()
        LOGGER(__name__).info(f"{self.name} has stopped.")
        os.kill(os.getpid(), 9)
