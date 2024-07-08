from youtubesearchpython.__future__ import VideosSearch

import logging
import os
import re

import aiofiles
import aiohttp

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from unidecode import unidecode

from config import YOUTUBE_IMG_URL


async def gen_thumb(video_id: str) -> str:
    try:
        url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        return url
    except Exception as e:
        logging.error(e)
        return YOUTUBE_IMG_URL


async def gen_qthumb(video_id: str) -> str:
    try:
        url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
        return url
    except Exception as e:
        logging.error(e)
        return YOUTUBE_IMG_URL


async def get_thumb(video_id: str):
    if os.path.isfile(f"cache/{video_id}.png"):
        return f"cache/{video_id}.png"

    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except Exception as e:
                logging.error(e)
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except Exception as e:
                logging.error(e)
                duration = "Unknown Mins"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                views = result["viewCount"]["short"]
            except Exception as e:
                logging.error(e)
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except Exception as e:
                logging.error(e)
                channel = "Unknown Channel"

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"cache/thumb{video_id}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        youtube = Image.open(f"cache/thumb{video_id}.png")
        image1 = change_image_size(1280, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(10))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.5)
        draw = ImageDraw.Draw(background)
        arial = ImageFont.truetype("WinxMusic/assets/font2.ttf", 30)
        font = ImageFont.truetype("WinxMusic/assets/font.ttf", 40)
        logo = ImageFont.truetype("WinxMusic/assets/font.ttf", 70)
        draw.text(
            (10, 5),
            unidecode(f"@cinewinx"),
            fill="white",
            font=logo,
            align="center",
        )
        draw.text(
            (55, 560),
            f"{channel} | {views[:23]}",
            (255, 255, 255),
            font=arial,
        )
        draw.text(
            (57, 600),
            clear(title),
            (255, 255, 255),
            font=font,
        )
        draw.line(
            [(55, 660), (1220, 660)],
            fill="white",
            width=5,
            joint="curve",
        )
        draw.ellipse(
            [(918, 648), (942, 672)],
            outline="white",
            fill="white",
            width=15,
        )
        draw.text(
            (36, 685),
            "00:00",
            (255, 255, 255),
            font=arial,
        )
        draw.text(
            (1185, 685),
            f"{duration[:23]}",
            (255, 255, 255),
            font=arial,
        )
        try:
            os.remove(f"cache/thumb{video_id}.png")
        except Exception as e:
            logging.error(e)
            pass
        background.save(f"cache/{video_id}.png")
        return f"cache/{video_id}.png"
    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL


def clear(text):
    list = text.split(" ")
    title = ""
    for i in list:
        if len(title) + len(i) < 60:
            title += " " + i
    return title.strip()


def change_image_size(max_width: int, max_height: int, image):
    width_ratio = max_width / image.size[0]
    height_ratio = max_height / image.size[1]

    new_width = int(width_ratio * image.size[0])
    new_height = int(height_ratio * image.size[1])

    new_image = image.resize((new_width, new_height))
    return new_image
