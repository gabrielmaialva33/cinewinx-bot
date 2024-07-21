import asyncio
from datetime import datetime, timedelta

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.errors import FloodWait
from pyrogram.raw import types
from pyrogram.types import Message

import config
from CineWinx import app
from CineWinx.misc import SUDOERS
from CineWinx.utils.cleanmode import protected_messages
from CineWinx.utils.database import (
    get_active_chats,
    get_authuser_names,
    get_client,
    get_particular_top,
    get_served_chats,
    get_served_users,
    get_user_top,
    is_cleanmode_on,
    set_queries,
    update_particular_top,
    update_user_top,
)
from CineWinx.utils.decorators.language import language
from CineWinx.utils.formatters import alpha_to_int
from config import adminlist, chatstats, clean, userstats, PREFIXES
from strings import get_command

BROADCAST_COMMAND = get_command("BROADCAST_COMMAND")
AUTO_DELETE = config.CLEANMODE_DELETE_MINS
AUTO_SLEEP = 5
IS_BROADCASTING = False
cleanmode_group = 15


@app.on_raw_update(group=cleanmode_group)
async def clean_mode(_client: app, update, users, chats):
    global IS_BROADCASTING
    if IS_BROADCASTING:
        return
    try:
        if not isinstance(update, types.UpdateReadChannelOutbox):
            return
    except:
        return
    if users:
        return
    if chats:
        return
    message_id = update.max_id
    chat_id = int(f"-100{update.channel_id}")
    if not await is_cleanmode_on(chat_id):
        return
    if chat_id not in clean:
        clean[chat_id] = []
    time_now = datetime.now()
    put = {
        "msg_id": message_id,
        "timer_after": time_now + timedelta(minutes=AUTO_DELETE),
    }
    clean[chat_id].append(put)
    await set_queries(1)


@app.on_message(filters.command(BROADCAST_COMMAND, PREFIXES) & SUDOERS)
@language
async def broadcast_message(_client: app, message: Message, _):
    global IS_BROADCASTING
    if message.reply_to_message:
        x = message.reply_to_message.id
        y = message.chat.id
    else:
        if len(message.command) < 2:
            return await message.reply_text(_["broad_5"])
        query = message.text.split(None, 1)[1]
        if "-pin" in query:
            query = query.replace("-pin", "")
        if "-nobot" in query:
            query = query.replace("-nobot", "")
        if "-pinloud" in query:
            query = query.replace("-pinloud", "")
        if "-assistant" in query:
            query = query.replace("-assistant", "")
        if "-user" in query:
            query = query.replace("-user", "")
        if query == "":
            return await message.reply_text(_["broad_6"])

    IS_BROADCASTING = True

    # Bot broadcast inside chats
    if "-nobot" not in message.text:
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            if i == config.LOG_GROUP_ID:
                continue
            try:
                m = (
                    await app.forward_messages(i, y, x)
                    if message.reply_to_message
                    else await app.send_message(i, text=query)
                )
                if "-pin" in message.text:
                    try:
                        await m.pin(disable_notification=True)
                        pin += 1
                    except Exception:
                        continue
                elif "-pinloud" in message.text:
                    try:
                        await m.pin(disable_notification=False)
                        pin += 1
                    except Exception:
                        continue
                sent += 1
            except FloodWait as e:
                flood_time = int(e.value)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except Exception:
                continue
        try:
            await message.reply_text(_["broad_1"].format(sent, pin))
        except:
            pass

    # Bot broadcasting to users
    if "-user" in message.text:
        susr = 0
        served_users = []
        susers = await get_served_users()
        for user in susers:
            served_users.append(int(user["user_id"]))
        for i in served_users:
            try:
                m = (
                    await app.forward_messages(i, y, x)
                    if message.reply_to_message
                    else await app.send_message(i, text=query)
                )
                susr += 1
            except FloodWait as e:
                flood_time = int(e.value)
                if flood_time > 200:
                    continue
                await asyncio.sleep(flood_time)
            except Exception:
                pass
        try:
            await message.reply_text(_["broad_7"].format(susr))
        except:
            pass

    # Bot broadcasting by assistant
    if "-assistant" in message.text:
        aw = await message.reply_text(_["broad_2"])
        text = _["broad_3"]
        from CineWinx.core.userbot import assistants

        for num in assistants:
            sent = 0
            client = await get_client(num)
            async for dialog in client.get_dialogs():
                if dialog.chat.id == config.LOG_GROUP_ID:
                    continue
                try:
                    (
                        await client.forward_messages(dialog.chat.id, y, x)
                        if message.reply_to_message
                        else await client.send_message(dialog.chat.id, text=query)
                    )
                    sent += 1
                except FloodWait as e:
                    flood_time = int(e.value)
                    if flood_time > 200:
                        continue
                    await asyncio.sleep(flood_time)
                except Exception as e:
                    print(e)
                    continue
            text += _["broad_4"].format(num, sent)
        try:
            await aw.edit_text(text)
        except:
            pass
    IS_BROADCASTING = False


async def auto_clean():
    while not await asyncio.sleep(AUTO_SLEEP):
        try:
            for chat_id in chatstats:
                for dic in chatstats[chat_id]:
                    vidid = dic["vidid"]
                    title = dic["title"]
                    chatstats[chat_id].pop(0)
                    spot = await get_particular_top(chat_id, vidid)
                    if spot:
                        spot = spot["spot"]
                        next_spot = spot + 1
                        new_spot = {"spot": next_spot, "title": title}
                        await update_particular_top(chat_id, vidid, new_spot)
                    else:
                        next_spot = 1
                        new_spot = {"spot": next_spot, "title": title}
                        await update_particular_top(chat_id, vidid, new_spot)
            for user_id in userstats:
                for dic in userstats[user_id]:
                    vidid = dic["vidid"]
                    title = dic["title"]
                    userstats[user_id].pop(0)
                    spot = await get_user_top(user_id, vidid)
                    if spot:
                        spot = spot["spot"]
                        next_spot = spot + 1
                        new_spot = {"spot": next_spot, "title": title}
                        await update_user_top(user_id, vidid, new_spot)
                    else:
                        next_spot = 1
                        new_spot = {"spot": next_spot, "title": title}
                        await update_user_top(user_id, vidid, new_spot)
        except:
            continue
        try:
            for chat_id in clean:
                if chat_id == config.LOG_GROUP_ID:
                    continue
                for x in clean[chat_id]:
                    if datetime.now() > x["timer_after"]:
                        # Skip deletion if the message is protected
                        if (
                                chat_id in protected_messages
                                and x["msg_id"] in protected_messages[chat_id]
                        ):
                            continue
                        try:
                            await app.delete_messages(chat_id, x["msg_id"])
                        except FloodWait as e:
                            await asyncio.sleep(e.value)
                        except:
                            continue
                    else:
                        continue
        except:
            continue
        try:
            served_chats = await get_active_chats()
            for chat_id in served_chats:
                if chat_id not in adminlist:
                    adminlist[chat_id] = []
                    admins = app.get_chat_members(
                        chat_id, filter=ChatMembersFilter.ADMINISTRATORS
                    )
                    async for user in admins:
                        if user.privileges.can_manage_video_chats:
                            adminlist[chat_id].append(user.user.id)
                    authusers = await get_authuser_names(chat_id)
                    for user in authusers:
                        user_id = await alpha_to_int(user)
                        adminlist[chat_id].append(user_id)
        except:
            continue


asyncio.create_task(auto_clean())

__MODULE__ = "G-cast"
__HELP__ = """🍒 <b><u>𝗙𝘂𝗻𝗰𝗶𝗼𝗻𝗮𝗹𝗶𝗱𝗮𝗱𝗲 𝗱𝗲 𝗧𝗿𝗮𝗻𝘀𝗺𝗶𝘀𝘀𝗮̃𝗼</u></b> [𝗮𝗽𝗲𝗻𝗮𝘀 𝗽𝗮𝗿𝗮 𝗮𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿𝗲𝘀]:
📣 <code>/broadcast [𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗼𝘂 𝗿𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗮 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺]</code> 𝗧𝗿𝗮𝗻𝘀𝗺𝗶𝘁𝗲 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗽𝗮𝗿𝗮 𝗼𝘀 𝗰𝗵𝗮𝘁𝘀 𝗮𝘁𝗲𝗻𝗱𝗶𝗱𝗼𝘀 𝗽𝗲𝗹𝗼 𝗯𝗼𝘁.

🔗 <u>𝗠𝗼𝗱𝗼𝘀 𝗱𝗲 𝗧𝗿𝗮𝗻𝘀𝗺𝗶𝘀𝘀𝗮̃𝗼:</u>
📌 <code>-pin</code> 𝗙𝗶𝘅𝗮 𝘀𝘂𝗮𝘀 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗻𝘀 𝘁𝗿𝗮𝗻𝘀𝗺𝗶𝘁𝗶𝗱𝗮𝘀 𝗻𝗼𝘀 𝗰𝗵𝗮𝘁𝘀 𝗮𝘁𝗲𝗻𝗱𝗶𝗱𝗼𝘀.
📢 <code>-pinloud</code> 𝗙𝗶𝘅𝗮 𝘀𝘂𝗮𝘀 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗻𝘀 𝘁𝗿𝗮𝗻𝘀𝗺𝗶𝘁𝗶𝗱𝗮𝘀 𝗻𝗼𝘀 𝗰𝗵𝗮𝘁𝘀 𝗮𝘁𝗲𝗻𝗱𝗶𝗱𝗼𝘀 𝗲 𝗲𝗻𝘃𝗶𝗮 𝗻𝗼𝘁𝗶𝗳𝗶𝗰𝗮𝗰̧𝗮̃𝗼 𝗮𝗼𝘀 𝗺𝗲𝗺𝗯𝗿𝗼𝘀.
👥 <code>-user</code> 𝗧𝗿𝗮𝗻𝘀𝗺𝗶𝘁𝗲 𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗽𝗮𝗿𝗮 𝗼𝘀 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗾𝘂𝗲 𝗶𝗻𝗶𝗰𝗶𝗮𝗿𝗮𝗺 𝘀𝗲𝘂 𝗯𝗼𝘁.
🤖 <code>-assistant</code> 𝗧𝗿𝗮𝗻𝘀𝗺𝗶𝘁𝗲 𝘀𝘂𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗮 𝗽𝗮𝗿𝘁𝗶𝗿 𝗱𝗮 𝗰𝗼𝗻𝘁𝗮 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗱𝗼 𝗯𝗼𝘁.
🚫 <code>-nobot</code> 𝗜𝗺𝗽𝗲𝗱𝗲 𝗼 𝗯𝗼𝘁 𝗱𝗲 𝘁𝗿𝗮𝗻𝘀𝗺𝗶𝘁𝗶𝗿 𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺.

📋<b>𝗘𝘅𝗲𝗺𝗽𝗹𝗼:</b> `/broadcast -user -assistant -pin 𝗧𝗲𝘀𝘁𝗮𝗻𝗱𝗼 𝘁𝗿𝗮𝗻𝘀𝗺𝗶𝘀𝘀𝗮̃𝗼`
"""
