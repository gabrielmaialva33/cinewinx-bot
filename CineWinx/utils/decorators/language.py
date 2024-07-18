from pyrogram.types import CallbackQuery, Message

from CineWinx.misc import SUDOERS
from CineWinx.utils.database import get_lang, is_commanddelete_on, is_maintenance
from strings import get_string


def language(mystic: callable):
    async def wrapper(_, message, **kwargs):
        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    "Bot está em manutenção por algum tempo, por favor, visite o chat de suporte para saber o motivo."
                )
        if await is_commanddelete_on(message.chat.id):
            try:
                await message.delete()
            except:
                pass
        try:
            language = await get_lang(message.chat.id)
            language = get_string(language)
        except:
            language = get_string("pt")
        return await mystic(_, message, language)

    return wrapper


def language_cb(mystic: callable):
    async def wrapper(_, callback_query: CallbackQuery, **kwargs):
        if await is_maintenance() is False:
            if callback_query.from_user.id not in SUDOERS:
                return await callback_query.answer(
                    "Bot está em manutenção por algum tempo, por favor, visite o chat de suporte para saber o motivo.",
                    show_alert=True,
                )
        try:
            language = await get_lang(callback_query.message.chat.id)
            language = get_string(language)
        except:
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
