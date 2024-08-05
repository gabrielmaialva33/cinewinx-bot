import asyncio
import logging

from pyrogram import filters, Client, enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from CineWinx import app
from CineWinx.utils.permissions import admins_only
from config import BANNED_USERS, PREFIXES
from strings import get_command

chat_queue = []

stop_process = False

ZOMBIES_COMMAND = get_command("ZOMBIES_COMMAND")


@app.on_message(
    filters.command(ZOMBIES_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS
)
@admins_only("can_restrict_members")
async def remove(_client: Client, message: Message):
    global stop_process
    try:
        try:
            sender = await app.get_chat_member(message.chat.id, message.from_user.id)
            has_permissions = sender.privileges
        except BaseException as e:
            logging.error(str(e))
            has_permissions = message.sender_chat
        if has_permissions:
            bot = await app.get_chat_member(message.chat.id, "self")
            if bot.status == ChatMemberStatus.MEMBER:
                await message.reply(
                    "🚫 𝗣𝗿𝗲𝗰𝗶𝘀𝗼 𝗱𝗲 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗼̃𝗲𝘀 𝗱𝗲 𝗮𝗱𝗺𝗶𝗻 𝗽𝗮𝗿𝗮 𝗿𝗲𝗺𝗼𝘃𝗲𝗿 𝗰𝗼𝗻𝘁𝗮𝘀 𝗲𝘅𝗰𝗹𝘂𝗶́𝗱𝗮𝘀. 🛠️"
                )
            else:
                if len(chat_queue) > 30:
                    await message.reply(
                        "🙇‍♂️ 𝗝𝗮́ 𝗲𝘀𝘁𝗼𝘂 𝘁𝗿𝗮𝗯𝗮𝗹𝗵𝗮𝗻𝗱𝗼 𝗻𝗼 𝗺𝗲𝘂 𝗻𝘂́𝗺𝗲𝗿𝗼 𝗺𝗮́𝘅𝗶𝗺𝗼 𝗱𝗲 "
                        "𝟯𝟬 𝗰𝗵𝗮𝘁𝘀 𝗮𝗴𝗼𝗿𝗮. 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝘁𝗲𝗻𝘁𝗲 𝗻𝗼𝘃𝗮𝗺𝗲𝗻𝘁𝗲 𝗲𝗺 "
                        "𝗯𝗿𝗲𝘃𝗲. ⏳"
                    )
                else:
                    if message.chat.id in chat_queue:
                        await message.reply(
                            "🔄 𝗝𝗮́ 𝗲𝘅𝗶𝘀𝘁𝗲 𝘂𝗺 𝗽𝗿𝗼𝗰𝗲𝘀𝘀𝗼 𝗲𝗺 𝗮𝗻𝗱𝗮𝗺𝗲𝗻𝘁𝗼 𝗻𝗲𝘀𝘁𝗲 𝗰𝗵𝗮𝘁. "
                            "𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗱𝗶𝗴𝗶𝘁𝗲 [ /stop ] 𝗽𝗮𝗿𝗮 𝗶𝗻𝗶𝗰𝗶𝗮𝗿 𝘂𝗺 𝗻𝗼𝘃𝗼. 🚫"
                        )
                    else:
                        chat_queue.append(message.chat.id)
                        deleted_list = []
                        async for member in app.get_chat_members(message.chat.id):
                            if member.user.is_deleted:
                                deleted_list.append(member.user)
                            else:
                                pass
                        len_deleted_list = len(deleted_list)
                        if len_deleted_list == 0:
                            await message.reply(
                                "👤 𝗡𝗮̃𝗼 𝗵𝗮́ 𝗰𝗼𝗻𝘁𝗮𝘀 𝗲𝘅𝗰𝗹𝘂𝗶́𝗱𝗮𝘀 𝗻𝗲𝘀𝘁𝗲 𝗰𝗵𝗮𝘁. 🚫"
                            )
                            chat_queue.remove(message.chat.id)
                        else:
                            k = 0
                            process_time = len_deleted_list * 1
                            temp = await app.send_message(
                                message.chat.id,
                                f"🧭 𝗧𝗼𝘁𝗮𝗹 𝗱𝗲 {len_deleted_list} 𝗰𝗼𝗻𝘁𝗮𝘀 𝗲𝘅𝗰𝗹𝘂𝗶́𝗱𝗮𝘀 𝗳𝗼𝗶 "
                                f"𝗱𝗲𝘁𝗲𝘁𝗮𝗱𝗼.\n⏳ 𝗧𝗲𝗺𝗽𝗼 𝗲𝘀𝘁𝗶𝗺𝗮𝗱𝗼: {process_time} "
                                f"𝘀𝗲𝗴𝘂𝗻𝗱𝗼𝘀 𝗮 𝗽𝗮𝗿𝘁𝗶𝗿 𝗱𝗲 𝗮𝗴𝗼𝗿𝗮.",
                            )
                            if stop_process:
                                stop_process = False
                            while len(deleted_list) > 0 and not stop_process:
                                deleted_account = deleted_list.pop(0)
                                try:
                                    await app.ban_chat_member(
                                        message.chat.id, deleted_account.id
                                    )
                                except FloodWait as e:
                                    await asyncio.sleep(e.value)
                                except Exception as e:
                                    logging.error(str(e))
                                k += 1
                            if k == len_deleted_list:
                                await message.reply(
                                    f"✅ 𝗦𝘂𝗰𝗲𝘀𝘀𝗼 𝗮𝗼 𝗿𝗲𝗺𝗼𝘃𝗲𝗿 𝘁𝗼𝗱𝗮𝘀 𝗮𝘀 𝗰𝗼𝗻𝘁𝗮𝘀 𝗲𝘅𝗰𝗹𝘂𝗶́𝗱𝗮𝘀 𝗱𝗲𝘀𝘀𝗲 𝗰𝗵𝗮𝘁. 🗑️"
                                )
                                await temp.delete()
                            else:
                                await message.reply(
                                    f"✅ 𝗦𝘂𝗰𝗲𝘀𝘀𝗼 𝗮𝗼 𝗿𝗲𝗺𝗼𝘃𝗲𝗿 {k} 𝗰𝗼𝗻𝘁𝗮𝘀 𝗲𝘅𝗰𝗹𝘂𝗶́𝗱𝗮𝘀 𝗱𝗲𝘀𝘀𝗲 𝗰𝗵𝗮𝘁. 🗑️"
                                )
                                await temp.delete()
                            chat_queue.remove(message.chat.id)
        else:
            await message.reply(
                f"👮🏻 𝗗𝗲𝘀𝗰𝘂𝗹𝗽𝗲, <b>𝘀𝗼́ 𝗮𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿𝗲𝘀</b> 𝗽𝗼𝗱𝗲𝗺 𝗲𝘅𝗲𝗰𝘂𝘁𝗮𝗿 𝗲𝘀𝘁𝗲 𝗰𝗼𝗺𝗮𝗻𝗱𝗼."
            )
    except FloodWait as e:
        await asyncio.sleep(e.value)


@app.on_message(filters.command(["admins", "staff"]) & filters.group & ~BANNED_USERS)
async def admins(_client: Client, message: Message):
    try:
        admin_list = []
        owner_list = []
        async for admin in app.get_chat_members(
            message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS
        ):
            if not admin.privileges.is_anonymous:
                if admin.user.is_bot:
                    pass
                elif admin.status == ChatMemberStatus.OWNER:
                    owner_list.append(admin.user)
                else:
                    admin_list.append(admin.user)
            else:
                pass
        len_admin_list = len(owner_list) + len(admin_list)
        text2 = f"<b>👥 𝗘𝗾𝘂𝗶𝗽𝗲 𝗱𝗼 𝗚𝗿𝘂𝗽𝗼 - {message.chat.title}</b>\n\n"
        try:
            owner = owner_list[0]
            if owner.username is None:
                text2 += f"👑 𝗗𝗼𝗻𝗼\n└ {owner.mention}\n\n👮🏻 𝗔𝗱𝗺𝗶𝗻𝘀\n"
            else:
                text2 += f"👑 𝗗𝗼𝗻𝗼\n└ @{owner.username}\n\n👮🏻 𝗔𝗱𝗺𝗶𝗻𝘀\n"
        except IndexError:
            text2 += f"👑 𝗗𝗼𝗻𝗼\n└ <i>𝗘𝘀𝗰𝗼𝗻𝗱𝗶𝗱𝗼</i>\n\n👮🏻 𝗔𝗱𝗺𝗶𝗻𝘀\n"
        if len(admin_list) == 0:
            text2 += "└ <i>𝗔𝗱𝗺𝗶𝗻𝘀 𝗲𝘀𝘁𝗮̃𝗼 𝗲𝘀𝗰𝗼𝗻𝗱𝗶𝗱𝗼𝘀</i>"
            await app.send_message(message.chat.id, text2)
        else:
            while len(admin_list) > 1:
                admin = admin_list.pop(0)
                if admin.username is None:
                    text2 += f"├ {admin.mention}\n"
                else:
                    text2 += f"├ @{admin.username}\n"
            else:
                admin = admin_list.pop(0)
                if admin.username is None:
                    text2 += f"└ {admin.mention}\n\n"
                else:
                    text2 += f"└ @{admin.username}\n\n"
            text2 += f"✅ | <b>𝗧𝗼𝘁𝗮𝗹 𝗱𝗲 𝗔𝗱𝗺𝗶𝗻𝘀</b>: {len_admin_list}"
            await app.send_message(message.chat.id, text2)
    except FloodWait as e:
        await asyncio.sleep(e.value)


@app.on_message(filters.command("bots"))
async def bots(_client: Client, message: Message):
    try:
        bot_list = []
        async for bot in app.get_chat_members(
            message.chat.id, filter=enums.ChatMembersFilter.BOTS
        ):
            bot_list.append(bot.user)
        len_bot_list = len(bot_list)
        text3 = f"<b>🤖 𝗟𝗶𝘀𝘁𝗮 𝗱𝗲 𝗕𝗼𝘁𝘀 - {message.chat.title}</b>\n\n🤖 𝗕𝗼𝘁𝘀\n"
        while len(bot_list) > 1:
            bot = bot_list.pop(0)
            text3 += f"├ @{bot.username}\n"
        else:
            bot = bot_list.pop(0)
            text3 += f"└ @{bot.username}\n\n"
            text3 += f"✅ | <b>𝗧𝗼𝘁𝗮𝗹 𝗱𝗲 𝗕𝗼𝘁𝘀</b>: {len_bot_list}"
            await app.send_message(message.chat.id, text3)
    except FloodWait as e:
        await asyncio.sleep(e.value)


__MODULE__ = "🧟‍♂️ 𝗭𝗼𝗺𝗯𝗶𝗲𝘀"
__HELP__ = """
🛠️ 𝗠𝗼́𝗱𝘂𝗹𝗼 𝗱𝗲 𝗙𝗲𝗿𝗿𝗮𝗺𝗲𝗻𝘁𝗮𝘀 𝗱𝗲 𝗔𝗱𝗺𝗶𝗻𝘀

<b>📝 𝗗𝗲𝘀𝗰𝗿𝗶𝗰̧𝗮̃𝗼:</b>

- 𝗘𝘀𝘁𝗲 𝗺𝗼́𝗱𝘂𝗹𝗼 𝗽𝗿𝗼𝘃𝗶𝗱𝗲𝗻𝗰𝗶𝗮 𝗳𝗲𝗿𝗿𝗮𝗺𝗲𝗻𝘁𝗮𝘀 𝗽𝗮𝗿𝗮 𝗮𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿𝗲𝘀 𝗱𝗲 𝗴𝗿𝘂𝗽𝗼𝘀 𝗴𝗲𝗿𝗲𝗻𝗰𝗶𝗮𝗿𝗲𝗺 𝗼 𝗴𝗿𝘂𝗽𝗼 𝗲𝗳𝗲𝘁𝗶𝘃𝗮𝗺𝗲𝗻𝘁𝗲.

📋 𝗖𝗼𝗺𝗮𝗻𝗱𝗼𝘀:

• <code>/zombies</code>: 𝗥𝗲𝗺𝗼𝘃𝗲𝗿 𝗰𝗼𝗻𝘁𝗮𝘀 𝗲𝘅𝗰𝗹𝘂𝗶́𝗱𝗮𝘀 𝗱𝗼 𝗴𝗿𝘂𝗽𝗼. 🗑️

• <code>/admins</code> ou <code>/staff</code>: 𝗢𝗯𝘁𝗲𝗿 𝘂𝗺𝗮 𝗹𝗶𝘀𝘁𝗮 𝗱𝗲 𝗮𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿𝗲𝘀 𝗲 𝗱𝗼𝗻𝗼𝘀 𝗱𝗼 𝗴𝗿𝘂𝗽𝗼. 👮🏻

• <code>/bots</code>: 𝗢𝗯𝘁𝗲𝗿 𝘂𝗺𝗮 𝗹𝗶𝘀𝘁𝗮 𝗱𝗲 𝗯𝗼𝘁𝘀 𝗻𝗼 𝗴𝗿𝘂𝗽𝗼. 🤖
"""
