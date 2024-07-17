from pyrogram import filters
from pyrogram.types import Message

from CineWinx import app
from CineWinx.misc import SUDOERS
from CineWinx.utils.database import autoend_off, autoend_on
from strings import get_command

AUTOEND_COMMAND = get_command("AUTOEND_COMMAND")


@app.on_message(filters.command(AUTOEND_COMMAND) & SUDOERS)
async def auto_end_stream(_client: app, message: Message):
    usage = "*Uso:**\n\n/autoend [enable|disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        await autoend_on()
        await message.reply_text(
            "Encerramento automático de transmissão ativado.\n\nO bot sairá do chat de voz automaticamente após 3 "
            "minutos se ninguém estiver ouvindo, com uma mensagem de aviso."
        )
    elif state == "disable":
        await autoend_off()
        await message.reply_text("Encerramento automático desativado")
    else:
        await message.reply_text(usage)
