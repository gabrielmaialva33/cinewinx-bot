import asyncio
import logging
import json
from typing import Union, Dict, Any, Optional, TypedDict, List

import aiohttp

from gradio_client import Client as GradioClient

from pyrogram import filters, Client
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from CineWinx import app
from CineWinx.utils.winx_font import Fonts
from config import PREFIXES, BANNED_USERS, HF_TOKEN
from strings import get_command

# curl -X POST https://guardiancc-flux-gif-animations-2.hf.space/call/infer -s -H "Content-Type: application/json" -d '{
#   "data": [
# 							"Hello!!",
# 							0,
# 							true,
# 							1
# ]}' \
#   | awk -F'"' '{ print $4}'  \
#   | read EVENT_ID; curl -N https://guardiancc-flux-gif-animations-2.hf.space/call/infer/$EVENT_ID

@app.on_message(filters.command(["gif"], PREFIXES) & ~BANNED_USERS)
async def hf_gif(_client: Client, message: Message):
    try:
        text = message.text.split(" ", 1)[1]
    except IndexError:
        await message.reply_text(
            "📝 𝗩𝗼𝗰𝗲 𝗽𝗼𝗱𝗲 𝗲𝗻𝘃𝗶𝗮𝗿 𝗼 𝘁𝗲𝘅𝘁𝗼 𝗽𝗮𝗿𝗮 𝗰𝗼𝗻𝘃𝗲𝗿𝘁𝗲 𝗲𝗺 𝗚𝗜𝗙.")
        return

    async with aiohttp.ClientSession() as session:
        mystic = await message.reply_text("🎞️ 𝗚𝗲𝗿𝗮𝗻𝗱𝗼 𝗚𝗜𝗙, 𝗽𝗼𝗿 𝗳𝗮𝘃𝗼𝗿 𝗮𝗴𝘂𝗮𝗿𝗱𝗲...")
        async with session.post(
            "https://guardiancc-flux-gif-animations-2.hf.space/call/infer",
            json={
                "data": [
                    text,
                    645956939,
                    True,
                    28
                ]
            },
            headers={"Content-Type": "application/json"},
        ) as infer_resp:
            data = await infer_resp.json()
            event_id = data["event_id"]
            logging.info(f"event ID: {event_id}")

            async with session.get(
                    f"https://guardiancc-flux-gif-animations-2.hf.space/call/infer/{event_id}"
            ) as event_resp:
                if event_resp.content_type == "text/event-stream":
                    async for line in event_resp.content:
                        event_data = line.decode('utf-8').strip()
                        if event_data.startswith("data:"):
                            json_str = event_data.replace("data:", "").strip()
                            try:
                                json_data = json.loads(json_str)
                                print("json_data", json_data)
                                #  [{'path': '/tmp/gradio/9a0eb62f04b8ba012618cb568bf8be2007181d793b8297bda622dd44df3b0c8f/9b4b56650fe4451d80ec2e95446636f6-flux.gif', 'url': 'https://guardiancc-flux-gif-animations-2.hf.space/file=/tmp/gradio/9a0eb62f04b8ba012618cb568bf8be2007181d793b8297bda622dd44df3b0c8f/9b4b56650fe4451d80ec2e95446636f6-flux.gif', 'size': None, 'orig_name': '9b4b56650fe4451d80ec2e95446636f6-flux.gif', 'mime_type': None, 'is_stream': False, 'meta': {'_type': 'gradio.FileData'}}, {'path': '/tmp/gradio/9f49a411b6fbe57827c57b7bf6501cbf3a9bc56dd36f548eb2c20755eebb37a2/image.webp', 'url': 'https://guardiancc-flux-gif-animations-2.hf.space/file=/tmp/gradio/9f49a411b6fbe57827c57b7bf6501cbf3a9bc56dd36f548eb2c20755eebb37a2/image.webp', 'size': None, 'orig_name': 'image.webp', 'mime_type': None, 'is_stream': False, 'meta': {'_type': 'gradio.FileData'}}, 907086999]
                                if json_data not in [None, ""]:
                                    await mystic.delete()
                                    await message.reply_animation(json_data[0]["url"], caption=f"🎞️ 𝗚𝗜𝗙 𝗴𝗲𝗿𝗮𝗱𝗼 𝗰𝗼𝗺 𝗼 𝘁𝗲𝘅𝘁𝗼: <code>{text}</code>")
                            except json.JSONDecodeError:
                                logging.error(f"error decoding json: {json_str}")
                                await mystic.edit_text("🚫 𝗘𝗿𝗿𝗼𝗿 𝗮𝗼 𝗴𝗲𝗿𝗮𝗿 𝗼 𝗚𝗜𝗙.")
                                await session.close()
                        else:
                            logging.info(f"event data: {event_data}")
                else:
                    logging.error(f"unexpected content-type: {event_resp.content_type}")
                    await mystic.edit_text("🚫 𝗘𝗿𝗿𝗼𝗿 𝗮𝗼 𝗴𝗲𝗿𝗮𝗿 𝗼 𝗚𝗜𝗙.")
                    await session.close()

