from typing import Any

from CineWinx.core.mongo import mongodb

couple_db = mongodb.couples


async def get_lovers(chat_id: int):
    lovers = await couple_db.find_one({"chat_id": chat_id})
    if lovers:
        lovers = lovers["couple"]
    else:
        lovers = {}
    return lovers


async def get_image(chat_id: int):
    lovers = await couple_db.find_one({"chat_id": chat_id})
    if lovers:
        lovers = lovers["image_url"]
    else:
        lovers = {}
    return lovers


async def get_lovers_date(chat_id: int, date: str):
    lovers = await get_lovers(chat_id)
    if date in lovers:
        return lovers[date]
    else:
        return False


async def get_couple(chat_id: int) -> dict[str, Any] or None:
    couple = await couple_db.find_one({"chat_id": chat_id})
    if couple:
        return couple
    else:
        couple = None
    return couple


async def save_couple(chat_id: int, date: str, couple: dict[str, Any], image_url: str, pin_id: int) -> None:
    lovers = await get_lovers(chat_id)
    lovers[date] = couple
    await couple_db.update_one(
        {"chat_id": chat_id},
        {"$set": {"couple": lovers, "image_url": image_url, "pin_id": pin_id}},
        upsert=True,
    )


async def save_pin(chat_id: int, pin_id: int) -> None:
    lovers = await get_lovers(chat_id)
    image_url = await get_image(chat_id)
    await couple_db.update_one(
        {"chat_id": chat_id},
        {"$set": {"couple": lovers, "image_url": image_url, "pin_id": pin_id}},
        upsert=True,
    )


async def get_pin(chat_id: int) -> int or None:
    lovers = await couple_db.find_one({"chat_id": chat_id})
    if lovers:
        lovers = lovers["pin_id"]
    else:
        lovers = None
    return lovers
