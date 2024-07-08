from Bot.core.mongo import mongodb

chats_db = mongodb.chats
chatstats_db = mongodb.chatstats
private_db = mongodb.privatechats


# private served chats
async def get_private_served_chats() -> list:
    chats_list = []
    async for chat in private_db.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list


async def is_served_private_chat(chat_id: int) -> bool:
    chat = await private_db.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True


async def add_private_chat(chat_id: int):
    is_served = await is_served_private_chat(chat_id)
    if is_served:
        return
    return await private_db.insert_one({"chat_id": chat_id})


async def remove_private_chat(chat_id: int):
    is_served = await is_served_private_chat(chat_id)
    if not is_served:
        return
    return await private_db.delete_one({"chat_id": chat_id})
