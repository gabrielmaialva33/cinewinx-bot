import asyncio
import logging

from pyrogram import filters, Client
from pyrogram.enums import ChatMembersFilter
from pyrogram.types import CallbackQuery, Message

from CineWinx import app
from CineWinx.core.call import CineWinx
from CineWinx.misc import db
from CineWinx.utils.database import get_authuser_names, get_cmode
from CineWinx.utils.decorators import actual_admin_cb, admin_actual, language
from CineWinx.utils.formatters import alpha_to_int
from config import BANNED_USERS, adminlist, lyrical, PREFIXES
from strings import get_command

RELOAD_COMMAND = get_command("RELOAD_COMMAND")
REBOOT_COMMAND = get_command("REBOOT_COMMAND")


@app.on_message(
    filters.command(RELOAD_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS
)
@language
async def reload_admin_cache(_client: Client, message: Message, _):
    try:
        chat_id = message.chat.id
        admins = app.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS)
        authusers = await get_authuser_names(chat_id)
        adminlist[chat_id] = []
        async for user in admins:
            if user.privileges.can_manage_video_chats:
                adminlist[chat_id].append(user.user.id)
        for user in authusers:
            user_id = await alpha_to_int(user)
            adminlist[chat_id].append(user_id)
        await message.reply_text(_["admin_20"])
    except Exception as e:
        logging.exception(e)
        await message.reply_text(
            "❌ 𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗿𝗲𝗰𝗮𝗿𝗿𝗲𝗴𝗮𝗿 𝗼 𝗰𝗮𝗰𝗵𝗲 𝗱𝗲 𝗮𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿𝗲𝘀. "
            "𝗖𝗲𝗿𝘁𝗶𝗳𝗶𝗾𝘂𝗲-𝘀𝗲 𝗱𝗲 𝗾𝘂𝗲 𝗼 𝗯𝗼𝘁 é 𝘂𝗺 𝗮𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿 𝗻𝗲𝘀𝘁𝗲 𝗰𝗵𝗮𝘁."
        )


@app.on_message(
    filters.command(REBOOT_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS
)
@admin_actual
async def restart_bot(_client: Client, message: Message, _):
    mystic = await message.reply_text(
        f"⏳ 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗮𝗴𝘂𝗮𝗿𝗱𝗲...\n🔄 𝗥𝗲𝗶𝗻𝗶𝗰𝗶𝗮𝗻𝗱𝗼 {app.mention} 𝗽𝗮𝗿𝗮 𝗼 𝘀𝗲𝘂 𝗰𝗵𝗮𝘁..."
    )
    await asyncio.sleep(1)
    try:
        db[message.chat.id] = []
        await CineWinx.stop_stream(message.chat.id)
    except Exception as e:
        logging.exception(e)
    chat_id = await get_cmode(message.chat.id)
    if chat_id:
        try:
            await app.get_chat(chat_id)
        except:
            pass
        try:
            db[chat_id] = []
            await CineWinx.stop_stream(chat_id)
        except:
            pass
    return await mystic.edit_text("Reiniciado com sucesso. \nTente tocar agora..")


@app.on_callback_query(filters.regex("close") & ~BANNED_USERS)
async def close_menu(_, callback_query: CallbackQuery):
    try:
        await callback_query.message.delete()
        await callback_query.answer()
    except Exception as e:
        logging.exception(e)
        try:
            await app.delete_messages(
                chat_id=callback_query.message.chat.id,
                message_ids=callback_query.message.id,
            )
        except Exception as e:
            logging.exception(e)
            return


@app.on_callback_query(filters.regex("close") & ~BANNED_USERS)
async def close_menu(_, callback_query: CallbackQuery):
    try:
        await callback_query.message.delete()
        await callback_query.answer()
    except:
        return


@app.on_callback_query(filters.regex("stop_downloading") & ~BANNED_USERS)
@actual_admin_cb
async def stop_download(client: Client, callback_query: CallbackQuery, _):
    message_id = callback_query.message.id
    task = lyrical.get(message_id)
    if not task:
        return await callback_query.answer("✅ 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗷á 𝗰𝗼𝗻𝗰𝗹𝘂í𝗱𝗼.", show_alert=True)
    if task.done() or task.cancelled():
        return await callback_query.answer(
            "✅ 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗷á 𝗰𝗼𝗻𝗰𝗹𝘂í𝗱𝗼 𝗼𝘂 𝗰𝗮𝗻𝗰𝗲𝗹𝗮𝗱𝗼.",
            show_alert=True,
        )
    if not task.done():
        try:
            task.cancel()
            try:
                lyrical.pop(message_id)
            except KeyError:
                pass
            await callback_query.answer("❌ 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗰𝗮𝗻𝗰𝗲𝗹𝗮𝗱𝗼", show_alert=True)
            return await callback_query.edit_message_text(
                f"❌ 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝗰𝗮𝗻𝗰𝗲𝗹𝗮𝗱𝗼 𝗽𝗼𝗿 {callback_query.from_user.mention}"
            )
        except Exception as e:
            logging.exception(e)
            return await callback_query.answer(
                "❌ 𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗽𝗮𝗿𝗮𝗿 𝗼 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱", show_alert=True
            )

    await callback_query.answer(
        "❌ 𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗿𝗲𝗰𝗼𝗻𝗵𝗲𝗰𝗲𝗿 𝗮 𝘁𝗮𝗿𝗲𝗳𝗮 𝗲𝗺 𝗲𝘅𝗲𝗰𝘂çã𝗼", show_alert=True
    )
