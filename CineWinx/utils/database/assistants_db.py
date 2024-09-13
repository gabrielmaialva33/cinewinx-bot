import random

from pytgcalls import PyTgCalls

from CineWinx import userbot
from CineWinx.core.mongo import mongodb

db = mongodb.assistants

assistant_dict = {}


async def get_client(assistant: int) -> userbot:
    assistant_clients = {
        1: userbot.one,
        2: userbot.two,
        3: userbot.three,
        4: userbot.four,
        5: userbot.five,
        6: userbot.six,
        7: userbot.seven,
        8: userbot.eight,
        9: userbot.nine,
        10: userbot.ten,
    }
    return assistant_clients[int(assistant)]


async def save_assistant(chat_id, number):
    number = int(number)
    await db.update_one(
        {"chat_id": chat_id},
        {"$set": {"assistant": number}},
        upsert=True,
    )


async def set_assistant(chat_id) -> int:
    from CineWinx.core.userbot import assistants

    ran_assistant = random.choice(assistants)
    assistant_dict[chat_id] = ran_assistant
    await db.update_one(
        {"chat_id": chat_id},
        {"$set": {"assistant": ran_assistant}},
        upsert=True,
    )
    user_bot = await get_client(ran_assistant)
    return user_bot


async def get_assistant(chat_id: int) -> userbot:
    from CineWinx.core.userbot import assistants

    assistant = assistant_dict.get(chat_id)
    if not assistant:
        db_assistant = await db.find_one({"chat_id": chat_id})
        if not db_assistant:
            user_bot = await set_assistant(chat_id)
            return user_bot
        else:
            got_assis = db_assistant["assistant"]
            if got_assis in assistants:
                assistant_dict[chat_id] = got_assis
                user_bot = await get_client(got_assis)
                return user_bot
            else:
                user_bot = await set_assistant(chat_id)
                return user_bot
    else:
        if assistant in assistants:
            user_bot = await get_client(assistant)
            return user_bot
        else:
            user_bot = await set_assistant(chat_id)
            return user_bot


async def set_calls_assistant(chat_id) -> int:
    from CineWinx.core.userbot import assistants

    ran_assistant = random.choice(assistants)
    assistant_dict[chat_id] = ran_assistant
    await db.update_one(
        {"chat_id": chat_id},
        {"$set": {"assistant": ran_assistant}},
        upsert=True,
    )
    return ran_assistant


async def group_assistant(self, chat_id: int) -> PyTgCalls:
    from CineWinx.core.userbot import assistants

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
        2: self.two,
        3: self.three,
        4: self.four,
        5: self.five,
        6: self.six,
        7: self.seven,
        8: self.eight,
        9: self.nine,
        10: self.ten,
    }
    return self_clients[int(assis)]
