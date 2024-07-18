from pyrogram.types import Message

from CineWinx import app
from CineWinx.utils.database import is_on_off
from config import LOG_GROUP_ID, LOG


async def play_logs(message: Message, stream_type: str):
    if await is_on_off(LOG):
        if message.chat.username:
            chatusername = f"@{message.chat.username}"
        else:
            chatusername = "Grupo privado"

        logger_text = f"""
        <b>{app.mention} play log</b>

<b>id do chat:</b> `{message.chat.id}`
<b>nome do chat:</b> {message.chat.title}
<b>username do chat:</b> {chatusername}

<b>id do usuário:</b> `{message.from_user.id}`
<b>nome:</b> {message.from_user.mention}
<b>username:</b> @{message.from_user.username}

<b>consulta:</b> {message.text.split(None, 1)[1]}
<b>tipo de stream:</b> {stream_type}"""
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
