import random

from Bot import userbot
from Bot.core.mongo import mongodb_async

db = mongodb_async.assistants
assistant_dict = {}


async def get_client(assistant: int) -> userbot:
    """
    Get the userbot client based on the assistant number
    :param assistant:
    :return userbot:
    """
    assistant_clients = {
        1: userbot.one,
    }
    return assistant_clients[int(assistant)]


async def set_assistant(chat_id: int) -> userbot:
    """
    Set random assistant to the chat_id
    :param chat_id:
    :return userbot:
    """
    from Bot.core.userbot import assistants

    ran_assistant = random.choice(assistants)
    assistant_dict[chat_id] = ran_assistant
    await db.update_one(
        {"chat_id": chat_id},
        {"$set": {"assistant": ran_assistant}},
        upsert=True,
    )
    assistant = await get_client(ran_assistant)
    return assistant


async def get_assistant(chat_id: int) -> userbot:
    """
    Get the assistant based on the chat_id
    :param chat_id:
    :return userbot:
    """
    from Bot.core.userbot import assistants

    assistant = assistant_dict.get(chat_id)
    if not assistant:
        db_assistant = await db.find_one({"chat_id": chat_id})
        if not db_assistant:
            user = await set_assistant(chat_id)
            return user
        else:
            got_assis = db_assistant["assistant"]
            if got_assis in assistants:
                assistant_dict[chat_id] = got_assis
                user = await get_client(got_assis)
                return user
            else:
                user = await set_assistant(chat_id)
                return user
    else:
        if assistant in assistants:
            user = await get_client(assistant)
            return user
        else:
            user = await set_assistant(chat_id)
            return user


async def set_calls_assistant(chat_id) -> int:
    """
    Set random assistant to the chat_id
    :param chat_id:
    :return int:
    """
    from Bot.core.userbot import assistants

    ran_assistant = random.choice(assistants)
    assistant_dict[chat_id] = ran_assistant
    await db.update_one(
        {"chat_id": chat_id},
        {"$set": {"assistant": ran_assistant}},
        upsert=True,
    )
    return ran_assistant


async def group_assistant(self, chat_id: int) -> int:
    """
    Get the assistant based on the chat_id
    :param self:
    :param chat_id:
    :return int:
    """
    from Bot.core.userbot import assistants

    assistant = assistant_dict.get(chat_id)
    if not assistant:
        db_assistant = await db.find_one({"chat_id": chat_id})
        if not db_assistant:
            assis = await set_calls_assistant(chat_id)
        else:
            assis = db_assistant["assistant"]
            if assis in assistants:
                assistant_dict[chat_id] = assis
                assis = assis
            else:
                assis = await set_calls_assistant(chat_id)
    else:
        if assistant in assistants:
            assis = assistant
        else:
            assis = await set_calls_assistant(chat_id)
    self_clients = {
        1: self.one,
    }
    return self_clients[int(assis)]
