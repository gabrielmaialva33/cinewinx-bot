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
    FloodWait,
)
from pyrogram.types import InlineKeyboardMarkup
from pytgcalls import PyTgCalls, filters
from pytgcalls.exceptions import AlreadyJoinedError, NoActiveGroupCall
from pytgcalls.types import (
    MediaStream,
    Update,
    ChatUpdate,
    GroupCallParticipant,
)
from pytgcalls.types.stream import StreamAudioEnded

import config
from CineWinx import LOGGER, YouTube, app
from CineWinx.misc import db
from CineWinx.utils.database import (
    add_active_chat,
    add_active_video_chat,
    get_assistant,
    get_audio_bitrate,
    get_lang,
    get_loop,
    get_video_bitrate,
    group_assistant,
    is_autoend,
    music_on,
    remove_active_chat,
    remove_active_video_chat,
    set_loop,
)
from CineWinx.utils.exceptions import AssistantErr
from CineWinx.utils.inline.play import stream_markup, telegram_markup
from CineWinx.utils.stream.autoclear import auto_clean
from CineWinx.utils.thumbnails import gen_thumb
from strings import get_string

autoend = {}
counter = {}
AUTO_END_TIME = 1


async def _clear_(chat_id):
    db[chat_id] = []
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)


class Call(PyTgCalls):
    def __init__(self):
        self.userbot1 = Client(
            name="WinxString1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
        )
        self.one = PyTgCalls(
            self.userbot1,
            cache_duration=100,
        )
        self.userbot2 = Client(
            name="WinxString2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
        )
        self.two = PyTgCalls(
            self.userbot2,
            cache_duration=100,
        )
        self.userbot3 = Client(
            name="WinxString3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
        )
        self.three = PyTgCalls(
            self.userbot3,
            cache_duration=100,
        )
        self.userbot4 = Client(
            name="WinxString4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
        )
        self.four = PyTgCalls(
            self.userbot4,
            cache_duration=100,
        )
        self.userbot5 = Client(
            name="WinxString5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
        )
        self.five = PyTgCalls(
            self.userbot5,
            cache_duration=100,
        )

    async def pause_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.pause_stream(chat_id)

    async def resume_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.resume_stream(chat_id)

    async def mute_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.mute_stream(chat_id)

    async def unmute_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.unmute_stream(chat_id)

    async def stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        try:
            await _clear_(chat_id)
            await assistant.leave_call(chat_id)
        except:
            pass

    async def set_volume(self, chat_id: int, volume: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.change_volume_call(chat_id, volume)

    async def get_participant(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.get_participants(chat_id)

    async def force_stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        try:
            check = db.get(chat_id)
            check.pop(0)
        except:
            pass
        await remove_active_video_chat(chat_id)
        await remove_active_chat(chat_id)
        try:
            await assistant.leave_call(chat_id)
        except:
            pass

    async def skip_stream(
        self,
        chat_id: int,
        link: str,
        video: Union[bool, str] = None,
        image: Union[bool, str] = None,
    ):
        assistant = await group_assistant(self, chat_id)
        audio_stream_quality = await get_audio_bitrate(chat_id)
        video_stream_quality = await get_video_bitrate(chat_id)
        if video:
            stream = MediaStream(
                link,
                audio_parameters=audio_stream_quality,
                video_parameters=video_stream_quality,
            )
        else:
            stream = MediaStream(link, audio_parameters=audio_stream_quality)
        await assistant.change_stream(
            chat_id,
            stream,
        )

    async def seek_stream(self, chat_id, file_path, to_seek, duration, mode):
        assistant = await group_assistant(self, chat_id)
        audio_stream_quality = await get_audio_bitrate(chat_id)
        video_stream_quality = await get_video_bitrate(chat_id)
        stream = (
            MediaStream(
                file_path,
                audio_parameters=audio_stream_quality,
                video_parameters=video_stream_quality,
                ffmpeg_parameters=f"-ss {to_seek} -to {duration}",
            )
            if mode == "video"
            else MediaStream(
                file_path,
                audio_parameters=audio_stream_quality,
                ffmpeg_parameters=f"-ss {to_seek} -to {duration}",
                video_flags=MediaStream.IGNORE,
            )
        )
        await assistant.change_stream(chat_id, stream)

    async def stream_call(self, link):
        assistant = await group_assistant(self, config.LOG_GROUP_ID)
        await assistant.play(
            config.LOG_GROUP_ID,
            MediaStream(link),
        )
        await asyncio.sleep(0.5)
        await assistant.leave_call(config.LOG_GROUP_ID)

    async def join_assistant(self, original_chat_id, chat_id):
        language = await get_lang(original_chat_id)
        _ = get_string(language)
        userbot = await get_assistant(chat_id)
        try:
            try:
                get = await app.get_chat_member(chat_id, userbot.id)
            except ChatAdminRequired:
                raise AssistantErr(_["call_1"])
            if get.status == "banned" or get.status == "kicked":
                try:
                    await app.unban_chat_member(chat_id, userbot.id)
                except:
                    raise AssistantErr(
                        _["call_2"].format(
                            app.mention,
                            userbot.id,
                            userbot.mention,
                            userbot.username,
                        ),
                    )
        except UserNotParticipant:
            chat = await app.get_chat(chat_id)
            if chat.username:
                try:
                    await userbot.join_chat(chat.username)
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    raise AssistantErr(_["call_3"].format(e))
            else:
                try:
                    try:
                        try:
                            invitelink = chat.invite_link
                            if invitelink is None:
                                invitelink = await app.export_chat_invite_link(chat_id)
                        except:
                            invitelink = await app.export_chat_invite_link(chat_id)
                    except ChatAdminRequired:
                        raise AssistantErr(_["call_4"])
                    except Exception as e:
                        raise AssistantErr(e)
                    m = await app.send_message(
                        original_chat_id, _["call_5"].format(userbot.name, chat.title)
                    )
                    if invitelink.startswith("https://t.me/+"):
                        invitelink = invitelink.replace(
                            "https://t.me/+", "https://t.me/joinchat/"
                        )
                    await asyncio.sleep(1)
                    await userbot.join_chat(invitelink)
                    await m.edit_text(_["call_6"].format(app.mention))
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    raise AssistantErr(_["call_3"].format(e))

    async def join_call(
        self,
        chat_id: int,
        original_chat_id: int,
        link,
        video: Union[bool, str] = None,
        image: Union[bool, str] = None,
    ):
        assistant = await group_assistant(self, chat_id)
        audio_stream_quality = await get_audio_bitrate(chat_id)
        video_stream_quality = await get_video_bitrate(chat_id)
        if video:
            stream = MediaStream(
                link,
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
            await assistant.play(
                chat_id,
                stream,
            )
        except NoActiveGroupCall:
            try:
                await self.join_assistant(original_chat_id, chat_id)
            except Exception as e:
                raise e
            try:
                await assistant.play(
                    chat_id,
                    stream,
                )
            except Exception as e:
                raise AssistantErr(
                    "Nenhum chat de vídeo ativo encontrado\n\nPor favor, certifique-se de que você iniciou o chat de "
                    "vídeo."
                )
        except AlreadyJoinedError:
            raise AssistantErr(
                "Assistente já está no chat de vídeo\n\nO sistema de bot de música detectou que o assistente já está "
                "no chat de vídeo. Se esse problema continuar, reinicie o chat de vídeo e tente novamente."
            )
        except TelegramServerError:
            raise AssistantErr(
                "Erro do servidor do Telegram\n\nPor favor, desligue e reinicie o chat de vídeo novamente."
            )
        except Exception as e:
            logging.error(e)
            if "phone.CreateGroupCall" in str(e):
                try:
                    await self.join_assistant(original_chat_id, chat_id)
                except Exception as e:
                    raise e
                try:
                    await assistant.play(
                        chat_id,
                        stream,
                    )
                except Exception:
                    raise AssistantErr(
                        "Nenhum chat de vídeo ativo encontrado\n\n"
                        "Por favor, certifique-se de que você iniciou o chat de vídeo."
                    )
        await add_active_chat(chat_id)
        await music_on(chat_id)
        if video:
            await add_active_video_chat(chat_id)
        if await is_autoend():
            counter[chat_id] = {}
            users = len(await assistant.get_participants(chat_id))
            if users == 1:
                autoend[chat_id] = datetime.now() + timedelta(minutes=AUTO_END_TIME)

    async def change_stream(self, client: Client, chat_id: int):
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
        except:
            try:
                await _clear_(chat_id)
                return await client.leave_call(chat_id)
            except:
                return
        else:
            queued = check[0]["file"]
            language = await get_lang(chat_id)
            _ = get_string(language)
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
                        text=_["call_7"],
                    )
                if video:
                    stream = MediaStream(
                        link,
                        audio_parameters=audio_stream_quality,
                        video_parameters=video_stream_quality,
                    )
                else:
                    stream = MediaStream(
                        link,
                        audio_parameters=audio_stream_quality,
                    )
                try:
                    await client.change_stream(chat_id, stream)
                except Exception:
                    return await app.send_message(
                        original_chat_id,
                        text=_["call_7"],
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
                mystic = await app.send_message(original_chat_id, _["call_8"])
                try:
                    file_path, direct = await YouTube.download(
                        videoid,
                        mystic,
                        videoid=True,
                        video=True if str(streamtype) == "video" else False,
                    )
                except:
                    return await mystic.edit_text(
                        _["call_7"], disable_web_page_preview=True
                    )
                if video:
                    stream = MediaStream(
                        file_path,
                        audio_parameters=audio_stream_quality,
                        video_parameters=video_stream_quality,
                    )
                else:
                    stream = MediaStream(
                        file_path,
                        audio_parameters=audio_stream_quality,
                    )
                try:
                    await client.change_stream(chat_id, stream)
                except Exception:
                    return await app.send_message(
                        original_chat_id,
                        text=_["call_7"],
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
                    await client.change_stream(chat_id, stream)
                except Exception:
                    return await app.send_message(
                        original_chat_id,
                        text=_["call_7"],
                    )
                button = telegram_markup(_, chat_id)
                run = await app.send_photo(
                    original_chat_id,
                    photo=config.STREAM_IMG_URL,
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
                    except:
                        image = None
                if video:
                    stream = MediaStream(
                        queued,
                        audio_parameters=audio_stream_quality,
                        video_parameters=video_stream_quality,
                    )
                else:
                    stream = MediaStream(
                        queued,
                        audio_parameters=audio_stream_quality,
                    )
                try:
                    await client.change_stream(chat_id, stream)
                except Exception as e:
                    logging.error(e)
                    return await app.send_message(
                        original_chat_id,
                        text=_["call_7"],
                    )
                if videoid == "telegram":
                    button = telegram_markup(_, chat_id)
                    run = await app.send_photo(
                        original_chat_id,
                        photo=(
                            config.TELEGRAM_AUDIO_URL
                            if str(streamtype) == "audio"
                            else config.TELEGRAM_VIDEO_URL
                        ),
                        caption=_["stream_1"].format(
                            title, config.SUPPORT_GROUP, check[0]["dur"], user
                        ),
                        reply_markup=InlineKeyboardMarkup(button),
                    )
                    db[chat_id][0]["mystic"] = run
                    db[chat_id][0]["markup"] = "tg"
                elif videoid == "soundcloud":
                    button = telegram_markup(_, chat_id)
                    run = await app.send_photo(
                        original_chat_id,
                        photo=config.SOUNCLOUD_IMG_URL,
                        caption=_["stream_1"].format(
                            title, config.SUPPORT_GROUP, check[0]["dur"], user
                        ),
                        reply_markup=InlineKeyboardMarkup(button),
                    )
                    db[chat_id][0]["mystic"] = run
                    db[chat_id][0]["markup"] = "tg"
                else:
                    img = await gen_thumb(videoid)
                    button = stream_markup(_, videoid, chat_id)
                    try:
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
                    except FloodWait as e:
                        await asyncio.sleep(e.value)
                    db[chat_id][0]["mystic"] = run
                    db[chat_id][0]["markup"] = "stream"

    async def ping(self):
        pings = []
        if config.STRING1:
            pings.append(self.one.ping)
        if config.STRING2:
            pings.append(self.two.ping)
        if config.STRING3:
            pings.append(self.three.ping)
        if config.STRING4:
            pings.append(self.four.ping)
        if config.STRING5:
            pings.append(self.five.ping)
        return str(round(sum(pings) / len(pings), 3))

    async def start(self):
        LOGGER(__name__).info("Starting PyTgCalls Client\n")
        if config.STRING1:
            await self.one.start()
        if config.STRING2:
            await self.two.start()
        if config.STRING3:
            await self.three.start()
        if config.STRING4:
            await self.four.start()
        if config.STRING5:
            await self.five.start()

    async def decorators(self):
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
            await self.change_stream(client, update.chat_id)

        @self.one.on_update(
            filters.call_participant(GroupCallParticipant.Action.UPDATED)
        )
        @self.two.on_update(
            filters.call_participant(GroupCallParticipant.Action.UPDATED)
        )
        @self.three.on_update(
            filters.call_participant(GroupCallParticipant.Action.UPDATED)
        )
        @self.four.on_update(
            filters.call_participant(GroupCallParticipant.Action.UPDATED)
        )
        @self.five.on_update(
            filters.call_participant(GroupCallParticipant.Action.UPDATED)
        )
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
                    logging.error(e)
                    return
                counter[chat_id] = got
                if got == 1:
                    autoend[chat_id] = datetime.now() + timedelta(minutes=AUTO_END_TIME)
                    return
                autoend[chat_id] = {}
            else:
                final = (
                    users + 1
                    if isinstance(update, GroupCallParticipant.Action.JOINED)
                    else users - 1
                )
                counter[chat_id] = final
                if final == 1:
                    autoend[chat_id] = datetime.now() + timedelta(minutes=AUTO_END_TIME)
                    return
                autoend[chat_id] = {}


CineWinx = Call()
