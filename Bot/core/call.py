from typing import Union

from pyrogram import Client
from pytgcalls import PyTgCalls

from Bot.database import group_assistant
from config import STRING_SESSION_1, API_ID, API_HASH


class Call(PyTgCalls):
    def __init__(self):
        self.userbot1 = Client(
            name="Assistant1",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=str(STRING_SESSION_1),
        )
        self.one = PyTgCalls(self.userbot1, cache_duration=100)

    async def join_call(self, chat_id: int, original_chat_id: int, link: str, video: Union[bool, str] = None,
                        image: Union[bool, str] = None):
        assistant = await group_assistant(self, chat_id)
