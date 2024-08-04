from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from CineWinx import app
from CineWinx.utils import get_chats_model
from config import PREFIXES, BANNED_USERS
from strings import get_command

LLM_COMMAND = get_command("LLM_COMMAND")

prompt_db = {}

MODELS = {}


@app.on_message(filters.command(LLM_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS)
async def llm(_client: Client, message: Message):
    models = await get_chats_model()

    page = 0
    markup = chat_markup(models, page)

    await message.reply_text(
        "📝 𝗘𝗹𝗶𝗴𝗲 𝗼 𝗺𝗼𝗱𝗲𝗹𝗼 𝗾𝘂𝗲 𝗱𝗲𝘀𝗲𝗮𝘀 𝗰𝗼𝗻𝘀𝘂𝗹𝘁𝗮𝗿.",
        reply_markup=markup,
    )


# paginate models into 4 per row with next
def chat_markup(models: list, page: int):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=model["name"],
                    callback_data=f"llm_{model['id']}",
                )
                for model in models[page * 4 : page * 4 + 4]
            ],
            [
                InlineKeyboardButton(
                    "« 𝗔𝗻𝘁𝗲𝗿𝗶𝗼𝗿",
                    callback_data=f"llm_prev_{page}",
                ),
                InlineKeyboardButton(
                    "𝗦𝗶𝗴𝘂𝗶𝗲𝗻𝘁𝗲 »",
                    callback_data=f"llm_next_{page}",
                ),
            ],
        ]
    )


# Callbacks pagination
@app.on_callback_query(filters.regex(pattern=r"^llm_(prev|next)_\d+"))
async def paginate_models(_, callback_query):
    models = await get_chats_model()
    data = callback_query.data.split("_")
    page = int(data[2])

    if data[1] == "prev":
        page -= 1
    elif data[1] == "next":
        page += 1

    markup = chat_markup(models, page)

    await callback_query.edit_message_reply_markup(markup)
