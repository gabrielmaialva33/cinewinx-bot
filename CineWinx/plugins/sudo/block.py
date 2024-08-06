from pyrogram import filters
from pyrogram.types import Message

from CineWinx import app
from CineWinx.misc import SUDOERS
from CineWinx.utils.database import add_gban_user, remove_gban_user
from CineWinx.utils.decorators.language import language
from config import BANNED_USERS, PREFIXES
from strings import get_command

BLOCK_COMMAND = get_command("BLOCK_COMMAND")
UNBLOCK_COMMAND = get_command("UNBLOCK_COMMAND")
BLOCKED_COMMAND = get_command("BLOCKED_COMMAND")


@app.on_message(filters.command(BLOCK_COMMAND, PREFIXES) & SUDOERS)
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


@app.on_message(filters.command(UNBLOCK_COMMAND, PREFIXES) & SUDOERS)
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


@app.on_message(filters.command(BLOCKED_COMMAND, PREFIXES) & SUDOERS)
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


__MODULE__ = "𝗟-𝗡𝗲𝗴𝗿𝗮 🌑"
__HELP__ = """
⚠️<u>𝗙𝘂𝗻𝗰̧𝗮̃𝗼 𝗱𝗲 𝗕𝗹𝗼𝗾𝘂𝗲𝗶𝗼 𝗱𝗲 𝗖𝗵𝗮𝘁:</u>

• <code>/blacklistchat</code> [id do chat] - 𝗜𝗺𝗽𝗲𝗱𝗲 𝗾𝘂𝗲 𝘂𝗺 𝗰𝗵𝗮𝘁 𝘂𝘁𝗶𝗹𝗶𝘇𝗲 𝗼 𝗠𝘂𝘀𝗶𝗰 𝗕𝗼𝘁.

• <code>/whitelistchat</code> [id do chat] - 𝗣𝗲𝗿𝗺𝗶𝘁𝗲 𝗾𝘂𝗲 𝘂𝗺 𝗰𝗵𝗮𝘁 𝗯𝗹𝗼𝗾𝘂𝗲𝗮𝗱𝗼 𝘃𝗼𝗹𝘁𝗲 𝗮 𝘂𝘁𝗶𝗹𝗶𝘇𝗮𝗿 𝗼 𝗠𝘂𝘀𝗶𝗰 𝗕𝗼𝘁.

• <code>/blacklistedchat</code> - 𝗩𝗲𝗿𝗶𝗳𝗶𝗾𝘂𝗲 𝘁𝗼𝗱𝗼𝘀 𝗼𝘀 𝗰𝗵𝗮𝘁𝘀 𝗯𝗹𝗼𝗾𝘂𝗲𝗮𝗱𝗼𝘀.

👤<u>𝗙𝘂𝗻𝗰̧𝗮̃𝗼 𝗱𝗲 𝗕𝗹𝗼𝗾𝘂𝗲𝗶𝗼 𝗱𝗲 𝗨𝘀𝘂𝗮́𝗿𝗶𝗼:</u>

• <code>/block</code> [nome de usuário ou responder a um usuário] - 𝗜𝗺𝗽𝗲𝗱𝗲 𝘂𝗺 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗱𝗲 𝘂𝘀𝗮𝗿 𝗼𝘀 𝗰𝗼𝗺𝗮𝗻𝗱𝗼𝘀 𝗱𝗼 𝗯𝗼𝘁.

• <code>/unblock</code> [nome de usuário ou responder a um usuário] - 𝗥𝗲𝗺𝗼𝘃𝗲 𝘂𝗺 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗱𝗮 𝗹𝗶𝘀𝘁𝗮 𝗱𝗲 𝗯𝗹𝗼𝗾𝘂𝗲𝗶𝗼 𝗱𝗼 𝗕𝗼𝘁.

• <code>/blockedusers</code> - 𝗩𝗲𝗿𝗶𝗳𝗶𝗾𝘂𝗲 𝗮 𝗹𝗶𝘀𝘁𝗮 𝗱𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗯𝗹𝗼𝗾𝘂𝗲𝗮𝗱𝗼𝘀.

🌍<u>𝗙𝘂𝗻𝗰̧𝗮̃𝗼 𝗱𝗲 𝗕𝗮𝗻𝗶𝗺𝗲𝗻𝘁𝗼 𝗚𝗹𝗼𝗯𝗮𝗹:</u>

• <code>/gban</code> [nome de usuário ou responder a um usuário] - 𝗕𝗮𝗻𝗲 𝘂𝗺 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗱𝗲 𝘁𝗼𝗱𝗼𝘀 𝗼𝘀 𝗰𝗵𝗮𝘁𝘀 𝗮𝘁𝗲𝗻𝗱𝗶𝗱𝗼𝘀 𝗽𝗲𝗹𝗼 𝗯𝗼𝘁 𝗲 𝗼 𝗶𝗺𝗽𝗲𝗱𝗲 𝗱𝗲 𝘂𝘀𝗮𝗿 𝗼 𝗯𝗼𝘁.

• <code>/ungban</code> [nome de usuário ou responder a um usuário] - 𝗥𝗲𝗺𝗼𝘃𝗲 𝘂𝗺 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗱𝗮 𝗹𝗶𝘀𝘁𝗮 𝗱𝗲 𝗯𝗮𝗻𝗶𝗺𝗲𝗻𝘁𝗼 𝗴𝗹𝗼𝗯𝗮𝗹 𝗱𝗼 𝗯𝗼𝘁 𝗲 𝗽𝗲𝗿𝗺𝗶𝘁𝗲 𝗾𝘂𝗲 𝗲𝗹𝗲 𝘂𝘀𝗲 𝗼 𝗯𝗼𝘁.

• <code>/gbannedusers</code> - 𝗩𝗲𝗿𝗶𝗳𝗶𝗾𝘂𝗲 𝗮 𝗹𝗶𝘀𝘁𝗮 𝗱𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗯𝗮𝗻𝗶𝗱𝗼𝘀 𝗴𝗹𝗼𝗯𝗮𝗹𝗺𝗲𝗻𝘁𝗲.
"""
