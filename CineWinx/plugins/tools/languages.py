from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, Message, CallbackQuery

from CineWinx import app
from CineWinx.utils.database import get_lang, set_lang
from CineWinx.utils.decorators import actual_admin_cb, language, language_cb
from config import BANNED_USERS
from strings import get_command, get_string, languages_present


def lanuages_keyboard(_):
    keyboard = InlineKeyboard(row_width=2)
    keyboard.add(
        *[
            (
                InlineKeyboardButton(
                    text=languages_present[i],
                    callback_data=f"languages:{i}",
                )
            )
            for i in languages_present
        ]
    )
    keyboard.row(
        InlineKeyboardButton(
            text=_["BACK_BUTTON"],
            callback_data=f"settingsback_helper",
        ),
        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"close"),
    )
    return keyboard


LANGUAGE_COMMAND = get_command("LANGUAGE_COMMAND")


@app.on_message(filters.command(LANGUAGE_COMMAND) & filters.group & ~BANNED_USERS)
@language
async def langs_command(_client: app, message: Message, _):
    keyboard = lanuages_keyboard(_)
    await message.reply_text(
        _["setting_1"].format(message.chat.title, message.chat.id),
        reply_markup=keyboard,
    )


@app.on_callback_query(filters.regex("LG") & ~BANNED_USERS)
@language_cb
async def lanuagecb(_client: app, callback_query: CallbackQuery, _):
    try:
        await callback_query.answer()
    except:
        pass
    keyboard = lanuages_keyboard(_)
    return await callback_query.edit_message_reply_markup(reply_markup=keyboard)


@app.on_callback_query(filters.regex(r"languages:(.*?)") & ~BANNED_USERS)
@actual_admin_cb
async def language_markup(_client: app, callback_query: CallbackQuery, _):
    langauge = (callback_query.data).split(":")[1]
    old = await get_lang(callback_query.message.chat.id)
    if str(old) == str(langauge):
        return await callback_query.answer(
            "Você já está usando esse idioma", show_alert=True
        )
    try:
        _ = get_string(langauge)
        await callback_query.answer(
            "Seu idioma foi alterado com sucesso!", show_alert=True
        )
    except:
        return await callback_query.answer(
            "Falha ao alterar o idioma ou o idioma está em atualização",
            show_alert=True,
        )
    await set_lang(callback_query.message.chat.id, langauge)
    keyboard = lanuages_keyboard(_)
    return await callback_query.edit_message_reply_markup(reply_markup=keyboard)
