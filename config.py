from os import getenv

from dotenv import load_dotenv

load_dotenv()

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
