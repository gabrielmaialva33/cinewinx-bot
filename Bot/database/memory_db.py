from pytgcalls.types import AudioQuality, VideoQuality

audio = {}
video = {}


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
