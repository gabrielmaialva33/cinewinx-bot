import time

from pyrogram import filters

from config import OWNER_ID, MONGO_DB_URI
from .core.mongo import mongodb_sync
from .logger import log

SUDOERS = filters.user()

_boot_ = time.time()


def memory_db():
    global db
    global db_clone
    db = {}
    db_clone = {}
    log(__name__).info("Memory database has been initialized.")


def sudo():
    global SUDOERS
    owner = OWNER_ID
    if MONGO_DB_URI is None:
        for user_id in owner:
            SUDOERS.add(user_id)
    else:
        sudoers_db = mongodb_sync.sudoers
        sudoers = sudoers_db.find_one({"sudo": "sudo"})
        sudoers = [] if not sudoers else sudoers["sudoers"]
        for user_id in owner:
            SUDOERS.add(user_id)
            if user_id not in sudoers:
                sudoers.append(user_id)
                sudoers_db.update_one(
                    {"sudo": "sudo"},
                    {"$set": {"sudoers": sudoers}},
                    upsert=True,
                )
        if sudoers:
            for x in sudoers:
                SUDOERS.add(x)
    log(__name__).info("Sudoers have been initialized.")
