import asyncio
import logging
from datetime import datetime, timedelta
from typing import Union

from ntgcalls import TelegramServerError
from pyrogram import Client
from pyrogram.errors import (
    ChatAdminRequired,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardMarkup
from pytgcalls import PyTgCalls, filters
from pytgcalls.exceptions import AlreadyJoinedError, NoActiveGroupCall
from pytgcalls.types import (
    ChatUpdate,
    GroupCallParticipant,
    MediaStream,
    StreamAudioEnded,
    Update,
)

from Bot import YouTube, app
from Bot.database import (
    add_active_chat,
    add_active_video_chat,
    get_assistant,
    get_audio_bitrate,
    get_loop,
    get_video_bitrate,
    group_assistant,
    is_auto_end,
    music_on,
    remove_active_chat,
    remove_active_video_chat,
    set_loop,
)
from Bot.misc import db
from Bot.utils import AssistantErr, telegram_markup, stream_markup

from config import (
    API_HASH,
    API_ID,
    LANGUAGE,
    PRIVATE_BOT_MODE,
    STRING_SESSION_1,
    STRING_SESSION_2,
    STRING_SESSION_3,
    STRING_SESSION_4,
    STRING_SESSION_5, STREAM_IMG_URL, TELEGRAM_AUDIO_URL, TELEGRAM_VIDEO_URL, SOUNCLOUD_IMG_URL,
)
from strings import get_string

from ..logger import log
from ..utils.stream.autoclear import auto_clean
from ..utils.thumbnails import gen_thumb

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
            name=f"{__name__}AssistantOne",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=str(STRING_SESSION_1),
        )
        self.one = PyTgCalls(self.userbot1, cache_duration=100)

        self.userbot2 = Client(
            name=f"{__name__}AssistantTwo",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=str(STRING_SESSION_2),
        )
        self.two = PyTgCalls(self.userbot2, cache_duration=100)

        self.userbot3 = Client(
            name=f"{__name__}AssistantThree",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=str(STRING_SESSION_3),
        )
        self.three = PyTgCalls(self.userbot3, cache_duration=100)

        self.userbot4 = Client(
            name=f"{__name__}AssistantFour",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=str(STRING_SESSION_4),
        )
        self.four = PyTgCalls(self.userbot4, cache_duration=100)

        self.userbot5 = Client(
            name=f"{__name__}AssistantFive",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=str(STRING_SESSION_5),
        )
        self.five = PyTgCalls(self.userbot5, cache_duration=100)

    async def join_assistant(self, original_chat_id: int, chat_id: int):
        assistant = await get_assistant(chat_id)
        try:
            try:
                get = await app.get_chat_member(chat_id, assistant.id)
            except ChatAdminRequired:
                raise AssistantErr(_["call_3"])
            if get.status == "banned" or get.status == "kicked":
                try:
                    await app.unban_chat_member(chat_id, assistant.id)
                except Exception as e:
                    logging.exception(e)
                    raise AssistantErr(
                        _["call_4"].format(
                            assistant.id, assistant.name, assistant.mention
                        )
                    )
        except UserNotParticipant:
            chat = await app.get_chat(chat_id)
            if chat.username:
                try:
                    await assistant.join_chat(chat.username)
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    raise AssistantErr(_["call_5"].format(e))
            else:
                try:
                    try:
                        try:
                            invite_link = chat.invite_link
                            if invite_link is None:
                                invite_link = await app.export_chat_invite_link(chat_id)
                        except Exception as e:
                            logging.exception(e)
                            invite_link = await app.export_chat_invite_link(chat_id)
                    except ChatAdminRequired:
                        raise AssistantErr(_["call_6"])
                    except Exception as e:
                        raise AssistantErr(e)
                    m = await app.send_message(
                        original_chat_id, _["call_7"].format(assistant.name, chat.title)
                    )
                    if invite_link.startswith("https://t.me/+"):
                        invite_link = invite_link.replace(
                            "https://t.me/+", "https://t.me/joinchat/"
                        )
                    await asyncio.sleep(1)
                    await assistant.join_chat(invite_link)
                    await m.edit_text(_["call_8"].format(app.mention))
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    raise AssistantErr(_["call_5"].format(e))

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

    async def play(self, client: PyTgCalls, chat_id: int):
        check = db.get(chat_id)
        popped = None
        loop = await get_loop(chat_id)
        try:
            if loop == 0:
                popped = check.pop(0)
            else:
                loop = loop - 1
                await set_loop(chat_id, loop)
            if popped:
                await auto_clean(popped)
            if not check:
                await _clear_(chat_id)
                return await client.leave_call(chat_id)
        except Exception as e:
            logging.exception(e)
            try:
                await _clear_(chat_id)
                return await client.leave_call(chat_id)
            except Exception as e:
                logging.exception(e)
                return
        else:
            queued = check[0]["file"]
            title = (check[0]["title"]).title()
            user = check[0]["by"]
            original_chat_id = check[0]["chat_id"]
            streamtype = check[0]["streamtype"]

            audio_stream_quality = await get_audio_bitrate(chat_id)
            video_stream_quality = await get_video_bitrate(chat_id)

            videoid = check[0]["vidid"]
            userid = check[0].get("user_id")
            check[0]["played"] = 0
            video = True if str(streamtype) == "video" else False

            if "live_" in queued:
                n, link = await YouTube.video(videoid, True)
                if n == 0:
                    return await app.send_message(
                        original_chat_id,
                        text=_["stream_2"],
                    )
                if video:
                    stream = MediaStream(
                        link,
                        audio_parameters=audio_stream_quality,
                        video_parameters=video_stream_quality,
                    )
                else:
                    try:
                        image = await YouTube.thumbnail(videoid, True)
                    except Exception as e:
                        logging.exception(e)
                        image = None
                    if image and PRIVATE_BOT_MODE == str(True):
                        stream = MediaStream(
                            link,
                            image,
                            audio_parameters=audio_stream_quality,
                            video_parameters=video_stream_quality,
                        )
                    else:
                        stream = MediaStream(
                            link,
                            audio_parameters=audio_stream_quality,
                        )
                try:
                    await client.play(chat_id, stream)
                except Exception as e:
                    logging.exception(e)
                    return await app.send_message(
                        original_chat_id,
                        text=_["stream_2"],
                    )
                img = await gen_thumb(videoid)
                button = telegram_markup(_, chat_id)
                run = await app.send_photo(
                    original_chat_id,
                    photo=img,
                    caption=_["stream_1"].format(
                        title[:27],
                        f"https://t.me/{app.username}?start=info_{videoid}",
                        check[0]["dur"],
                        user,
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            elif "vid_" in queued:
                mystic = await app.send_message(original_chat_id, _["play_1"])
                try:
                    file_path, direct = await YouTube.download(
                        videoid,
                        mystic,
                        videoid=True,
                        video=True if str(streamtype) == "video" else False,
                    )
                except Exception as e:
                    logging.exception(e)
                    return await mystic.edit_text(
                        _["stream_2"], disable_web_page_preview=True
                    )
                if video:
                    stream = MediaStream(
                        file_path,
                        audio_parameters=audio_stream_quality,
                        video_parameters=video_stream_quality,
                    )
                else:
                    try:
                        image = await YouTube.thumbnail(videoid, True)
                    except Exception as e:
                        logging.exception(e)
                        image = None
                    if image and PRIVATE_BOT_MODE == str(True):
                        stream = MediaStream(
                            file_path,
                            image,
                            audio_parameters=audio_stream_quality,
                            video_parameters=video_stream_quality,
                        )
                    else:
                        stream = MediaStream(
                            file_path,
                            audio_parameters=audio_stream_quality,
                        )
                try:
                    await client.play(chat_id, stream)
                except Exception as e:
                    logging.exception(e)
                    return await app.send_message(
                        original_chat_id,
                        text=_["stream_2"],
                    )
                img = await gen_thumb(videoid)
                button = stream_markup(_, videoid, chat_id)
                await mystic.delete()
                run = await app.send_photo(
                    original_chat_id,
                    photo=img,
                    caption=_["stream_1"].format(
                        title[:27],
                        f"https://t.me/{app.username}?start=info_{videoid}",
                        check[0]["dur"],
                        user,
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"
            elif "index_" in queued:
                stream = (
                    MediaStream(
                        videoid,
                        audio_parameters=audio_stream_quality,
                        video_parameters=video_stream_quality,
                    )
                    if str(streamtype) == "video"
                    else MediaStream(videoid, audio_parameters=audio_stream_quality)
                )
                try:
                    await client.play(chat_id, stream)
                except Exception as e:
                    logging.exception(e)
                    return await app.send_message(
                        original_chat_id,
                        text=_["stream_2"],
                    )
                button = telegram_markup(_, chat_id)
                run = await app.send_photo(
                    original_chat_id,
                    photo=STREAM_IMG_URL,
                    caption=_["stream_2"].format(user),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            else:
                if videoid == "telegram":
                    image = None
                elif videoid == "soundcloud":
                    image = None
                else:
                    try:
                        image = await YouTube.thumbnail(videoid, True)
                    except Exception as e:
                        logging.exception(e)
                        image = None
                if video:
                    stream = MediaStream(
                        queued,
                        audio_parameters=audio_stream_quality,
                        video_parameters=video_stream_quality,
                    )
                else:
                    if image and PRIVATE_BOT_MODE == str(True):
                        stream = MediaStream(
                            queued,
                            image,
                            audio_parameters=audio_stream_quality,
                            video_parameters=video_stream_quality,
                        )
                    else:
                        stream = MediaStream(
                            queued,
                            audio_parameters=audio_stream_quality,
                        )
                try:
                    await client.play(chat_id, stream)
                except Exception as e:
                    logging.exception(e)
                    return await app.send_message(
                        original_chat_id,
                        text=_["stream_2"],
                    )
                if videoid == "telegram":
                    button = telegram_markup(_, chat_id)
                    run = await app.send_photo(
                        original_chat_id,
                        photo=(
                            TELEGRAM_AUDIO_URL
                            if str(streamtype) == "audio"
                            else TELEGRAM_VIDEO_URL
                        ),
                        caption=_["stream_3"].format(title, check[0]["dur"], user),
                        reply_markup=InlineKeyboardMarkup(button),
                    )
                    db[chat_id][0]["mystic"] = run
                    db[chat_id][0]["markup"] = "tg"
                elif videoid == "soundcloud":
                    button = telegram_markup(_, chat_id)
                    run = await app.send_photo(
                        original_chat_id,
                        photo=SOUNCLOUD_IMG_URL,
                        caption=_["stream_3"].format(title, check[0]["dur"], user),
                        reply_markup=InlineKeyboardMarkup(button),
                    )
                    db[chat_id][0]["mystic"] = run
                    db[chat_id][0]["markup"] = "tg"
                else:
                    img = await gen_thumb(videoid)
                    button = stream_markup(_, videoid, chat_id)
                    run = await app.send_photo(
                        original_chat_id,
                        photo=img,
                        caption=_["stream_1"].format(
                            title[:27],
                            f"https://t.me/{app.username}?start=info_{videoid}",
                            check[0]["dur"],
                            user,
                        ),
                        reply_markup=InlineKeyboardMarkup(button),
                    )
                    db[chat_id][0]["mystic"] = run
                    db[chat_id][0]["markup"] = "stream"

    async def ping(self):
        """
        Get the average ping of all the assistants
        :return:
        """
        pings = []
        if STRING_SESSION_1:
            pings.append(self.one.ping)
        if STRING_SESSION_2:
            pings.append(self.two.ping)
        if STRING_SESSION_3:
            pings.append(self.three.ping)
        if STRING_SESSION_4:
            pings.append(self.four.ping)
        if STRING_SESSION_5:
            pings.append(self.five.ping)
        return str(round(sum(pings) / len(pings), 3))

    async def start(self):
        """
        Start the PyTgCalls Assistants
        :return:
        """
        log(__name__).info("Starting PyTgCalls Assistants")
        if STRING_SESSION_1:
            await self.one.start()
        if STRING_SESSION_2:
            await self.two.start()
        if STRING_SESSION_3:
            await self.three.start()
        if STRING_SESSION_4:
            await self.four.start()
        if STRING_SESSION_5:
            await self.five.start()
        log(__name__).info("PyTgCalls Assistants Started")

    async def decorators(self):
        """
        Decorators for the PyTgCalls Assistants
        :return:
        """

        @self.one.on_update(filters.chat_update(ChatUpdate.Status.LEFT_CALL))
        @self.two.on_update(filters.chat_update(ChatUpdate.Status.LEFT_CALL))
        @self.three.on_update(filters.chat_update(ChatUpdate.Status.LEFT_CALL))
        @self.four.on_update(filters.chat_update(ChatUpdate.Status.LEFT_CALL))
        @self.five.on_update(filters.chat_update(ChatUpdate.Status.LEFT_CALL))
        async def stream_services_handler(_, chat_id: int):
            await self.stop_stream(chat_id)

        @self.one.on_update(filters.stream_end)
        @self.two.on_update(filters.stream_end)
        @self.three.on_update(filters.stream_end)
        @self.four.on_update(filters.stream_end)
        @self.five.on_update(filters.stream_end)
        async def stream_end_handler(client, update: Update):
            if not isinstance(update, StreamAudioEnded):
                return
            await self.play(client, update.chat_id)

        @self.one.on_update(filters.chat_update(GroupCallParticipant.Action.UPDATED))
        @self.two.on_update(filters.chat_update(GroupCallParticipant.Action.UPDATED))
        @self.three.on_update(filters.chat_update(GroupCallParticipant.Action.UPDATED))
        @self.four.on_update(filters.chat_update(GroupCallParticipant.Action.UPDATED))
        @self.five.on_update(filters.chat_update(GroupCallParticipant.Action.UPDATED))
        async def participants_change_handler(client, update: Update):
            if not isinstance(
                update, GroupCallParticipant.Action.JOINED
            ) and not isinstance(update, GroupCallParticipant.Action.LEFT):
                return
            chat_id = update.chat_id
            users = counter.get(chat_id)
            if not users:
                try:
                    got = len(await client.get_participants(chat_id))
                except Exception as e:
                    logging.exception(e)
                    return
                counter[chat_id] = got
                if got == 1:
                    auto_end[chat_id] = datetime.now() + timedelta(
                        minutes=AUTO_END_TIME
                    )
                    return
                auto_end[chat_id] = {}
            else:
                final = (
                    users + 1
                    if isinstance(update, GroupCallParticipant.Action.JOINED)
                    else users - 1
                )
                counter[chat_id] = final
                if final == 1:
                    auto_end[chat_id] = datetime.now() + timedelta(
                        minutes=AUTO_END_TIME
                    )
                    return
                auto_end[chat_id] = {}


call = Call()
