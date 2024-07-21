import os
from inspect import getfullargspec

from pyrogram import filters
from pyrogram.types import Message

from CineWinx import app
from CineWinx.misc import SUDOERS
from CineWinx.utils.database import get_client


@app.on_message(filters.command("setpfp", prefixes=".") & SUDOERS)
async def set_pfp(_client: app, message: Message):
    from CineWinx.core.userbot import assistants

    if not message.reply_to_message or not message.reply_to_message.photo:
        return await eor(message, text="📸 𝗥𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗮 𝘂𝗺𝗮 𝗳𝗼𝘁𝗼.")
    for num in assistants:
        client = await get_client(num)
        photo = await message.reply_to_message.download()
        try:
            await client.set_profile_photo(photo=photo)
            await eor(message, text="✅ 𝗙𝗼𝘁𝗼 𝗱𝗲 𝗽𝗿𝗼𝗳𝗶𝗹 𝗮𝘁𝘂𝗮𝗹𝗶𝘇𝗮𝗱𝗮 𝗰𝗼𝗺 𝘀𝘂𝗰𝗲𝘀𝘀𝗼.")
            os.remove(photo)
        except Exception as e:
            await eor(message, text=e)
            os.remove(photo)


@app.on_message(filters.command("setbio", prefixes=".") & SUDOERS)
async def set_bio(client: app, message: Message):
    from CineWinx.core.userbot import assistants

    if len(message.command) == 1:
        return await eor(
            message, text="❗ 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗳𝗼𝗿𝗻𝗲𝗰̧𝗮 𝘂𝗺 𝘁𝗲𝘅𝘁𝗼 𝗽𝗮𝗿𝗮 𝗱𝗲𝗳𝗶𝗻𝗶𝗿 𝗰𝗼𝗺𝗼 𝗯𝗶𝗼."
        )
    elif len(message.command) > 1:
        for num in assistants:
            client = await get_client(num)
            bio = message.text.split(None, 1)[1]
        try:
            await client.update_profile(bio=bio)
            await eor(message, text="✅ 𝗕𝗶𝗼 𝗮𝘁𝘂𝗮𝗹𝗶𝘇𝗮𝗱𝗮.")
        except Exception as e:
            await eor(message, text=e)
    else:
        return await eor(
            message, text="❗ 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗳𝗼𝗿𝗻𝗲𝗰̧𝗮 𝘂𝗺 𝘁𝗲𝘅𝘁𝗼 𝗽𝗮𝗿𝗮 𝘀𝗲𝗿 𝗱𝗲𝗳𝗶𝗻𝗶𝗱𝗼 𝗰𝗼𝗺𝗼 𝗯𝗶𝗼."
        )


@app.on_message(filters.command("setname", prefixes=".") & SUDOERS)
async def set_name(client: app, message: Message):
    from CineWinx.core.userbot import assistants

    if len(message.command) == 1:
        return await eor(
            message, text="❗ 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗳𝗼𝗿𝗻𝗲𝗰̧𝗮 𝘂𝗺 𝘁𝗲𝘅𝘁𝗼 𝗽𝗮𝗿𝗮 𝗱𝗲𝗳𝗶𝗻𝗶𝗿 𝗰𝗼𝗺𝗼 𝗻𝗼𝗺𝗲."
        )
    elif len(message.command) > 1:
        for num in assistants:
            client = await get_client(num)
            name = message.text.split(None, 1)[1]
        try:
            await client.update_profile(first_name=name)
            await eor(message, text=f"✅ 𝗡𝗼𝗺𝗲 𝗮𝘁𝘂𝗮𝗹𝗶𝘇𝗮𝗱𝗼 𝗽𝗮𝗿𝗮 {name}.")
        except Exception as e:
            await eor(message, text=e)
    else:
        return await eor(
            message, text="❗ 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗳𝗼𝗿𝗻𝗲𝗰̧𝗮 𝘂𝗺 𝘁𝗲𝘅𝘁𝗼 𝗽𝗮𝗿𝗮 𝗱𝗲𝗳𝗶𝗻𝗶𝗿 𝗰𝗼𝗺𝗼 𝗻𝗼𝗺𝗲."
        )


@app.on_message(filters.command("delpfp", prefixes=".") & SUDOERS)
async def del_pfp(_client: app, message: Message):
    from CineWinx.core.userbot import assistants

    for num in assistants:
        client = await get_client(num)
        photos = [p async for p in client.get_chat_photos("me")]
        try:
            if photos:
                await client.delete_profile_photos(photos[0].file_id)
                await eor(message, text="✅ 𝗙𝗼𝘁𝗼 𝗲𝘅𝗰𝗹𝘂𝗶́𝗱𝗮 𝗰𝗼𝗺 𝘀𝘂𝗰𝗲𝘀𝘀𝗼.")
            else:
                await eor(message, text="❌ 𝗡𝗲𝗻𝗵𝘂𝗺𝗮 𝗳𝗼𝘁𝗼 𝗱𝗲 𝗽𝗲𝗿𝗳𝗶𝗹.")
        except Exception as e:
            await eor(message, text=e)


@app.on_message(filters.command("delallpfp", prefixes=".") & SUDOERS)
async def delall_pfp(_client: app, message: Message):
    from CineWinx.core.userbot import assistants

    for num in assistants:
        client = await get_client(num)
        photos = [p async for p in client.get_chat_photos("me")]
        try:
            if photos:
                await client.delete_profile_photos([p.file_id for p in photos[1:]])
                await eor(message, text="✅ 𝗧𝗼𝗱𝗮𝘀 𝗮𝘀 𝗳𝗼𝘁𝗼𝘀 𝗱𝗲 𝗽𝗲𝗿𝗳𝗶𝗹 𝗲𝘅𝗰𝗹𝘂𝗶́𝗱𝗼.")
            else:
                await eor(message, text="❌ 𝗡𝗲𝗻𝗵𝘂𝗺𝗮 𝗳𝗼𝘁𝗼 𝗱𝗲 𝗽𝗲𝗿𝗳𝗶𝗹.")
        except Exception as e:
            await eor(message, text=e)


async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})


__MODULE__ = "Assistente"
__HELP__ = """
<u>👩‍💼 𝗖𝗼𝗺𝗮𝗻𝗱𝗼𝘀 𝗱𝗼 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲:</u>

📸 <code>.setpfp</code> - 𝗥𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗰𝗼𝗺 𝘂𝗺𝗮 𝗳𝗼𝘁𝗼 𝗽𝗮𝗿𝗮 𝗱𝗲𝗳𝗶𝗻𝗶𝗿 𝗮 𝗶𝗺𝗮𝗴𝗲𝗺 𝗱𝗲 𝗽𝗲𝗿𝗳𝗶𝗹 𝗱𝗲 𝘁𝗼𝗱𝗼𝘀 𝗼𝘀 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲𝘀 𝗱𝗼 𝗯𝗼𝘁 [𝗮𝗽𝗲𝗻𝗮𝘀 𝗳𝗼𝘁𝗼] [𝗮𝗽𝗲𝗻𝗮𝘀 𝗽𝗮𝗿𝗮 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝘀𝘂𝗱𝗼]
📝 <code>.setname</code> [𝘁𝗲𝘅𝘁𝗼] - 𝗣𝗮𝗿𝗮 𝗱𝗲𝗳𝗶𝗻𝗶𝗿 𝗼 𝗻𝗼𝗺𝗲 𝗱𝗲 𝘁𝗼𝗱𝗼𝘀 𝗼𝘀 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲𝘀 [𝗮𝗽𝗲𝗻𝗮𝘀 𝗽𝗮𝗿𝗮 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝘀𝘂𝗱𝗼]
📝 <code>.setbio</code> [𝘁𝗲𝘅𝘁𝗼] - 𝗣𝗮𝗿𝗮 𝗱𝗲𝗳𝗶𝗻𝗶𝗿 𝗮 𝗯𝗶𝗼 𝗱𝗲 𝘁𝗼𝗱𝗼𝘀 𝗼𝘀 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲𝘀 [𝗮𝗽𝗲𝗻𝗮𝘀 𝗽𝗮𝗿𝗮 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝘀𝘂𝗱𝗼]
❌ <code>.delpfp</code> - 𝗘𝘅𝗰𝗹𝘂𝗶 𝗮 𝗳𝗼𝘁𝗼 𝗱𝗲 𝗽𝗲𝗿𝗳𝗶𝗹 𝗱𝗼𝘀 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲𝘀 [𝗮𝗽𝗲𝗻𝗮𝘀 𝘂𝗺𝗮 𝗳𝗼𝘁𝗼 𝗱𝗲 𝗽𝗲𝗿𝗳𝗶𝗹 𝘀𝗲𝗿𝗮́ 𝗲𝘅𝗰𝗹𝘂𝗶́𝗱𝗮] [𝗮𝗽𝗲𝗻𝗮𝘀 𝗽𝗮𝗿𝗮 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝘀𝘂𝗱𝗼]
❌ <code>.delallpfp</code> - 𝗘𝘅𝗰𝗹𝘂𝗶 𝘁𝗼𝗱𝗮𝘀 𝗮𝘀 𝗳𝗼𝘁𝗼𝘀 𝗱𝗲 𝗽𝗲𝗿𝗳𝗶𝗹 𝗱𝗼𝘀 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲𝘀 [𝗮𝗽𝗲𝗻𝗮𝘀 𝘂𝗺𝗮 𝗳𝗼𝘁𝗼 𝗱𝗲 𝗽𝗲𝗿𝗳𝗶𝗹 𝗽𝗲𝗿𝗺𝗮𝗻𝗲𝗰𝗲𝗿𝗮́] [𝗮𝗽𝗲𝗻𝗮𝘀 𝗽𝗮𝗿𝗮 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝘀𝘂𝗱𝗼]

<u>👥 𝗖𝗼𝗺𝗮𝗻𝗱𝗼𝘀 𝗱𝗼 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗱𝗲 𝗴𝗿𝘂𝗽𝗼:</u>

📋 <code>/checkassistant</code> - 𝗩𝗲𝗿𝗶𝗳𝗶𝗾𝘂𝗲 𝗼𝘀 𝗱𝗲𝘁𝗮𝗹𝗵𝗲𝘀 𝗱𝗼 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗱𝗼 𝘀𝗲𝘂 𝗴𝗿𝘂𝗽𝗼
🔄 <code>/setassistant</code> - 𝗔𝗹𝘁𝗲𝗿𝗲 𝗼 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗽𝗮𝗿𝗮 𝘂𝗺 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗲𝘀𝗽𝗲𝗰𝗶́𝗳𝗶𝗰𝗼 𝗽𝗮𝗿𝗮 𝗼 𝘀𝗲𝘂 𝗴𝗿𝘂𝗽𝗼
🔀 <code>/changeassistant</code> - 𝗔𝗹𝘁𝗲𝗿𝗲 𝗼 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗱𝗼 𝘀𝗲𝘂 𝗴𝗿𝘂𝗽𝗼 𝗽𝗮𝗿𝗮 𝘂𝗺 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗮𝗹𝗲𝗮𝘁𝗼́𝗿𝗶𝗼 𝗱𝗶𝘀𝗽𝗼𝗻𝗶́𝘃𝗲𝗹 𝗻𝗼𝘀 𝘀𝗲𝗿𝘃𝗶𝗱𝗼𝗿𝗲𝘀 𝗱𝗼 𝗯𝗼𝘁.
"""
