import logging

from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, Message, CallbackQuery

from CineWinx import app
from CineWinx.utils.database import get_lang, set_lang
from CineWinx.utils.decorators import actual_admin_cb, language, language_cb
from config import BANNED_USERS, PREFIXES
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


@app.on_message(
    filters.command(LANGUAGE_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS
)
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
    except Exception as e:
        logging.error(e)
    keyboard = lanuages_keyboard(_)
    return await callback_query.edit_message_reply_markup(reply_markup=keyboard)


@app.on_callback_query(filters.regex(r"languages:(.*?)") & ~BANNED_USERS)
@actual_admin_cb
async def language_markup(_client: app, callback_query: CallbackQuery, _):
    langauge = (callback_query.data).split(":")[1]
    old = await get_lang(callback_query.message.chat.id)
    if str(old) == str(langauge):
        return await callback_query.answer(
            "🌐 𝗩𝗼𝗰𝗲̂ 𝗷𝗮́ 𝗲𝘀𝘁𝗮́ 𝘂𝘀𝗮𝗻𝗱𝗼 𝗲𝘀𝘀𝗲 𝗶𝗱𝗶𝗼𝗺𝗮", show_alert=True
        )
    try:
        _ = get_string(langauge)
        await callback_query.answer(
            "🌐 𝗦𝗲𝘂 𝗶𝗱𝗶𝗼𝗺𝗮 𝗳𝗼𝗶 𝗮𝗹𝘁𝗲𝗿𝗮𝗱𝗼 𝗰𝗼𝗺 𝘀𝘂𝗰𝗲𝘀𝘀𝗼!", show_alert=True
        )
    except Exception as e:
        logging.error(str(e))
        return await callback_query.answer(
            "❌ 𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗮𝗹𝘁𝗲𝗿𝗮𝗿 𝗼 𝗶𝗱𝗶𝗼𝗺𝗮 𝗼𝘂 𝗼 𝗶𝗱𝗶𝗼𝗺𝗮 𝗲𝘀𝘁𝗮́ 𝗲𝗺 𝗮𝘁𝘂𝗮𝗹𝗶𝘇𝗮𝗰̧𝗮̃𝗼",
            show_alert=True,
        )
    await set_lang(callback_query.message.chat.id, langauge)
    keyboard = lanuages_keyboard(_)
    return await callback_query.edit_message_reply_markup(reply_markup=keyboard)
