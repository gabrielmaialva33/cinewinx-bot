import logging
from typing import Any

from pytgcalls.types import AudioQuality, VideoQuality

from Bot.core.mongo import mongodb

auto_end_db = mongodb.autoend
channel_db = mongodb.cplaymode
playmode_db = mongodb.playmode
playtype_db = mongodb.playtype

loop = {}
audio = {}
video = {}
pause = {}
auto_end = {}
play_mode = {}
play_type = {}
channel_connect = {}

active = []
active_video = []
command = []


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


async def get_active_chats() -> list:
    return active


async def is_active_chat(chat_id: int) -> bool:
    if chat_id not in active:
        return False
    else:
        return True


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


# loop
async def get_loop(chat_id: int) -> int:
    lop = loop.get(chat_id)
    if not lop:
        return 0
    return lop


async def set_loop(chat_id: int, mode: int):
    loop[chat_id] = mode


# delete command mode
async def is_command_delete_on(chat_id: int) -> bool:
    if chat_id not in command:
        return True
    else:
        return False


async def command_delete_off(chat_id: int):
    if chat_id not in command:
        command.append(chat_id)


async def command_delete_on(chat_id: int):
    try:
        command.remove(chat_id)
    except Exception as e:
        logging.error(e)


# channel play mode
async def get_cmode(chat_id: int) -> Any | None:
    """
    Get the channel play mode
    :param chat_id:
    :return:
    """
    mode = channel_connect.get(chat_id)
    if not mode:
        mode = await channel_db.find_one({"chat_id": chat_id})
        if not mode:
            return None
        channel_connect[chat_id] = mode["mode"]
        return mode["mode"]
    return mode


async def set_cmode(chat_id: int, mode: int):
    """
    Set the channel play mode
    :param chat_id:
    :param mode:
    :return:
    """
    channel_connect[chat_id] = mode
    await channel_db.update_one(
        {"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True
    )


# play mode and play type
async def get_playmode(chat_id: int) -> str:
    mode = play_mode.get(chat_id)
    if not mode:
        mode = await playmode_db.find_one({"chat_id": chat_id})
        if not mode:
            play_mode[chat_id] = "Direct"
            return "Direct"
        play_mode[chat_id] = mode["mode"]
        return mode["mode"]
    return mode


async def set_playmode(chat_id: int, mode: str):
    play_mode[chat_id] = mode
    await playmode_db.update_one(
        {"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True
    )


async def get_playtype(chat_id: int) -> str:
    mode = play_type.get(chat_id)
    if not mode:
        mode = await playtype_db.find_one({"chat_id": chat_id})
        if not mode:
            play_type[chat_id] = "Everyone"
            return "Everyone"
        play_type[chat_id] = mode["mode"]
        return mode["mode"]
    return mode


async def set_playtype(chat_id: int, mode: str):
    play_type[chat_id] = mode
    await playtype_db.update_one(
        {"chat_id": chat_id}, {"$set": {"mode": mode}}, upsert=True
    )
