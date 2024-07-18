from pyrogram import filters
from pyrogram.types import Message

from CineWinx import app
from CineWinx.misc import SUDOERS
from CineWinx.utils.database import add_sudo, remove_sudo
from CineWinx.utils.decorators.language import language
from config import BANNED_USERS, MONGO_DB_URI, OWNER_ID
from strings import get_command

ADDSUDO_COMMAND = get_command("ADDSUDO_COMMAND")
DELSUDO_COMMAND = get_command("DELSUDO_COMMAND")
SUDOUSERS_COMMAND = get_command("SUDOUSERS_COMMAND")


@app.on_message(filters.command(ADDSUDO_COMMAND) & filters.user(OWNER_ID))
@language
async def useradd(_client: app, message: Message, _):
    if MONGO_DB_URI is None:
        return await message.reply_text(
            "<b>Devido a questões de privacidade do bot, você não pode gerenciar usuários sudo ao usar o banco de "
            "dados do Winx.</b>\n\n<b>Por favor, preencha sua MONGO_DB_URI nas suas variáveis de ambiente para usar "
            "esta função.</b>"
        )
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id in SUDOERS:
            return await message.reply_text(_["sudo_1"].format(user.mention))
        added = await add_sudo(user.id)
        if added:
            SUDOERS.add(user.id)
            await message.reply_text(_["sudo_2"].format(user.mention))
        else:
            await message.reply_text("Falhou")
        return
    if message.reply_to_message.from_user.id in SUDOERS:
        return await message.reply_text(
            _["sudo_1"].format(message.reply_to_message.from_user.mention)
        )
    added = await add_sudo(message.reply_to_message.from_user.id)
    if added:
        SUDOERS.add(message.reply_to_message.from_user.id)
        await message.reply_text(
            _["sudo_2"].format(message.reply_to_message.from_user.mention)
        )
    else:
        await message.reply_text("Falhou")
    return


@app.on_message(filters.command(DELSUDO_COMMAND) & filters.user(OWNER_ID))
@language
async def userdel(_client: app, message: Message, _):
    if MONGO_DB_URI is None:
        return await message.reply_text(
            "<b>Devido a questões de privacidade do bot, você não pode gerenciar usuários sudo ao usar o banco de "
            "dados do Winx.</b>\n\n<b>Por favor, preencha sua MONGO_DB_URI nas suas variáveis de ambiente para usar "
            "esta função.</b>"
        )
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id not in SUDOERS:
            return await message.reply_text(_["sudo_3"])
        removed = await remove_sudo(user.id)
        if removed:
            SUDOERS.remove(user.id)
            await message.reply_text(_["sudo_4"])
            return
        await message.reply_text(f"Algo deu errado.")
        return
    user_id = message.reply_to_message.from_user.id
    if user_id not in SUDOERS:
        return await message.reply_text(_["sudo_3"])
    removed = await remove_sudo(user_id)
    if removed:
        SUDOERS.remove(user_id)
        await message.reply_text(_["sudo_4"])
        return
    await message.reply_text(f"Algo deu errado.")


@app.on_message(filters.command(SUDOUSERS_COMMAND) & ~BANNED_USERS)
@language
async def sudoers_list(_client: app, message: Message, _):
    text = _["sudo_5"]
    count = 0
    for x in OWNER_ID:
        try:
            user = await app.get_users(x)
            user = user.first_name if not user.mention else user.mention
            count += 1
        except Exception:
            continue
        text += f"{count}➤ {user}\n"
    smex = 0
    for user_id in SUDOERS:
        if user_id not in OWNER_ID:
            try:
                user = await app.get_users(user_id)
                user = user.first_name if not user.mention else user.mention
                if smex == 0:
                    smex += 1
                    text += _["sudo_6"]
                count += 1
                text += f"{count}➤ {user}\n"
            except Exception:
                continue
    if not text:
        await message.reply_text(_["sudo_7"])
    else:
        await message.reply_text(text)
