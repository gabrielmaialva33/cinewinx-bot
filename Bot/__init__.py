from telethon import TelegramClient

from Bot.core.bot import Bot
from Bot.core.userbot import UserBot
from config import API_HASH, API_ID

from .logger import log
from .misc import memory_db

memory_db()

# Bot Client
app = Bot()

# Assistant Client
userbot = UserBot()

# Platforms
from .platforms import *

YouTube = YouTubeAPI()

# Misc
TEMP_DOWNLOAD_DIRECTORY = "downloads"
telethn = TelegramClient("Bot", API_ID, API_HASH)
