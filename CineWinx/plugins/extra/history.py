import asyncio
import logging
import random

from pyrogram import Client, filters
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.types import Message

from CineWinx import app
from CineWinx.core.userbot import assistants
from CineWinx.utils.database import get_client
from config import BANNED_USERS


@app.on_message(filters.command(["sg", "history"]) & filters.group & ~BANNED_USERS)
async def sg(client: Client, message: Message):
    if len(message.text.split()) < 2 and not message.reply_to_message:
        return await message.reply("📢 𝘀𝗴 𝘂𝘀𝗲𝗿𝗻𝗮𝗺𝗲 / 𝗶𝗱 / 𝗿𝗲𝗽𝗹𝘆")
    if message.reply_to_message:
        args = message.reply_to_message.from_user.id
    else:
        args = message.text.split()[1:]
        if not args:
            return await message.reply(
                "🔍 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗳𝗼𝗿𝗻𝗲𝗰̧𝗮 𝘂𝗺 𝗻𝗼𝗺𝗲 𝗱𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼, 𝗜𝗗 𝗼𝘂 𝗿𝗲𝗽𝗹𝘆 𝗮 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺."
            )
        args = args[0]
    lol = await message.reply("<code>🔄 𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗮𝗻𝗱𝗼...</code>")
    if args:
        try:
            user = await client.get_users(f"{args}")
        except Exception as e:
            logging.error(e)
            return await lol.edit(
                "<code>❗️ 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗲𝘀𝗽𝗲𝗰𝗶𝗳𝗶𝗾𝘂𝗲 𝘂𝗺 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝘃𝗮́𝗹𝗶𝗱𝗼!</code>"
            )

    sg_bot = ["sangmata_bot", "sangmata_beta_bot"]
    sg = random.choice(sg_bot)
    winx = random.choice(assistants)
    ubot = await get_client(winx)

    try:
        a = await ubot.send_message(sg, f"{user.id}")
        await a.delete()
    except Exception as e:
        return await lol.edit(str(e))
    await asyncio.sleep(1)

    async for stalk in ubot.search_messages(a.chat.id):
        if stalk.text is None:
            continue
        if not stalk:
            await message.reply("🤖 𝗢 𝗯𝗼𝘁 𝗲𝘀𝘁𝗮́ 𝗻𝗲𝗿𝘃𝗼𝘀𝗼")
        elif stalk:
            await message.reply(f"{stalk.text}")
            break

    try:
        user_info = await ubot.resolve_peer(sg)
        await ubot.send(DeleteHistory(peer=user_info, max_id=0, revoke=True))
    except Exception as e:
        logging.warning(e)

    await lol.delete()


__MODULE__ = "📜 𝗛𝗶𝘀𝘁𝗼́𝗿𝗶𝗰𝗼"
__HELP__ = """
## 📚 𝗔𝗷𝘂𝗱𝗮 𝗱𝗲 𝗖𝗼𝗺𝗮𝗻𝗱𝗼𝘀 𝗱𝗲 𝗛𝗶𝘀𝘁𝗼́𝗿𝗶𝗰𝗼

### 1. /sg ou /History
<b>📝 𝗗𝗲𝘀𝗰𝗿𝗶𝗰̧𝗮̃𝗼:</b>
𝗢𝗯𝘁𝗲𝗺 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗮𝗹𝗲𝗮𝘁𝗼́𝗿𝗶𝗮 𝗱𝗼 𝗵𝗶𝘀𝘁𝗼́𝗿𝗶𝗰𝗼 𝗱𝗲 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗻𝘀 𝗱𝗲 𝘂𝗺 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼.

<b>🔧 𝗨𝘀𝗼:</b>
/sg [nome de usuário / id / resposta]

<b>📋 𝗗𝗲𝘁𝗮𝗹𝗵𝗲𝘀:</b>
- 𝗢𝗯𝘁𝗲́𝗺 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗮𝗹𝗲𝗮𝘁𝗼́𝗿𝗶𝗮 𝗱𝗼 𝗵𝗶𝘀𝘁𝗼́𝗿𝗶𝗰𝗼 𝗱𝗲 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗻𝘀 𝗱𝗼 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗲𝘀𝗽𝗲𝗰𝗶𝗳𝗶𝗰𝗮𝗱𝗼.
- 𝗣𝗼𝗱𝗲 𝘀𝗲𝗿 𝘂𝘀𝗮𝗱𝗼 𝗳𝗼𝗿𝗻𝗲𝗰𝗲𝗻𝗱𝗼 𝘂𝗺 𝗻𝗼𝗺𝗲 𝗱𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼, 𝗜𝗗 𝗱𝗲 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼 𝗼𝘂 𝗿𝗲𝘀𝗽𝗼𝗻𝗱𝗲𝗻𝗱𝗼 𝗮 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗱𝗼 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼.
- 𝗔𝗰𝗲𝘀𝘀𝗶́𝘃𝗲𝗹 𝗮𝗽𝗲𝗻𝗮𝘀 𝗽𝗲𝗹𝗼𝘀 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲𝘀 𝗱𝗼 𝗯𝗼𝘁.

<b>💡 𝗘𝘅𝗲𝗺𝗽𝗹𝗼𝘀:</b>
- <code>/sg nome_de_usuário</code>
- <code>/sg user_id</code>
- <code>/sg [responder a uma mensagem]</code>
"""
