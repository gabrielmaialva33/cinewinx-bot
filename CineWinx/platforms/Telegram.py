import asyncio
import logging
import os
import time
from datetime import datetime, timedelta
from typing import Union

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
        out = [(string[i: i + n]) for i in range(0, len(string), n)]
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
                                text="🚦 Cancelar download",
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
📥 <u><b>{app.mention} telegram media downloader</b></u>

📁 <b>Tamanho total do arquivo:</b> {total_size}
✅ <b>Completado:</b> {completed_size}
📊 <b>Porcentagem:</b> {percentage[:5]}%

⚡ <b>Velocidade:</b> {speed}/s
⏳<b>Tempo decorrido:</b> {eta}"""
                    try:
                        await mystic.edit_text(text, reply_markup=upl)
                    except Exception as e:
                        logging.error(str(e))
                    left_time[message.id] = datetime.now() + timedelta(
                        seconds=self.sleep
                    )

            speed_counter[message.id] = time.time()
            left_time[message.id] = datetime.now()

            try:
                await app.download_media(
                    message.reply_to_message,
                    file_name=filename,
                    progress=progress,
                )
                await mystic.edit_text(
                    "✅ <i>Download concluído com sucesso...</i>\nProcessando arquivo agora"
                )
                downloader.pop(message.id)
            except Exception as e:
                logging.error(str(e))
                await mystic.edit_text(_["tg_2"])

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
