from typing import Union

from pyrogram import Client
from pytgcalls import PyTgCalls

from Bot.database import group_assistant
from Bot.database.memory_db import get_audio_bitrate, get_video_bitrate
from config import API_HASH, API_ID, STRING_SESSION_1


class Call(PyTgCalls):
    def __init__(self):
        self.userbot1 = Client(
            name="Assistant1",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=str(STRING_SESSION_1),
        )
        self.one = PyTgCalls(self.userbot1, cache_duration=100)

    async def join_call(
            self,
            chat_id: int,
            original_chat_id: int,
            link: str,
            video: Union[bool, str] = None,
            image: Union[bool, str] = None,
    ):
        assistant = await group_assistant(self, chat_id)
        audio_stream_quality = await get_audio_bitrate(chat_id)
        video_stream_quality = await get_video_bitrate(chat_id)
