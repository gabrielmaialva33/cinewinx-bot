import logging
import re
import unicodedata
from math import ceil

import asyncio
from pyrogram import filters, Client
from pyrogram.errors import FloodWait
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)

from CineWinx import app
from CineWinx.utils import SessionAsyncClient
from config import PREFIXES, BANNED_USERS, LX_CHT_MODELS
from strings import get_command

LLM_COMMAND = get_command("LLM_COMMAND")

context_db: dict = {}

main_prompt = (
    "Você é a AI do CineWinx. Ao responder, por favor, chame o usuário pelo nome. {0}\n\n"
    "A seguir está o prompt:\n\n{1}"
)


@app.on_message(filters.command(LLM_COMMAND, PREFIXES) & ~BANNED_USERS)
async def llm(_client: Client, message: Message):
    prompt = get_prompt(message)
    if prompt is None:
        return await message.reply_text("🦙 𝘃𝗼𝗰𝗲̂ 𝗻𝗮̃𝗼 𝗺𝗲 𝗱𝗲𝘂 𝘂𝗺 𝗽𝗿𝗼𝗺𝗽𝘁!")

    reply_to_id = (
        message.reply_to_message.id if message.reply_to_message else message.id
    )

    user_name = message.from_user.first_name
    user_name = normalize_username(user_name)
    if user_name == "":
        user_name = "Usuário"

    context_db[message.from_user.id] = {
        "prompt": prompt,
        "reply_to_id": reply_to_id,
        "user_name": user_name,
        "model_id": None,
        "model_name": None,
    }

    markup = chat_models_markup(message.from_user.id, LX_CHT_MODELS)

    await message.reply_text(
        f"🦙 𝗦𝗲𝗹𝗲𝗰𝗶𝗼𝗻𝗲 𝘂𝗺 𝗺𝗼𝗱𝗲𝗹𝗼 𝗟𝗟𝗠 👇",
        reply_markup=markup,
    )


def chat_models_markup(
        user_id: int, models: list | dict, page: int = 1
) -> InlineKeyboardMarkup:
    models = sorted(
        [
            InlineKeyboardButton(
                model["name"],
                callback_data=f"llm_{user_id}_{model['id']}_{model['name']}",
            )
            for model in models
        ],
        key=lambda x: x.text,
    )

    pairs = list(zip(models[::2], models[1::2]))
    i = 0
    for m in pairs:
        for _ in m:
            i += 1
    if len(models) - i == 1:
        pairs.append((models[-1],))
    elif len(models) - i == 2:
        pairs.append((models[-2], models[-1]))

    column_size = 3
    max_num_pages = ceil(len(pairs) / column_size)
    modulo_page = page % max_num_pages

    if len(pairs) > column_size:
        pairs = pairs[modulo_page * column_size: column_size * (modulo_page + 1)] + [
            (
                InlineKeyboardButton(
                    "⬅️ 𝗔𝗻𝘁𝗲𝗿𝗶𝗼𝗿", callback_data=f"llm_prev_{modulo_page}"
                ),
                InlineKeyboardButton("❌", callback_data=f"llm_cancel_{user_id}"),
                InlineKeyboardButton(
                    "➡️ 𝗣𝗿𝗼́𝘅𝗶𝗺𝗼", callback_data=f"llm_next_{modulo_page}"
                ),
            )
        ]
    else:
        pairs += [
            [
                InlineKeyboardButton(
                    "❌ 𝗖𝗮𝗻𝗰𝗲𝗹𝗮𝗿", callback_data=f"llm_cancel_{user_id}"
                )
            ]
        ]

    return InlineKeyboardMarkup(pairs)


@app.on_callback_query(filters.regex(pattern=r"^llm_(prev|next)_\d+"))
async def paginate_models(_: Client, callback_query: CallbackQuery):
    try:
        data = callback_query.data.split("_")
        page = int(data[2])

        if data[1] == "prev":
            page -= 1
        elif data[1] == "next":
            page += 1

        markup = chat_models_markup(callback_query.from_user.id, LX_CHT_MODELS, page)

        await callback_query.edit_message_reply_markup(markup)
    except FloodWait as e:
        logging.warning(e)
        await asyncio.sleep(e.value)
    except Exception as e:
        logging.warning(e)


@app.on_callback_query(filters.regex(pattern=r"^llm_\d+_\d+_\w+") & ~BANNED_USERS)
async def select_model(_: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.data.split("_")[1])
    model_id = int(callback_query.data.split("_")[2])
    model_name = callback_query.data.split("_")[3]

    # check if the user is the same as the one who initiated the command
    if callback_query.from_user.id != user_id:
        return await callback_query.answer("❌ 𝗡ã𝗼 𝗮𝘂𝘁𝗼𝗿𝗶𝘇𝗮𝗱𝗼.", show_alert=True)

    context_db[user_id]["model_id"] = model_id
    context_db[user_id]["model_name"] = model_name

    prompt = main_prompt.format(
        context_db[user_id]["user_name"], context_db[user_id]["prompt"]
    )

    params = {
        "prompt": prompt,
        "model_id": context_db[user_id]["model_id"],
    }

    query = await callback_query.message.edit(text="🔄 𝗚𝗲𝗿𝗮𝗻𝗱𝗼 ...", reply_markup=None)

    try:
        async with SessionAsyncClient() as client_async:
            response = await client_async.fetch(
                url=f"{client_async.url}/models",
                method="POST",
                params=params,
                json={},
                headers={"content-type": "application/json"},
            )
            if response["code"] != 2:
                return await query.edit_text(
                    f"🦙 𝗠𝗼𝗱𝗲𝗹𝗼: {context_db[user_id]['model_name']}\n"
                    f"❌ 𝗔𝗹𝗴𝗼 𝗱𝗲𝘂 𝗲𝗿𝗿𝗼, 𝘁𝗲𝗻𝘁𝗲 𝗻𝗼𝘃𝗮𝗺𝗲𝗻𝘁𝗲 𝗺𝗮𝗶𝘀 𝘁𝗮𝗿𝗱𝗲."
                )

            await query.edit_text(
                f"📝 <u>𝗣𝗿𝗼𝗺𝗽𝘁</u>: {context_db[user_id]['prompt']}"
                f"\n🦙 <u>𝗠𝗼𝗱𝗲𝗹𝗼</u>: {context_db[user_id]['model_name']}"
                f"\n📬 <u>𝗥𝗲𝘀𝗽𝗼𝘀𝘁𝗮</u>: \n\n"
                f"<i>{response['content']}</i>",
            )
    except ValueError as e:
        logging.warning(e)
        return await query.edit_text(
            f"🦙 𝗠𝗼𝗱𝗲𝗹𝗼: {context_db[user_id]['model_name']}\n"
            f"❌ 𝗔𝗹𝗴𝗼 𝗱𝗲𝘂 𝗲𝗿𝗿𝗼, 𝘁𝗲𝗻𝘁𝗲 𝗻𝗼𝘃𝗮𝗺𝗲𝗻𝘁𝗲 𝗺𝗮𝗶𝘀 𝘁𝗮𝗿𝗱𝗲."
        )
    except Exception as e:
        logging.warning(e)
        return await query.edit_text(
            f"🦙 𝗠𝗼𝗱𝗲𝗹𝗼: {context_db[user_id]['model_name']}\n"
            f"❌ 𝗔𝗹𝗴𝗼 𝗱𝗲𝘂 𝗲𝗿𝗿𝗼, 𝘁𝗲𝗻𝘁𝗲 𝗻𝗼𝘃𝗮𝗺𝗲𝗻𝘁𝗲 𝗺𝗮𝗶𝘀 𝘁𝗮𝗿𝗱𝗲."
        )

    # response = client.fetch(
    #     url=f"{client.url}/models",
    #     method="POST",
    #     params=params,
    #     json={},
    #     headers={"content-type": "application/json"},
    # )
    #
    # if response["code"] != 2:
    #     return await callback_query.edit_message_text(
    #         f"🦙 𝗠𝗼𝗱𝗲𝗹𝗼: {context_db[user_id]['model_name']}\n"
    #         f"❌ 𝗔𝗹𝗴𝗼 𝗱𝗲𝘂 𝗲𝗿𝗿𝗼, 𝘁𝗲𝗻𝘁𝗲 𝗻𝗼𝘃𝗮𝗺𝗲𝗻𝘁𝗲 𝗺𝗮𝗶𝘀 𝘁𝗮𝗿𝗱𝗲."
    #     )
    #
    # await callback_query.message.delete()
    # await callback_query.message.reply_to_message.reply_text(
    #     f"📝 <u>𝗣𝗿𝗼𝗺𝗽𝘁</u>: {context_db[user_id]['prompt']}"
    #     f"\n🦙 <u>𝗠𝗼𝗱𝗲𝗹𝗼</u>: {context_db[user_id]['model_name']}"
    #     f"\n📬 <u>𝗥𝗲𝘀𝗽𝗼𝘀𝘁𝗮</u>: \n\n"
    #     f"<i>{response['content']}</i>",
    #     reply_to_message_id=context_db[user_id]["reply_to_id"],
    # )


@app.on_callback_query(filters.regex(pattern=r"^llm_cancel_\d+") & ~BANNED_USERS)
async def cancel(_: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.data.split("_")[2])

    if callback_query.from_user.id != user_id:
        return await callback_query.answer("❌ 𝗡ã𝗼 𝗮𝘂𝘁𝗼𝗿𝗶𝘇𝗮𝗱𝗼.", show_alert=True)

    del context_db[user_id]

    await callback_query.edit_message_text("🦙 𝗠𝗼𝗱𝗲𝗹𝗼 𝗰𝗮𝗻𝗰𝗲𝗹𝗮𝗱𝗼.")


def normalize_username(username: str) -> str:
    normalized = unicodedata.normalize("NFKC", username)
    normalized = re.sub(r"\W+", "", normalized)
    return normalized


def get_prompt(message: Message) -> str:
    return message.text.split(None, 1)[1].strip() if len(message.text.split()) > 1 else (
        message.reply_to_message.text if message.reply_to_message else None
    )


__MODULE__ = "🦙 𝗟𝗟𝗠"
__HELP__ = """
🛠️ 𝗠𝗼́𝗱𝘂𝗹𝗼 𝗱𝗲 𝗟𝗶𝗻𝗴𝘂𝗮𝗴𝗲𝗺 𝗱𝗲 𝗚𝗿𝗮𝗻𝗱𝗲 𝗘𝘀𝗰𝗮𝗹𝗮

<b>📝 𝗗𝗲𝘀𝗰𝗿𝗶𝗰̧𝗮̃𝗼:</b>

- 𝗘𝘀𝘁𝗲 𝗺𝗼́𝗱𝘂𝗹𝗼 𝗽𝗲𝗿𝗺𝗶𝘁𝗲 𝗾𝘂𝗲 𝘃𝗼𝗰𝗲̂ 𝘂𝘀𝗲 𝗺𝗼𝗱𝗲𝗹𝗼𝘀 𝗱𝗲 𝗹𝗶𝗻𝗴𝘂𝗮𝗴𝗲𝗺 𝗱𝗲 𝗴𝗿𝗮𝗻𝗱𝗲 𝗲𝘀𝗰𝗮𝗹𝗮 𝗽𝗮𝗿𝗮 𝗴𝗲𝗿𝗮𝗿 𝘁𝗲𝘅𝘁𝗼 𝗰𝗼𝗺 𝗯𝗮𝘀𝗲 𝗲𝗺 𝘂𝗺 𝗽𝗿𝗼𝗺𝗽𝘁.

<b>🔖 𝗖𝗼𝗺𝗮𝗻𝗱𝗼𝘀:</b>

• <code>/llm</code> [𝘁𝗲𝘅𝘁𝗼]: 𝗚𝗲𝗿𝗲 𝘁𝗲𝘅𝘁𝗼 𝗰𝗼𝗺 𝗯𝗮𝘀𝗲 𝗻𝗼 𝗽𝗿𝗼𝗺𝗽𝘁 𝗳𝗼𝗿𝗻𝗲𝗰𝗶𝗱𝗼.

• <code>/llmgen</code> [𝘁𝗲𝘅𝘁𝗼]: 𝗚𝗲𝗿𝗲 𝘁𝗲𝘅𝘁𝗼 𝗰𝗼𝗺 𝗯𝗮𝘀𝗲 𝗻𝗼 𝗽𝗿𝗼𝗺𝗽𝘁 𝗳𝗼𝗿𝗻𝗲𝗰𝗶𝗱𝗼.

• <code>/llmgenerate</code> [𝘁𝗲𝘅𝘁𝗼]: 𝗚𝗲𝗿𝗲 𝘁𝗲𝘅𝘁𝗼 𝗰𝗼𝗺 𝗯𝗮𝘀𝗲 𝗻𝗼 𝗽𝗿𝗼𝗺𝗽𝘁 𝗳𝗼𝗿𝗻𝗲𝗰𝗶𝗱𝗼.

• <code>/llma</code> [𝘁𝗲𝘅𝘁𝗼]: 𝗚𝗲𝗿𝗲 𝘁𝗲𝘅𝘁𝗼 𝗰𝗼𝗺 𝗯𝗮𝘀𝗲 𝗻𝗼 𝗽𝗿𝗼𝗺𝗽𝘁 𝗳𝗼𝗿𝗻𝗲𝗰𝗶𝗱𝗼.

<b>💡 𝗘𝘅𝗲𝗺𝗽𝗹𝗼𝘀:</b>

• <code>/llm</code> O que é a vida?
• <code>/llmgen</code> O que é a vida?
• <code>/llma</code> Como fazer um bolo?
"""
