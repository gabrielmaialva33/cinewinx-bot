import asyncio
import logging
from datetime import datetime

from pyrogram.enums import ChatType

import config
from CineWinx import app
from CineWinx.core.call import CineWinx, autoend
from CineWinx.utils.database import get_client, is_active_chat, is_autoend


async def auto_leave():
    if config.AUTO_LEAVING_ASSISTANT == str(True):
        while not await asyncio.sleep(config.AUTO_LEAVE_ASSISTANT_TIME):
            from CineWinx.core.userbot import assistants

            for num in assistants:
                client = await get_client(num)
                left = 0
                try:
                    async for i in client.get_dialogs():
                        chat_type = i.chat.type
                        if chat_type in [
                            ChatType.SUPERGROUP,
                            ChatType.GROUP,
                            ChatType.CHANNEL,
                        ]:
                            chat_id = i.chat.id
                            if chat_id not in [config.LOG_GROUP_ID]:
                                if left == 20:
                                    continue
                                if not await is_active_chat(chat_id):
                                    try:
                                        await client.leave_chat(chat_id)
                                        left += 1
                                    except:
                                        continue
                except:
                    pass


asyncio.create_task(auto_leave())


async def auto_end():
    while not await asyncio.sleep(5):
        if not await is_autoend():
            continue
        for chat_id in autoend:
            timer = autoend.get(chat_id)
            if not timer:
                continue
            if datetime.now() > timer:
                if not await is_active_chat(chat_id):
                    autoend[chat_id] = {}
                    continue
                autoend[chat_id] = {}
                try:
                    await CineWinx.stop_stream(chat_id)
                except Exception as e:
                    logging.warning(e)
                    continue
                try:
                    await app.send_message(
                        chat_id,
                        "𝗕𝗼𝘁 𝘀𝗮𝗶𝘂 𝗱𝗼 𝗰𝗵𝗮𝘁 𝗱𝗲 𝘃𝗼𝘇 𝗽𝗼𝗿 𝗶𝗻𝗮𝘁𝗶𝘃𝗶𝗱𝗮𝗱𝗲 💤 𝗽𝗮𝗿𝗮 𝗲𝘃𝗶𝘁𝗮𝗿 𝘀𝗼𝗯𝗿𝗲𝗰𝗮𝗿𝗴𝗮 𝗻𝗼𝘀 𝘀𝗲𝗿𝘃𝗶𝗱𝗼𝗿𝗲𝘀 ⚠️. "
                        "𝗡𝗶𝗻𝗴𝘂𝗲́𝗺 𝗲𝘀𝘁𝗮𝘃𝗮 𝗼𝘂𝘃𝗶𝗻𝗱𝗼 𝗼 𝗯𝗼𝘁 𝗻𝗼 𝗰𝗵𝗮𝘁 𝗱𝗲 𝘃𝗼𝘇 🎧.",
                    )
                except Exception as e:
                    logging.error(e)
                    continue


asyncio.create_task(auto_end())
