import string
from math import ceil

from pyrogram import Client, filters
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)

from CineWinx import app, AnimiZeY
from config import BANNED_USERS, PREFIXES
from strings import get_command

MOVIES_COMMAND = get_command("MOVIES_COMMAND")

context_db = {}


@app.on_message(filters.command(MOVIES_COMMAND, PREFIXES) & ~BANNED_USERS)
async def movies(client: Client, message: Message):
    input = (
        message.text.split(None, 1)[1].strip()
        if len(message.text.split()) > 1
        else (message.reply_to_message.text if message.reply_to_message else None)
    )

    context_db[message.from_user.id] = {
        "query": input,
        "page_token": None,
        "page_index": 0,
    }

    if not input:
        await message.reply_text(
            "🎬 𝗘𝗻𝗰𝗼𝗻𝘁𝗿𝗲 𝗼 𝗳𝗼𝗿𝗺𝗮𝘁𝗼 𝗱𝗲 𝗯𝘂𝘀𝗰𝗮𝗿 𝗽𝗼𝗿 𝗹𝗲𝘁𝗿𝗮 𝗼𝘂 𝗻𝘂𝗺é𝗿𝗼:",
            reply_markup=alpha_markup(),
        )


def alpha_markup(page: int = 0) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(letter, callback_data=f"alpha_{letter}")
        for letter in string.ascii_uppercase
    ]
    pairs = list(zip(buttons[::2], buttons[1::2]))

    if len(buttons) % 2 != 0:
        pairs.append((buttons[-1],))

    column_size = 3
    max_num_pages = ceil(len(pairs) / column_size)
    m_page = page % max_num_pages

    if len(pairs) > column_size:
        pairs = pairs[m_page * column_size : column_size * (m_page + 1)] + [
            (
                InlineKeyboardButton("⬅️", callback_data=f"alpha_prev_{m_page}"),
                InlineKeyboardButton("❌ 𝗙𝗲𝗰𝗵𝗮𝗿", callback_data="alpha_cancel"),
                InlineKeyboardButton("➡️", callback_data=f"alpha_next_{m_page}"),
            )
        ]
    else:
        pairs += [[InlineKeyboardButton("❌ 𝗙𝗲𝗰𝗵𝗮𝗿", callback_data="alpha_cancel")]]

    return InlineKeyboardMarkup(pairs)


@app.on_callback_query(filters.regex(r"^alpha_[A-Z]$"))
async def alpha(_client: Client, callback_query: CallbackQuery):

    data = callback_query.data.split("_")
    print("callback_query.alpha_", data)
    letter = data[1]

    await callback_query.message.delete()

    context = context_db[callback_query.from_user.id]

    context["query"] = letter
    context["page_token"] = None
    context["page_index"] = 0

    results = await AnimiZeY.search_movie(context["query"], context["page_token"])
    if not results:
        await callback_query.message.reply_text("🎬 𝗡𝗲𝗻𝗵𝘂𝗺 𝗿𝗲𝘀𝘂𝗹𝘁𝗮𝗱𝗼.")
        return

    print(results)


@app.on_callback_query(filters.regex(r"^alpha_(prev|next)_\d+$"))
async def paginate_alpha(_client: Client, callback_query: CallbackQuery):
    data = callback_query.data.split("_")
    page = int(data[2])

    if data[1] == "prev":
        page -= 1
    elif data[1] == "next":
        page += 1

    markup = alpha_markup(page)
    await callback_query.edit_message_reply_markup(markup)


@app.on_callback_query(filters.regex(r"^alpha_cancel$"))
async def cancel_alpha(client: Client, callback_query: CallbackQuery):
    await callback_query.message.delete()


class EqInlineKeyboardButton(InlineKeyboardButton):
    """
    This class is used to compare InlineKeyboardButton objects.
    """

    def __eq__(self, other: InlineKeyboardButton):
        return self.text == other.text

    def __lt__(self, other: InlineKeyboardButton):
        return self.text < other.text

    def __gt__(self, other: InlineKeyboardButton):
        return self.text > other.text
