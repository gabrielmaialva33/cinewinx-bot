import asyncio
import logging
import os
import time
from datetime import datetime, timedelta
from typing import Union

from pyrogram.errors import FloodWait
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Voice,
    Message,
    Video,
    Audio,
)

import config
from CineWinx import app
from config import lyrical
from ..utils.formatters import convert_bytes, get_readable_time, seconds_to_min

downloader = {}


class TeleAPI:
    def __init__(self):
        self.chars_limit = 4096
        self.sleep = config.TELEGRAM_DOWNLOAD_EDIT_SLEEP

    async def send_split_text(self, message: Message, string: str):
        n = self.chars_limit
        out = [(string[i : i + n]) for i in range(0, len(string), n)]
        j = 0
        for x in out:
            if j <= 2:
                j += 1
                await message.reply_text(x)
        return True

    async def get_link(self, message: Message):
        if message.chat.username:
            link = f"https://t.me/{message.chat.username}/{message.reply_to_message.id}"
        else:
            xf = str(message.chat.id)[4:]
            link = f"https://t.me/c/{xf}/{message.reply_to_message.id}"
        return link

    async def get_link_2(self, message: Message):
        if message.chat.username:
            link = f"https://t.me/{message.chat.username}/{message.id}"
        else:
            xf = str(message.chat.id)[4:]
            link = f"https://t.me/c/{xf}/{message.id}"
        return link

    async def get_filename(self, file, audio: Audio = None):
        try:
            file_name = file.file_name
            if file_name is None:
                file_name = (
                    "🎵 telegram audio file" if audio else "🎥 telegram video file"
                )

        except AttributeError as e:
            logging.error(str(e))
            file_name = "🎵 telegram audio file" if audio else "🎥 telegram video file"
        return file_name

    async def get_duration(self, file: Union[Audio, Video]):
        try:
            dur = seconds_to_min(file.duration)
        except AttributeError as e:
            logging.error(str(e))
            dur = "0:00"
        return dur

    async def get_filepath(
        self,
        audio: Audio = None,
        video: Video = None,
    ):
        if audio:
            try:
                file_name = (
                    audio.file_unique_id
                    + "."
                    + (
                        (audio.file_name.split(".")[-1])
                        if (not isinstance(audio, Voice))
                        else "ogg"
                    )
                )
            except Exception as e:
                logging.error(str(e))
                file_name = audio.file_unique_id + "." + ".ogg"
            file_name = os.path.join(os.path.realpath("downloads"), file_name)
        if video:
            try:
                file_name = (
                    video.file_unique_id + "." + (video.file_name.split(".")[-1])
                )
            except Exception as e:
                logging.error(str(e))
                file_name = video.file_unique_id + "." + "mp4"
            file_name = os.path.join(os.path.realpath("downloads"), file_name)
        return file_name

    async def download(self, _, message: Message, mystic: Message, filename: str):
        left_time = {}
        speed_counter = {}
        if os.path.exists(filename):
            return True

        async def down_load():
            async def progress(current: int, total: int):
                if current == total:
                    return
                current_time = time.time()
                start_time = speed_counter.get(message.id)
                check_time = current_time - start_time
                upl = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="🚦 𝗖𝗮𝗻𝗰𝗲𝗹𝗮𝗿 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱",
                                callback_data="stop_downloading",
                            ),
                        ]
                    ]
                )
                if datetime.now() > left_time.get(message.id):
                    percentage = current * 100 / total
                    percentage = str(round(percentage, 2))
                    speed = current / check_time
                    eta = int((total - current) / speed)
                    downloader[message.id] = eta
                    eta = get_readable_time(eta)
                    if not eta:
                        eta = "0 sec"
                    total_size = convert_bytes(total)
                    completed_size = convert_bytes(current)
                    speed = convert_bytes(speed)
                    text = f"""
📥 <b>{app.mention} 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗺 𝗠𝗲𝗱𝗶𝗮 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱𝗲𝗿</b>

📁 <b>𝗧𝗮𝗺𝗮𝗻𝗵𝗼:</b> {total_size}
✅ <b>𝗖𝗼𝗺𝗽𝗹𝗲𝘁𝗮𝗱𝗼:</b> {completed_size}
📊 <b>𝗣𝗼𝗿𝗰𝗲𝗻𝘁𝗮𝗴𝗲𝗺:</b> {percentage[:5]}%

⚡ <b>𝗩𝗲𝗹𝗼𝗰𝗶𝗱𝗮𝗱𝗲:</b> {speed}/s
⏳ <b>𝗧𝗲𝗺𝗽𝗼 𝗱𝗲𝗰𝗼𝗿𝗿𝗶𝗱𝗼:</b> {eta}"""
                    try:
                        await mystic.edit_text(text, reply_markup=upl)
                    except Exception as ex:
                        logging.error(str(ex))
                    left_time[message.id] = datetime.now() + timedelta(
                        seconds=self.sleep
                    )

            speed_counter[message.id] = time.time()
            left_time[message.id] = datetime.now()

            try:
                await app.download_media(
                    message or message.reply_to_message,
                    file_name=filename,
                    progress=progress,
                )
                await mystic.edit_text(
                    "✅ <i>𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗰𝗼𝗻𝗰𝗹𝘂𝗶́𝗱𝗼 𝗰𝗼𝗺 𝘀𝘂𝗰𝗲𝘀𝘀𝗼...</i>\n𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗮𝗻𝗱𝗼 𝗮𝗿𝗾𝘂𝗶𝘃𝗼 𝗮𝗴𝗼𝗿𝗮"
                )
                downloader.pop(message.id)
            except Exception as err:
                logging.error(str(err))
                try:
                    await mystic.edit_text(_["tg_2"])
                except FloodWait as ex:
                    await asyncio.sleep(ex.value)
                except Exception as exx:
                    logging.error(str(exx))


        if len(downloader) > 10:
            timers = []
            for x in downloader:
                timers.append(downloader[x])
            try:
                low = min(timers)
                eta = get_readable_time(low)
            except Exception as e:
                logging.error(str(e))
                eta = "0 sec"
            await mystic.edit_text(_["tg_1"].format(eta))
            return False

        task = asyncio.create_task(down_load())
        lyrical[mystic.id] = task
        await task
        downloaded = downloader.get(message.id)
        if downloaded:
            downloader.pop(message.id)
            return False
        verify = lyrical.get(mystic.id)
        if not verify:
            return False
        lyrical.pop(mystic.id)
        return True
