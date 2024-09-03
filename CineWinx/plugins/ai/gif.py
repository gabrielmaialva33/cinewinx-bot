import logging
import json

import aiohttp

from pyrogram import filters, Client
from pyrogram.types import Message

from CineWinx import app
from config import PREFIXES, BANNED_USERS

SPACE_URL = "https://guardiancc-flux-gif-animations-2.hf.space/call/infer"


@app.on_message(filters.command(["gif"], PREFIXES) & ~BANNED_USERS)
async def hf_gif(_client: Client, message: Message):
    try:
        text = message.text.split(" ", 1)[1]
    except IndexError:
        await message.reply_text("📝 𝗩𝗼𝗰𝗲 𝗽𝗼𝗱𝗲 𝗲𝗻𝘃𝗶𝗮𝗿 𝗼 𝘁𝗲𝘅𝘁𝗼 𝗽𝗮𝗿𝗮 𝗰𝗼𝗻𝘃𝗲𝗿𝘁𝗲 𝗲𝗺 𝗚𝗜𝗙.")
        return

    async with aiohttp.ClientSession() as session:
        mystic = await message.reply_text("🎞️ 𝗚𝗲𝗿𝗮𝗻𝗱𝗼 𝗚𝗜𝗙, 𝗽𝗼𝗿 𝗳𝗮𝘃𝗼𝗿 𝗮𝗴𝘂𝗮𝗿𝗱𝗲...")
        async with session.post(
            SPACE_URL,
            json={
                "data": [
                    text,
                    645956939,
                    True,
                    30,
                ]
            },
            headers={"Content-Type": "application/json"},
        ) as infer_resp:
            data = await infer_resp.json()
            event_id = data["event_id"]
            logging.info(f"event ID: {event_id}")

            async with session.get(f"{SPACE_URL}/{event_id}") as event_resp:
                if event_resp.content_type == "text/event-stream":
                    async for line in event_resp.content:
                        event_data = line.decode("utf-8").strip()
                        if event_data.startswith("data:"):
                            json_str = event_data.replace("data:", "").strip()
                            try:
                                json_data = json.loads(json_str)
                                if json_data not in [None, ""]:
                                    await mystic.delete()
                                    await message.reply_animation(
                                        json_data[0]["url"],
                                        caption=f"🎞️ 𝗚𝗜𝗙 𝗴𝗲𝗿𝗮𝗱𝗼 𝗰𝗼𝗺 𝗼 𝘁𝗲𝘅𝘁𝗼: <code>{text}</code>",
                                    )
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
