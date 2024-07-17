from pyrogram import filters
from pyrogram.types import Message

from CineWinx import app
from CineWinx.misc import SUDOERS
from CineWinx.utils.database.memorydatabase import (
    get_active_chats,
    get_active_video_chats,
)
from strings import get_command

ACTIVEVC_COMMAND = get_command("ACTIVEVC_COMMAND")
ACTIVEVIDEO_COMMAND = get_command("ACTIVEVIDEO_COMMAND")


@app.on_message(filters.command(ACTIVEVC_COMMAND) & SUDOERS)
async def activevc(_, message: Message):
    mystic = await message.reply_text("Obtendo o chat de voz ativo... Por favor, aguarde")
    served_chats = await get_active_chats()
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
        except Exception:
            title = "Grupo privado"
        if (await app.get_chat(x)).username:
            user = (await app.get_chat(x)).username
            text += f"<b>{j + 1}.</b>  [{title}](https://t.me/{user})[`{x}`]\n"
        else:
            text += f"<b>{j + 1}. {title}</b> [`{x}`]\n"
        j += 1
    if not text:
        await mystic.edit_text("Nenhum chat de voz ativo")
    else:
        await mystic.edit_text(
            f"**Chats de Voz Ativos:**\n\n{text}",
            disable_web_page_preview=True,
        )


@app.on_message(filters.command(ACTIVEVIDEO_COMMAND) & SUDOERS)
async def activevi_(_, message: Message):
    mystic = await message.reply_text("Obtendo chats de voz ativos... Por favor, aguarde")
    served_chats = await get_active_video_chats()
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
        except Exception:
            title = "Grupo privado"
        if (await app.get_chat(x)).username:
            user = (await app.get_chat(x)).username
            text += f"<b>{j + 1}.</b>  [{title}](https://t.me/{user})[`{x}`]\n"
        else:
            text += f"<b>{j + 1}. {title}</b> [`{x}`]\n"
        j += 1
    if not text:
        await mystic.edit_text("Nenhum chat de vídeo ativo")
    else:
        await mystic.edit_text(
            f"**Chats de Vídeo Ativos:**\n\n{text}",
            disable_web_page_preview=True,
        )


@app.on_message(filters.command(["ac"]) & SUDOERS)
async def vc(client: app, message: Message):
    ac_audio = str(len(await get_active_chats()))
    ac_video = str(len(await get_active_video_chats()))
    await message.reply_text(
        f"✫ **<u>Informações de Chats Ativos</u>**:\n\nVoz: {ac_audio}\nVídeo: {ac_video}"
    )


__MODULE__ = "Ativos"
__HELP__ = """<u>Comandos de Chats Ativos:</u>
/ac - Verificar os chats de voz ativos no bot.
/activevoice - Verificar os chats de voz e chamadas de vídeo ativos no bot.
/activevideo - Verificar as chamadas de vídeo ativas no bot.
/stats - Verificar as estatísticas do bot."""
