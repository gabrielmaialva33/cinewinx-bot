from pyrogram import filters, Client
from pyrogram.types import Message

from CineWinx import app
from config import BANNED_USERS


@app.on_message(filters.command("id") & ~BANNED_USERS)
async def get_id(_client: Client, message: Message):
    try:
        if not message.reply_to_message and message.chat:
            await message.reply(
                f"🆔 𝗨𝘀𝘂𝗮́𝗿𝗶𝗼 <b>{message.from_user.first_name}</b>'𝘀 𝗜𝗗 𝗲́ <code>{message.from_user.id}</code>.\n𝗘𝘀𝘁𝗲 𝗰𝗵𝗮𝘁'𝘀 𝗜𝗗 𝗲́: <code>{message.chat.id}</code>."
            )
        elif not message.reply_to_message.sticker or message.reply_to_message is None:
            if message.reply_to_message.forward_from_chat:
                await message.reply(
                    f"🆔 𝗢 {str(message.reply_to_message.forward_from_chat.type)[9:].lower()}, {message.reply_to_message.forward_from_chat.title} 𝘁𝗲𝗺 𝘂𝗺 𝗜𝗗 𝗱𝗲 <code>{message.reply_to_message.forward_from_chat.id}</code>"
                )
            elif message.reply_to_message.forward_from:
                await message.reply(
                    f"🆔 𝗢 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗲𝗻𝘃𝗶𝗮𝗱𝗼, {message.reply_to_message.forward_from.first_name} 𝘁𝗲𝗺 𝘂𝗺 𝗜𝗗 𝗱𝗲 <code>{message.reply_to_message.forward_from.id}</code>."
                )
            elif message.reply_to_message.forward_sender_name:
                await message.reply(
                    "🆔 𝗗𝗲𝘀𝗰𝘂𝗹𝗽𝗲, 𝗻𝘂𝗻𝗰𝗮 𝘃𝗶 𝗲𝘀𝘁𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝘂𝗺 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗼𝘂 𝗻𝗮̃𝗼 𝗽𝗼𝘀𝘀𝗼 𝗼𝗯𝘁𝗲𝗿 𝗼 𝗜𝗗."
                )
            else:
                await message.reply(
                    f"🆔 𝗢 𝗜𝗗 𝗱𝗼 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 {message.reply_to_message.from_user.first_name} 𝗲́ <code>{message.reply_to_message.from_user.id}</code>."
                )
        elif message.reply_to_message.sticker:
            if message.reply_to_message.forward_from_chat:
                await message.reply(
                    f"🆔 𝗢 {str(message.reply_to_message.forward_from_chat.type)[9:].lower()}, {message.reply_to_message.forward_from_chat.title} 𝘁𝗲𝗺 𝘂𝗺 𝗜𝗗 𝗱𝗲 <code>{message.reply_to_message.forward_from_chat.id}</code> \n𝗘 𝗼 𝗜𝗗 𝗱𝗼 𝘀𝘁𝗶𝗰𝗸𝗲𝗿 𝗲𝗻𝘃𝗶𝗮𝗱𝗼 𝗲́ <code>{message.reply_to_message.sticker.file_id}</code>"
                )
            elif message.reply_to_message.forward_from:
                await message.reply(
                    f"🆔 𝗢 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗲𝗻𝘃𝗶𝗮𝗱𝗼, {message.reply_to_message.forward_from.first_name} 𝘁𝗲𝗺 𝘂𝗺 𝗜𝗗 𝗱𝗲 <code>{message.reply_to_message.forward_from.id}</code> \n𝗘 𝗼 𝗜𝗗 𝗱𝗼 𝘀𝘁𝗶𝗰𝗸𝗲𝗿 𝗲𝗻𝘃𝗶𝗮𝗱𝗼 𝗲́ <code>{message.reply_to_message.sticker.file_id}</code>."
                )
            elif message.reply_to_message.forward_sender_name:
                await message.reply(
                    "🆔 𝗗𝗲𝘀𝗰𝘂𝗹𝗽𝗲, 𝗻𝘂𝗻𝗰𝗮 𝘃𝗶 𝗲𝘀𝘁𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗲 𝘂𝗺 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗼𝘂 𝗻𝗮̃𝗼 𝗽𝗼𝘀𝘀𝗼 𝗼𝗯𝘁𝗲𝗿 𝗼 𝗜𝗗."
                )
            else:
                await message.reply(
                    f"🆔 𝗢 𝗜𝗗 𝗱𝗼 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 {message.reply_to_message.from_user.first_name} 𝗲́ <code>{message.reply_to_message.from_user.id}</code>\n𝗘 𝗼 𝗜𝗗 𝗱𝗼 𝘀𝘁𝗶𝗰𝗸𝗲𝗿 𝗲𝗻𝘃𝗶𝗮𝗱𝗼 𝗲́ <code>{message.reply_to_message.sticker.file_id}</code>."
                )
        else:
            await message.reply(
                f"🆔 𝗢 𝗜𝗗 𝗱𝗼 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 {message.reply_to_message.from_user.first_name} 𝗲́ <code>{message.reply_to_message.from_user.id}</code>."
            )
    except Exception as r:
        await message.reply(f"❗ 𝗢𝗰𝗼𝗿𝗿𝗲𝘂 𝘂𝗺 𝗲𝗿𝗿𝗼 𝗮𝗼 𝗼𝗯𝘁𝗲𝗿 𝗼 𝗜𝗗. {r}")


__MODULE__ = "🆔 𝗜𝗗 𝗱𝗼 𝗨𝘀𝘂𝗮́𝗿𝗶𝗼"
__HELP__ = """
**🔍 𝗥𝗲𝘁𝗼𝗿𝗻𝗮 𝗜𝗗:**

• `/id`: 𝗥𝗲𝘁𝗼𝗿𝗻𝗮 𝗼 𝗜𝗗 𝗱𝗼 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗲 𝗱𝗼 𝗰𝗵𝗮𝘁.
"""
