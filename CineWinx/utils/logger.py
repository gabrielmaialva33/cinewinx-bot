from pyrogram.types import Message

from CineWinx import app
from CineWinx.utils.database import is_on_off
from config import LOG_GROUP_ID, LOG


async def play_logs(message: Message, stream_type: str):
    if await is_on_off(LOG):
        if message.chat.username:
            chat_username = f"@{message.chat.username}"
        else:
            chat_username = "𝗚𝗿𝘂𝗽𝗼 𝗽𝗿𝗶𝘃𝗮𝗱𝗼 🔒"

        logger_text = f"""
        🎵 <b>{app.mention} 𝗣𝗹𝗮𝘆 𝗟𝗼𝗴</b>

🆔 <b>𝗜𝗗 𝗱𝗼 𝗖𝗵𝗮𝘁:</b> <code>{message.chat.id}</code>
🏠 <b>𝗡𝗼𝗺𝗲 𝗱𝗼 𝗖𝗵𝗮𝘁:</b> {message.chat.title}
📧 <b>𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲 𝗱𝗼 𝗖𝗵𝗮𝘁:</b> {chat_username}

🆔 <b>𝗜𝗗 𝗱𝗼 𝗨𝘀𝘂𝗮́𝗿𝗶𝗼:</b> <code>{message.from_user.id}</code>
👤 <b>𝗡𝗼𝗺𝗲:</b> {message.from_user.mention}
📧 <b>𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲:</b> @{message.from_user.username}

📝 <b>𝗖𝗼𝗻𝘀𝘂𝗹𝘁𝗮:</b> {message.text.split(None, 1)[1]}
📡 <b>𝗧𝗶𝗽𝗼 𝗱𝗲 𝗦𝘁𝗿𝗲𝗮𝗺:</b> {stream_type}"""
        if message.chat.id != LOG_GROUP_ID:
            try:
                await app.send_message(
                    chat_id=LOG_GROUP_ID,
                    text=logger_text,
                    disable_web_page_preview=True,
                )
            except Exception as e:
                print(e)
        return
