from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from CineWinx import app
from CineWinx.utils.database import delete_served_chat, get_assistant, is_on_off
from config import LOG_GROUP_ID, LOG


@app.on_message(filters.new_chat_members)
async def join_watcher(_, message: Message):
    try:
        if not await is_on_off(LOG):
            return
        userbot = await get_assistant(message.chat.id)
        chat = message.chat
        chat_id = -1000000000000 + message.chat.id
        for members in message.new_chat_members:
            if members.id == app.id:
                members_count = await app.get_chat_members_count(chat.id)
                username = (
                    message.chat.username if message.chat.username else "private chat"
                )
                username = f"@{username}" if username != "private chat" else username
                me = await app.get_me()
                msg = (
                    f"<b>{me.mention} 𝗮𝗱𝗶𝗰𝗶𝗼𝗻𝗮𝗱𝗮 𝗮 𝘂𝗺 𝗻𝗼𝘃𝗼 𝗴𝗿𝘂𝗽𝗼 #novogrupo</b>\n\n"
                    f"<b>📝 𝗡𝗼𝗺𝗲 𝗱𝗼 𝗰𝗵𝗮𝘁:</b> {message.chat.title}\n"
                    f"<b>🆔 𝗜𝗗 𝗱𝗼 𝗰𝗵𝗮𝘁:</b> {chat_id}\n"
                    f"<b>🔤 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲 𝗱𝗼 𝗖𝗵𝗮𝘁:</b> {username}\n"
                    f"<b>👥 𝗡𝘂𝗺𝗲𝗿𝗼 𝗱𝗲 𝗺𝗲𝗺𝗯𝗿𝗼𝘀:</b> {members_count}\n"
                    f"<b>👤 𝗔𝗱𝗶𝗰𝗶𝗼𝗻𝗮𝗱𝗼 𝗽𝗼𝗿:</b> {message.from_user.mention}"
                )
                await app.send_message(
                    LOG_GROUP_ID,
                    text=msg,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    f"𝗮𝗱𝗶𝗰𝗶𝗼𝗻𝗮𝗱𝗼 𝗽𝗼𝗿",
                                    url=f"tg://openmessage?user_id={message.from_user.id}",
                                )
                            ]
                        ]
                    ),
                )
                await userbot.join_chat(f"{username}")
    except Exception as e:
        print(f"Error: {e}")


@app.on_message(filters.left_chat_member)
async def on_left_chat_member(_, message: Message):
    try:
        if not await is_on_off(LOG):
            return
        userbot = await get_assistant(message.chat.id)

        left_chat_member = message.left_chat_member
        if left_chat_member and left_chat_member.id == app.id:
            remove_by = (
                message.from_user.mention
                if message.from_user
                else "Usuário Desconhecido"
            )
            title = message.chat.title
            username = (
                f"@{message.chat.username}" if message.chat.username else "Chat Privado"
            )
            chat_id = message.chat.id
            left = (
                f"<b>#saiu_do_grupo</b>\n"
                f"<b>🏷️ 𝗡𝗼𝗺𝗲 𝗱𝗼 𝗖𝗵𝗮𝘁:</b> {title}\n"
                f"<b>🆔 𝗜𝗗 𝗱𝗼 𝗖𝗵𝗮𝘁:</b> {chat_id}\n\n"
                f"<b>👤 𝗥𝗲𝗺𝗼𝘃𝗶𝗱𝗼 𝗽𝗼𝗿:</b> {remove_by}"
            )
            await app.send_message(LOG_GROUP_ID, text=left)
            await delete_served_chat(chat_id)
            await userbot.leave_chat(chat_id)
    except Exception as e:
        print(f"Error: {e}")
