from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

adminlist = {}
autoclean = []

# Get this value from my.telegram.org/apps
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH", None)

# Get your token from @BotFather on Telegram.
BOT_TOKEN = getenv("BOT_TOKEN", None)

# Get your mongo url from cloud.mongodb.com
MONGO_DB_URI = getenv("MONGO_DB_URI", None)

# Bot settings
LANGUAGE = getenv("LANGUAGE", "pt-br")
LOGGER_GROUP_ID = int(getenv("LOGGER_GROUP_ID", None))
OWNER_ID = int(getenv("OWNER_ID", None))
PRIVATE_BOT_MODE = getenv("PRIVATE_BOT_MODE", False)

# UserBot settings
STRING_SESSION_1 = getenv("STRING_SESSION_1", None)
STRING_SESSION_2 = getenv("STRING_SESSION_2", None)
STRING_SESSION_3 = getenv("STRING_SESSION_3", None)
STRING_SESSION_4 = getenv("STRING_SESSION_4", None)
STRING_SESSION_5 = getenv("STRING_SESSION_5", None)

# Filters
BANNED_USERS = filters.user()

# Assets
STREAM_IMG_URL = getenv(
    "STREAM_IMG_URL", "https://telegra.ph/file/fb8b2718c68c97e7b8706.png"
)

YOUTUBE_IMG_URL = getenv(
    "YOUTUBE_IMG_URL", "https://telegra.ph/file/fb8b2718c68c97e7b8706.png"
)
SOUNCLOUD_IMG_URL = getenv(
    "SOUNCLOUD_IMG_URL", "https://telegra.ph/file/fb8b2718c68c97e7b8706.png"
)
PLAYLIST_IMG_URL = getenv(
    "PLAYLIST_IMG_URL", "https://telegra.ph/file/fb8b2718c68c97e7b8706.png"
)

TELEGRAM_AUDIO_URL = getenv(
    "TELEGRAM_AUDIO_URL", "https://telegra.ph/file/fb8b2718c68c97e7b8706.png"
)
TELEGRAM_VIDEO_URL = getenv(
    "TELEGRAM_VIDEO_URL", "https://telegra.ph/file/fb8b2718c68c97e7b8706.png"
)
