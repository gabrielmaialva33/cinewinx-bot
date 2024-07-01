from pytgcalls.types import AudioQuality, VideoQuality

from Bot.core.mongo import mongodb

auto_end_db = mongodb.autoend

audio = {}
video = {}
pause = {}
auto_end = {}

active = []
active_video = []


# auto end stream
async def is_auto_end() -> bool:
    chat_id = 123
    mode = auto_end.get(chat_id)
    if not mode:
        user = await auto_end_db.find_one({"chat_id": chat_id})
        if not user:
            auto_end[chat_id] = False
            return False
        auto_end[chat_id] = True
        return True
    return mode


async def auto_end_on():
    chat_id = 123
    auto_end[chat_id] = True
    user = await auto_end_db.find_one({"chat_id": chat_id})
    if not user:
        return await auto_end_db.insert_one({"chat_id": chat_id})


async def auto_end_off():
    chat_id = 123
    auto_end[chat_id] = False
    user = await auto_end_db.find_one({"chat_id": chat_id})
    if user:
        return await auto_end_db.delete_one({"chat_id": chat_id})


# pause-skip
async def music_on(chat_id: int):
    """
    Set the music to on
    :param chat_id:
    :return:
    """
    pause[chat_id] = True


# audio and video bitrate
async def save_audio_bitrate(chat_id: int, bitrate: str):
    """
    Save the audio bitrate to the chat_id
    :param chat_id:
    :param bitrate:
    :return:
    """
    audio[chat_id] = bitrate


async def save_video_bitrate(chat_id: int, bitrate: str):
    """
    Save the video bitrate to the chat_id
    :param chat_id:
    :param bitrate:
    :return:
    """
    video[chat_id] = bitrate


async def get_audio_bitrate(chat_id: int) -> AudioQuality:
    """
    Get the audio bitrate based on the chat_id
    :param chat_id:
    :return:
    """
    mode = audio.get(chat_id)
    audio_qualities = {
        "STUDIO": AudioQuality.STUDIO,
        "HIGH": AudioQuality.HIGH,
        "MEDIUM": AudioQuality.MEDIUM,
        "LOW": AudioQuality.LOW,
    }
    return audio_qualities.get(mode, AudioQuality.MEDIUM)


async def get_video_bitrate(chat_id: int) -> VideoQuality:
    """
    Get the video bitrate based on the chat_id
    :param chat_id:
    :return:
    """
    mode = video.get(chat_id)
    video_qualities = {
        "UHD_4K": VideoQuality.UHD_4K,
        "QHD_2K": VideoQuality.QHD_2K,
        "FHD_1080p": VideoQuality.FHD_1080p,
        "HD_720p": VideoQuality.HD_720p,
        "SD_480p": VideoQuality.SD_480p,
        "SD_360p": VideoQuality.SD_360p,
    }
    return video_qualities.get(mode, VideoQuality.HD_720p)


# active video chats
async def add_active_chat(chat_id: int):
    """
    Add the chat_id to the active list
    :param chat_id:
    :return:
    """
    if chat_id not in active:
        active.append(chat_id)


async def add_active_video_chat(chat_id: int):
    """
    Add the chat_id to the active_video list
    :param chat_id:
    :return:
    """
    if chat_id not in active_video:
        active_video.append(chat_id)


async def remove_active_video_chat(chat_id: int):
    """
    Remove the chat_id from the active_video list
    :param chat_id:
    :return:
    """
    if chat_id in active_video:
        active_video.remove(chat_id)


async def remove_active_chat(chat_id: int):
    """
    Remove the chat_id from the active list
    :param chat_id:
    :return:
    """
    if chat_id in active:
        active.remove(chat_id)
