from CineWinx import app
from CineWinx.utils.database import is_on_off
from config import LOG_GROUP_ID, LOG


async def play_logs(message, streamtype):
    if await is_on_off(LOG):
        if message.chat.username:
            chatusername = f"@{message.chat.username}"
        else:
            chatusername = "ᴘʀɪᴠᴀᴛᴇ ɢʀᴏᴜᴘ"

        logger_text = f"""
**{app.mention} ᴘʟᴀʏ ʟᴏɢ**

**ᴄʜᴀᴛ ɪᴅ :** `{message.chat.id}`
**ᴄʜᴀᴛ ɴᴀᴍᴇ :** {message.chat.title}
**ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ :** {chatusername}

**ᴜsᴇʀ ɪᴅ :** `{message.from_user.id}`
**ɴᴀᴍᴇ :** {message.from_user.mention}
**ᴜsᴇʀɴᴀᴍᴇ :** @{message.from_user.username}

**ǫᴜᴇʀʏ :** {message.text.split(None, 1)[1]}
**sᴛʀᴇᴀᴍᴛʏᴘᴇ :** {streamtype}"""
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
