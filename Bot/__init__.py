from Bot.core.bot import Bot
from Bot.core.userbot import UserBot

from .logger import log
from .misc import memory_db

memory_db()

app = Bot()
userbot = UserBot()
