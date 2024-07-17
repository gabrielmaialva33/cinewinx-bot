from pyrogram import filters
from pyrogram.types import Message

from CineWinx import app
from CineWinx.misc import SUDOERS
from CineWinx.utils.database import add_gban_user, remove_gban_user
from CineWinx.utils.decorators.language import language
from config import BANNED_USERS
from strings import get_command

BLOCK_COMMAND = get_command("BLOCK_COMMAND")
UNBLOCK_COMMAND = get_command("UNBLOCK_COMMAND")
BLOCKED_COMMAND = get_command("BLOCKED_COMMAND")


@app.on_message(filters.command(BLOCK_COMMAND) & SUDOERS)
@language
async def useradd(_client: app, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id in BANNED_USERS:
            return await message.reply_text(_["block_1"].format(user.mention))
        await add_gban_user(user.id)
        BANNED_USERS.add(user.id)
        await message.reply_text(_["block_2"].format(user.mention))
        return
    if message.reply_to_message.from_user.id in BANNED_USERS:
        return await message.reply_text(
            _["block_1"].format(message.reply_to_message.from_user.mention)
        )
    await add_gban_user(message.reply_to_message.from_user.id)
    BANNED_USERS.add(message.reply_to_message.from_user.id)
    await message.reply_text(
        _["block_2"].format(message.reply_to_message.from_user.mention)
    )


@app.on_message(filters.command(UNBLOCK_COMMAND) & SUDOERS)
@language
async def userdel(_client: app, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id not in BANNED_USERS:
            return await message.reply_text(_["block_3"])
        await remove_gban_user(user.id)
        BANNED_USERS.remove(user.id)
        await message.reply_text(_["block_4"])
        return
    user_id = message.reply_to_message.from_user.id
    if user_id not in BANNED_USERS:
        return await message.reply_text(_["block_3"])
    await remove_gban_user(user_id)
    BANNED_USERS.remove(user_id)
    await message.reply_text(_["block_4"])


@app.on_message(filters.command(BLOCKED_COMMAND) & SUDOERS)
@language
async def sudoers_list(_client: app, message: Message, _):
    if not BANNED_USERS:
        return await message.reply_text(_["block_5"])
    mystic = await message.reply_text(_["block_6"])
    msg = _["block_7"]
    count = 0
    for users in BANNED_USERS:
        try:
            user = await app.get_users(users)
            user = user.first_name if not user.mention else user.mention
            count += 1
        except Exception:
            continue
        msg += f"{count}➤ {user}\n"
    if count == 0:
        return await mystic.edit_text(_["block_5"])
    else:
        return await mystic.edit_text(msg)


__MODULE__ = "Lista-Negra"
__HELP__ = """⚠️<u>Função de Bloqueio de Chat:</u>
/blacklistchat [ID_DO_CHAT] - Impede que um chat utilize o Music Bot.
/whitelistchat [ID_DO_CHAT] - Permite que um chat bloqueado volte a utilizar o Music Bot.
/blacklistedchat - Verifica todos os chats bloqueados.

👤<u>Função de Bloqueio de Usuário:</u>
/block [Nome de Usuário ou Responder a um usuário] - Impede um usuário de usar os comandos do bot.
/unblock [Nome de Usuário ou Responder a um usuário] - Remove um usuário da lista de bloqueio do Bot.
/blockedusers - Verifica a lista de usuários bloqueados.

👤<u>Função de Banimento Global:</u>
/gban [Nome de Usuário ou Responder a um usuário] - Bane um usuário de todos os chats atendidos pelo bot e o impede de usar o bot.
/ungban [Nome de Usuário ou Responder a um usuário] - Remove um usuário da lista de banimento global do bot e permite que ele use o bot.
/gbannedusers - Verifica a lista de usuários banidos globalmente.
"""
