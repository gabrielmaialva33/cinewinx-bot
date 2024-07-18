import asyncio
import logging

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.types import CallbackQuery, Message

from CineWinx import app
from CineWinx.core.call import CineWinx
from CineWinx.misc import db
from CineWinx.utils.database import get_authuser_names, get_cmode
from CineWinx.utils.decorators import actual_admin_cb, admin_actual, language
from CineWinx.utils.formatters import alpha_to_int
from config import BANNED_USERS, adminlist, lyrical
from strings import get_command

RELOAD_COMMAND = get_command("RELOAD_COMMAND")
REBOOT_COMMAND = get_command("REBOOT_COMMAND")


@app.on_message(filters.command(RELOAD_COMMAND) & filters.group & ~BANNED_USERS)
@language
async def reload_admin_cache(_client: app, message: Message, _):
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
    except:
        await message.reply_text(
            "Falha ao recarregar o cache de administradores. Certifique-se de que o bot é um administrador neste chat."
        )


@app.on_message(filters.command(REBOOT_COMMAND) & filters.group & ~BANNED_USERS)
@admin_actual
async def restartbot(_client: app, message: Message, _):
    mystic = await message.reply_text(
        f"Por favor, aguarde...\nReiniciando {app.mention} para o seu chat..."
    )
    await asyncio.sleep(1)
    try:
        db[message.chat.id] = []
        await CineWinx.stop_stream(message.chat.id)
    except:
        pass
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
async def stop_download(client, callback_query: CallbackQuery, _):
    message_id = callback_query.message.id
    task = lyrical.get(message_id)
    if not task:
        return await callback_query.answer("Download já concluído..", show_alert=True)
    if task.done() or task.cancelled():
        return await callback_query.answer(
            "Download já concluído ou cancelado.",
            show_alert=True,
        )
    if not task.done():
        try:
            task.cancel()
            try:
                lyrical.pop(message_id)
            except:
                pass
            await callback_query.answer("Download cancelado", show_alert=True)
            return await callback_query.edit_message_text(
                f"Download cancelado por {callback_query.from_user.mention}"
            )
        except:
            return await callback_query.answer(
                "Falha ao parar o download", show_alert=True
            )

    await callback_query.answer(
        "Falha ao reconhecer a tarefa em execução", show_alert=True
    )
