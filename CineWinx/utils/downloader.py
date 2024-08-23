from os import path
import yt_dlp

from CineWinx import LOGGER

DEFAULT_YTDL_OPTS = {
    "outtmpl": "downloads/%(id)s.%(ext)s",
    "format": "bestaudio[ext=m4a]",
    "geo_bypass": True,
    "nocheckcertificate": True,
    "quiet": True,
    "no_warnings": True,
}

ytdl = yt_dlp.YoutubeDL(DEFAULT_YTDL_OPTS)


def download(url: str, progress_hook: callable) -> str:
    try:
        info = ytdl.extract_info(url, download=False)

        downloader = yt_dlp.YoutubeDL(DEFAULT_YTDL_OPTS)
        downloader.add_progress_hook(progress_hook)

        downloader.download([url])

        downloaded_file_path = path.join("downloads", f"{info['id']}.m4a")

        return downloaded_file_path
    except Exception as e:
        LOGGER(__name__).exception(e)
        return ""