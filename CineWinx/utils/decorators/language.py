import logging

from pyrogram.types import CallbackQuery, Message

from CineWinx.misc import SUDOERS
from CineWinx.utils.database import get_lang, is_commanddelete_on, is_maintenance
from strings import get_string


def language(mystic: callable):
    async def wrapper(_, message, **kwargs):
        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    "🔧 𝗕𝗼𝘁 𝗲𝘀𝘁á 𝗲𝗺 𝗺𝗮𝗻𝘂𝘁𝗲𝗻çã𝗼 𝗽𝗼𝗿 𝗮𝗹𝗴𝘂𝗺 𝘁𝗲𝗺𝗽𝗼, 𝗽𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝘃𝗶𝘀𝗶𝘁𝗲 𝗼 𝗰𝗵𝗮𝘁 𝗱𝗲 𝘀𝘂𝗽𝗼𝗿𝘁𝗲 𝗽𝗮𝗿𝗮 𝘀𝗮𝗯𝗲𝗿 𝗼 𝗺𝗼𝘁𝗶𝘃𝗼."
                )
        if await is_commanddelete_on(message.chat.id):
            try:
                await message.delete()
            except Exception as e:
                logging.exception(e)
                pass
        try:
            language = await get_lang(message.chat.id)
            language = get_string(language)
        except Exception as e:
            logging.exception(e)
            language = get_string("pt")
        return await mystic(_, message, language)

    return wrapper


def language_cb(mystic: callable):
    async def wrapper(_, callback_query: CallbackQuery, **kwargs):
        if await is_maintenance() is False:
            if callback_query.from_user.id not in SUDOERS:
                return await callback_query.answer(
                    "🔧 𝗕𝗼𝘁 𝗲𝘀𝘁á 𝗲𝗺 𝗺𝗮𝗻𝘂𝘁𝗲𝗻çã𝗼 𝗽𝗼𝗿 𝗮𝗹𝗴𝘂𝗺 𝘁𝗲𝗺𝗽𝗼, 𝗽𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝘃𝗶𝘀𝗶𝘁𝗲 𝗼 𝗰𝗵𝗮𝘁 𝗱𝗲 𝘀𝘂𝗽𝗼𝗿𝘁𝗲 𝗽𝗮𝗿𝗮 𝘀𝗮𝗯𝗲𝗿 𝗼 𝗺𝗼𝘁𝗶𝘃𝗼.",
                    show_alert=True,
                )
        try:
            language = await get_lang(callback_query.message.chat.id)
            language = get_string(language)
        except Exception as e:
            logging.exception(e)
            language = get_string("pt")
        return await mystic(_, callback_query, language)

    return wrapper


def language_start(mystic: callable):
    async def wrapper(_, message: Message, **kwargs: dict):
        try:
            language = await get_lang(message.chat.id)
            language = get_string(language)
        except:
            language = get_string("pt")
        return await mystic(_, message, language)

    return wrapper
