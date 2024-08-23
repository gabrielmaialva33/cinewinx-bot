import asyncio

from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import SUPPORT_GROUP
from strings import get_string
from CineWinx import app, LOGGER
from CineWinx.misc import SUDOERS
from CineWinx.utils.database import (
    get_assistant,
    get_lang,
    is_active_chat,
    is_maintenance,
)

links = {}


def userbot_wrapper(command: callable):
    async def wrapper(client: Client, message: Message):
        language = await get_lang(message.chat.id)
        _ = get_string(language)

        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    text=f"🔧 {app.mention} 𝗲𝘀𝘁á 𝗲𝗺 𝗺𝗮𝗻𝘂𝘁𝗲𝗻𝗰̧𝗮̃𝗼, 𝘃𝗶𝘀𝗶𝘁𝗲 𝗼 <a href={SUPPORT_GROUP}>𝗰𝗵𝗮𝘁 𝗱𝗲 𝘀𝘂𝗽𝗼𝗿𝘁𝗲</a> 𝗽𝗮𝗿𝗮 𝘀𝗮𝗯𝗲𝗿 𝗼 𝗺𝗼𝘁𝗶𝘃𝗼.",
                    disable_web_page_preview=True,
                )

        try:
            await message.delete()
        except:
            pass

        chat_id = message.chat.id

        if not await is_active_chat(chat_id):
            userbot = await get_assistant(chat_id)
            try:
                try:
                    get = await app.get_chat_member(chat_id, userbot.id)
                except ChatAdminRequired:
                    return await message.edit_text(
                        f"🚫 𝗡𝗮̃𝗼 𝘁𝗲𝗻𝗵𝗼 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗽𝗮𝗿𝗮 <b>𝗰𝗼𝗻𝘃𝗶𝗱𝗮𝗿 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗽𝗼𝗿 "
                        f"𝗹𝗶𝗻𝗸</b> 𝗽𝗮𝗿𝗮 𝗮𝗱𝗶𝗰𝗶𝗼𝗻𝗮𝗿 𝗮 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 {userbot.mention} 𝗮𝗼 "
                        f"{message.chat.title}."
                    )
                if (
                        get.status == ChatMemberStatus.BANNED
                        or get.status == ChatMemberStatus.RESTRICTED
                ):
                    return await message.reply_text(
                        _["call_2"].format(
                            app.mention, userbot.id, userbot.name, userbot.username
                        ),
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        text="🔓 𝗗𝗲𝘀𝗯𝗮𝗻𝗶𝗿 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲",
                                        callback_data=f"unban_assistant",
                                    )
                                ]
                            ]
                        ),
                    )
            except UserNotParticipant:
                if message.chat.username:
                    invite_link = message.chat.username
                    await userbot.join_chat(invite_link)
                else:
                    if chat_id in links:
                        invite_link = links[chat_id]
                        try:
                            await userbot.resolve_peer(invite_link)
                        except:
                            pass
                    else:
                        try:
                            invite_link = await app.export_chat_invite_link(chat_id)
                        except ChatAdminRequired:
                            return await message.edit_text(
                                f"🚫 𝗡𝗮̃𝗼 𝘁𝗲𝗻𝗵𝗼 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗽𝗮𝗿𝗮 <b>𝗰𝗼𝗻𝘃𝗶𝗱𝗮𝗿 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗽𝗼𝗿 "
                                f"𝗹𝗶𝗻𝗸</b> 𝗽𝗮𝗿𝗮 𝗮𝗱𝗶𝗰𝗶𝗼𝗻𝗮𝗿 𝗮 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 {userbot.mention} 𝗮𝗼 "
                                f"{message.chat.title}."
                            )
                        except Exception as e:
                            LOGGER(__name__).warning(e)
                            return await message.reply_text(
                                f"{app.mention} 𝗔𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗲𝗻𝘁𝗿𝗼𝘂 𝗻𝗲𝘀𝘁𝗲 𝗴𝗿𝘂𝗽𝗼 𝗰𝗼𝗺 𝘀𝘂𝗰𝗲𝘀𝘀𝗼 ✅\n\n𝗜𝗱:- {userbot.mention}.."
                            )

                if invite_link.startswith("https://t.me/+"):
                    invite_link = invite_link.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
                myu = await message.reply_text("𝗔𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗘𝗻𝘁𝗿𝗮𝗻𝗱𝗼 𝗻𝗲𝘀𝘁𝗲 𝗖𝗵𝗮𝘁..")
                try:
                    await asyncio.sleep(1)
                    await userbot.join_chat(invite_link)
                    await myu.delete()
                    await message.reply_text(
                        f"{app.mention} 𝗔𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗲𝗻𝘁𝗿𝗼𝘂 𝗻𝗲𝘀𝘁𝗲 𝗴𝗿𝘂𝗽𝗼 𝗰𝗼𝗺 𝘀𝘂𝗰𝗲𝘀𝘀𝗼 ✅\n\n𝗜𝗱:- <b>@{userbot.username}</b>"
                    )
                except InviteRequestSent:
                    try:
                        await app.approve_chat_join_request(chat_id, userbot.id)
                    except Exception as e:
                        return await message.reply_text(
                            _["call_3"].format(app.mention, type(e).__name__)
                        )
                    await asyncio.sleep(3)
                    await myu.delete()
                    await message.reply_text(
                        f"{app.mention} 𝗔𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗲𝗻𝘁𝗿𝗼𝘂 𝗻𝗲𝘀𝘁𝗲 𝗴𝗿𝘂𝗽𝗼 𝗰𝗼𝗺 𝘀𝘂𝗰𝗲𝘀𝘀𝗼 ✅\n\n𝗜𝗱:- <b>@{userbot.username}</b>"
                    )
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    return await message.reply_text(
                        f"{app.mention} 𝗔𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗲𝗻𝘁𝗿𝗼𝘂 𝗻𝗲𝘀𝘁𝗲 𝗴𝗿𝘂𝗽𝗼 𝗰𝗼𝗺 𝘀𝘂𝗰𝗲𝘀𝘀𝗼 ✅\n\n𝗜𝗱:- <b>@{userbot.username}</b>"
                    )

                links[chat_id] = invite_link

                try:
                    await userbot.resolve_peer(chat_id)
                except:
                    pass

        return await command(client, message, _, chat_id)

    return wrapper