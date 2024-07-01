import logging
from datetime import datetime, timedelta
from typing import Union

from ntgcalls import TelegramServerError
from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.exceptions import AlreadyJoinedError, NoActiveGroupCall
from pytgcalls.types import MediaStream

from Bot import app
from Bot.database import group_assistant, get_assistant, get_audio_bitrate, get_video_bitrate, remove_active_video_chat, \
    remove_active_chat, add_active_chat, music_on, add_active_video_chat, is_auto_end
from Bot.misc import db
from Bot.utils import AssistantErr
from config import API_HASH, API_ID, PRIVATE_BOT_MODE, STRING_SESSION_1, LANGUAGE
from strings import get_string

_ = get_string(LANGUAGE)

auto_end = {}
counter = {}
AUTO_END_TIME = 1


async def _clear_(chat_id: int):
    db[chat_id] = []
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)


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
        userbot = await get_assistant(chat_id)
        audio_stream_quality = await get_audio_bitrate(chat_id)
        video_stream_quality = await get_video_bitrate(chat_id)

        if video:
            stream = MediaStream(
                link,
                audio_parameters=audio_stream_quality,
                video_parameters=video_stream_quality,
            )
        else:
            if image and PRIVATE_BOT_MODE == str(True):
                stream = MediaStream(
                    link,
                    image,
                    audio_parameters=audio_stream_quality,
                    video_parameters=video_stream_quality,
                )
            else:
                stream = (
                    MediaStream(
                        link,
                        audio_parameters=audio_stream_quality,
                        video_parameters=video_stream_quality,
                    )
                    if video
                    else MediaStream(link, audio_parameters=audio_stream_quality)
                )

        try:
            await assistant.play(chat_id, stream)
        except NoActiveGroupCall:
            try:
                await self.join_assistant(original_chat_id, chat_id)
            except Exception as e:
                logging.exception(e)
                raise e
            try:
                await assistant.play(chat_id, stream)
            except Exception as e:
                logging.exception(e)
                raise AssistantErr(f"Exception : {e}")
        except AlreadyJoinedError as e:
            logging.exception(e)
            raise AssistantErr(_("assistant_3").format(userbot.mention))
        except TelegramServerError as e:
            logging.exception(e)
            raise AssistantErr(_("tg_1"))
        except Exception as e:
            if "phone.CreateGroupCall" in str(e):
                return await app.edit_text(_("call_2"))
            else:
                logging.exception(e)
                raise AssistantErr(f"Exception : {e}")
        await add_active_chat(chat_id)
        await music_on(chat_id)
        if video:
            await add_active_video_chat(chat_id)
        if await is_auto_end():
            counter[chat_id] = {}
            users = len(await assistant.get_participants(chat_id))
            if users == 1:
                auto_end[chat_id] = datetime.now() + timedelta(minutes=AUTO_END_TIME)
