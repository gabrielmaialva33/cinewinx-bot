from CineWinx import app
from config import LOG_GROUP_ID

protected_messages = {}


async def protect_message(chat_id, message_id):
    if chat_id not in protected_messages:
        protected_messages[chat_id] = []
    protected_messages[chat_id].append(message_id)


async def send_message(chat_id, text, reply=None):
    if reply:
        try:
            message = await app.send_message(
                chat_id, text, reply_to_message_id=reply, disable_web_page_preview=True
            )
            await protect_message(chat_id, message.id)
        except Exception as e:
            return await app.send_message(LOG_GROUP_ID, e)
    else:
        try:
            message = await app.send_message(
                chat_id, text, disable_web_page_preview=True
            )
            await protect_message(chat_id, message.id)
        except Exception as e:
            return await app.send_message(LOG_GROUP_ID, e)
