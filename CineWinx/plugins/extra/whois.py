from datetime import datetime

from pyrogram import filters, Client
from pyrogram.errors import PeerIdInvalid
from pyrogram.types import Message, User

from CineWinx import app
from config import BANNED_USERS


def reply_check(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.message_id

    elif not message.from_user.is_self:
        reply_id = message.message_id

    return reply_id


info_text = (
    "<a href='tg://user?id={user_id}'>{full_name}</a>\n\n"
    "🆔 𝗨𝘀𝗲𝗿 𝗜𝗗: {user_id}\n"
    "📛 𝗣𝗿𝗶𝗺𝗲𝗶𝗿𝗼 𝗻𝗼𝗺𝗲: {first_name}\n"
    "📝 𝗨́𝗹𝘁𝗶𝗺𝗼 𝗻𝗼𝗺𝗲: {last_name}\n"
    "👤 𝗨𝘀𝘂𝗮́𝗿𝗶𝗼: @{username}\n"
    "🕒 𝗨́𝗹𝘁𝗶𝗺𝗮 𝘃𝗲𝘇 𝗼𝗻𝗹𝗶𝗻𝗲: {last_online}"
)


def last_online(user: User):
    if user.is_bot:
        return ""
    elif user.status == "recently":
        return "🕒 𝗥𝗲𝗰𝗲𝗻𝘁𝗲𝗺𝗲𝗻𝘁𝗲"
    elif user.status == "within_week":
        return "📅 𝗡𝗮 𝘂́𝗹𝘁𝗶𝗺𝗮 𝘀𝗲𝗺𝗮𝗻𝗮"
    elif user.status == "within_month":
        return "📅 𝗡𝗼 𝘂́𝗹𝘁𝗶𝗺𝗼 𝗺𝗲̂𝘀"
    elif user.status == "long_time_ago":
        return "⏳ 𝗛𝗮́ 𝗺𝘂𝗶𝘁𝗼 𝘁𝗲𝗺𝗽𝗼 :("
    elif user.status == "online":
        return "🟢 𝗔𝘁𝘂𝗮𝗹𝗺𝗲𝗻𝘁𝗲 𝗼𝗻𝗹𝗶𝗻𝗲"
    elif user.status == "offline":
        return datetime.fromtimestamp(user.status.date).strftime(
            "📅 %a, %d %b %Y, %H:%M:%S"
        )


def full_name(user: User):
    return user.first_name + " " + user.last_name if user.last_name else user.first_name


@app.on_message(filters.command("whois") & filters.group & ~BANNED_USERS)
async def whois(client: Client, message: Message):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await client.get_users(get_user)
    except PeerIdInvalid:
        await message.reply("🤷‍♂️ 𝗡𝗮̃𝗼 𝗰𝗼𝗻𝗵𝗲𝗰𝗼 𝗲𝘀𝘀𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼.")
        return
    desc = await client.get_chat(get_user)
    desc = desc.description
    await message.reply_text(
        info_text.format(
            full_name=full_name(user),
            user_id=user.id,
            user_dc=user.dc_id,
            first_name=user.first_name,
            last_name=user.last_name if user.last_name else "",
            username=user.username if user.username else "",
            last_online=last_online(user),
            bio=desc if desc else "𝗩𝗮𝘇𝗶𝗼.",
        ),
        disable_web_page_preview=True,
    )


__MODULE__ = "🕵️‍♂️ 𝗪𝗵𝗼𝗶𝘀"
__HELP__ = """
**📋 𝗖𝗼𝗺𝗮𝗻𝗱𝗼:**

• /whois - 𝗩𝗲𝗿 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗼 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼.

<b>ℹ️ 𝗜𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀:</b>

- 𝗘𝘀𝘁𝗲 𝗯𝗼𝘁 𝗳𝗼𝗿𝗻𝗲𝗰𝗲 𝘂𝗺 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 𝗽𝗮𝗿𝗮 𝘃𝗲𝗿 𝗮𝘀 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗼 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼.
- 𝗨𝘀𝗲 𝗼 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 /whois 𝘀𝗲𝗴𝘂𝗶𝗱𝗼 𝗽𝗼𝗿 𝘂𝗺𝗮 𝗿𝗲𝗽𝗹𝘆 𝗮 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗼𝘂 𝘂𝗺 𝗨𝘀𝗲𝗿 𝗜𝗗 𝗽𝗮𝗿𝗮 𝗼𝗯𝘁𝗲𝗿 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝘀𝗼𝗯𝗿𝗲 𝗼 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼.

<b>📌 𝗡𝗼𝘁𝗮:</b>

- 𝗢 𝗰𝗼𝗺𝗮𝗻𝗱𝗼 /whois 𝗽𝗼𝗱𝗲 𝘀𝗲𝗿 𝘂𝘀𝗮𝗱𝗼 𝗽𝗮𝗿𝗮 𝗿𝗲𝗰𝘂𝗽𝗲𝗿𝗮𝗿 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝘀𝗼𝗯𝗿𝗲 𝘂𝗺 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗻𝗼 𝗰𝗵𝗮𝘁.
- 𝗔𝘀 𝗶𝗻𝗳𝗼𝗿𝗺𝗮𝗰̧𝗼̃𝗲𝘀 𝗶𝗻𝗰𝗹𝘂𝗲𝗺 𝗨𝘀𝗲𝗿 𝗜𝗗, 𝗽𝗿𝗶𝗺𝗲𝗶𝗿𝗼 𝗻𝗼𝗺𝗲, 𝘂́𝗹𝘁𝗶𝗺𝗼 𝗻𝗼𝗺𝗲, 𝗻𝗼𝗺𝗲 𝗱𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗲 𝘀𝘁𝗮𝘁𝘂𝘀 𝗱𝗲 𝘂́𝗹𝘁𝗶𝗺𝗮 𝘃𝗲𝘇 𝗼𝗻𝗹𝗶𝗻𝗲.
"""

