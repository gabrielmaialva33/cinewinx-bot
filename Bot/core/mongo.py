from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

from config import MONGO_DB_URI

from ..logger import log

log(__name__).info("Connecting to MongoDB...")

if not MONGO_DB_URI:
    log(__name__).error("No MongoDB URI found. Exiting...")
    exit()

try:
    # extract the database name from the URI
    db_name = MONGO_DB_URI.split("/")[-1].split("?")[0]
    print(db_name)

    _mongo_async_ = AsyncIOMotorClient(MONGO_DB_URI)
    _mongo_sync_ = MongoClient(MONGO_DB_URI)
    mongodb = _mongo_async_.db_name
    py_mongodb = _mongo_sync_.db_name
    log(__name__).info("Connected to MongoDB.")
except Exception as e:
    log(__name__).error(f"An error occurred: {e}")
    exit()
