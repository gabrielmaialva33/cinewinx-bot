import asyncio
import logging
from math import ceil

from pyrogram import filters, Client
from pyrogram.errors import FloodWait
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    InputMediaPhoto,
)

from CineWinx import app
from CineWinx.utils import SessionAsyncClient, normalize_string
from config import PREFIXES, BANNED_USERS, LX_IMG_MODELS
from strings import get_command

DRAW_COMMAND = get_command("DRAW_COMMAND")

context_db = {}


@app.on_message(filters.command(DRAW_COMMAND, PREFIXES) & ~BANNED_USERS)
async def draw(_client: Client, message: Message):
    prompt, negative_prompt = get_prompt(message, PREFIXES)
    if prompt is None:
        return await message.reply_text("🖍️ 𝘃𝗼𝗰𝗲̂ 𝗻𝗮̃𝗼 𝗺𝗲 𝗱𝗲𝘂 𝘂𝗺 𝗽𝗿𝗼𝗺𝗽𝘁 𝗽𝗮𝗿𝗮 𝗱𝗲𝘀𝗲𝗻𝗵𝗮𝗿!")

    markup = image_models_markup(message.from_user.id, LX_IMG_MODELS)

    context_db[message.from_user.id] = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "reply_to_id": message.id,
    }

    await message.reply_text(
        f"✨ 𝗦𝗲𝗹𝗲𝗰𝗶𝗼𝗻𝗲 𝘂𝗺 𝗺𝗼𝗱𝗲𝗹𝗼 👇",
        reply_markup=markup,
    )


def image_models_markup(
    user_id: int, models: list | dict, page: int = 0
) -> InlineKeyboardMarkup:
    models = sorted(
        [
            InlineKeyboardButton(
                model["name"],
                callback_data=f"select_{user_id}_{model['id']}_{model['name']}",
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
        pairs = pairs[modulo_page * column_size : column_size * (modulo_page + 1)] + [
            (
                InlineKeyboardButton(
                    "⬅️ 𝗔𝗻𝘁𝗲𝗿𝗶𝗼𝗿", callback_data=f"draw_prev_{modulo_page}"
                ),
                InlineKeyboardButton("❌", callback_data=f"draw_cancel_{user_id}"),
                InlineKeyboardButton(
                    "➡️ 𝗣𝗿𝗼́𝘅𝗶𝗺𝗼", callback_data=f"draw_next_{modulo_page}"
                ),
            )
        ]
    else:
        pairs += [
            [
                InlineKeyboardButton(
                    "❌ 𝗖𝗮𝗻𝗰𝗲𝗹𝗮𝗿", callback_data=f"draw_cancel_{user_id}"
                )
            ]
        ]

    return InlineKeyboardMarkup(pairs)


@app.on_callback_query(filters.regex(pattern=r"^draw_(prev|next)_\d+") & ~BANNED_USERS)
async def paginate_models(_: Client, callback_query: CallbackQuery):
    try:
        data = callback_query.data.split("_")
        page = int(data[2])

        if data[1] == "prev":
            page -= 1
        elif data[1] == "next":
            page += 1

        markup = image_models_markup(callback_query.from_user.id, LX_IMG_MODELS, page)

        await callback_query.edit_message_reply_markup(markup)
    except FloodWait as e:
        logging.warning(e)
        await asyncio.sleep(e.value)
    except Exception as e:
        logging.warning(e)


@app.on_callback_query(filters.regex(pattern=r"^select_\d+_\d+_\w+") & ~BANNED_USERS)
async def select_model(_: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.data.split("_")[1])
    model_id = int(callback_query.data.split("_")[2])
    model_name = callback_query.data.split("_")[3]

    if callback_query.from_user.id != user_id:
        return await callback_query.answer("❌ 𝗡ã𝗼 𝗮𝘂𝘁𝗼𝗿𝗶𝘇𝗮𝗱𝗼.", show_alert=True)

    context_db[user_id]["model_id"] = model_id
    context_db[user_id]["model_name"] = model_name

    try:
        await callback_query.message.edit(
            text=f"🖼️ 𝗡𝘂𝗺𝗲𝗿𝗼 𝗱𝗲 𝗶𝗺𝗮𝗴𝗲𝗻𝘀",
            reply_markup=num_image_markup(user_id, model_id),
        )
    except Exception as e:
        logging.warning(e)
        await callback_query.answer(
            "❌ Ocorreu um erro. Tente novamente.", show_alert=True
        )
        await callback_query.message.delete()


def num_image_markup(user_id: int, model_id: int):
    buttons = [
        InlineKeyboardButton("1️⃣", callback_data=f"num_{user_id}_{model_id}_1"),
        InlineKeyboardButton("2️⃣", callback_data=f"num_{user_id}_{model_id}_2"),
        InlineKeyboardButton("3️⃣", callback_data=f"num_{user_id}_{model_id}_3"),
        InlineKeyboardButton("4️⃣", callback_data=f"num_{user_id}_{model_id}_4"),
    ]

    return InlineKeyboardMarkup([buttons[:2], buttons[2:]])


@app.on_callback_query(filters.regex(pattern=r"^num_\d+_\d+_\d+") & ~BANNED_USERS)
async def select_num_images(_: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.data.split("_")[1])
    model_id = int(callback_query.data.split("_")[2])
    num_images = int(callback_query.data.split("_")[3])

    query = await callback_query.message.edit(
        text=f"🦙 𝗠𝗼𝗱𝗲𝗹𝗼: {context_db[user_id]['model_name']}\n"
        f"🔢 𝗡𝘂𝗺𝗲𝗿𝗼 𝗱𝗲 𝗶𝗺𝗮𝗴𝗲𝗻𝘀: {num_images}\n"
        f"🏞️ 𝗣𝗿𝗼𝗰𝗲𝘀𝘀𝗮𝗻𝗱𝗼 𝗮 𝗶𝗺𝗮𝗴𝗲𝗺...",
        reply_markup=None,
    )

    if callback_query.from_user.id != user_id:
        return await callback_query.answer("❌ 𝗡𝗮̃𝗼 𝗮𝘂𝘁𝗼𝗿𝗶𝘇𝗮𝗱𝗼.", show_alert=True)

    context_db[user_id]["model_id"] = model_id
    context_db[user_id]["num_images"] = num_images

    payload = {
        "model_id": context_db[user_id]["model_id"],
        "prompt": context_db[user_id]["prompt"],
        "negative_prompt": context_db[user_id]["negative_prompt"],
        "num_images": context_db[user_id]["num_images"],
    }

    try:
        async with SessionAsyncClient() as client_async:
            request = await client_async.fetch(
                url=f"{client_async.url}/models/inference",
                method="POST",
                json=payload,
                headers={"content-type": "application/json"},
            )

            if request["code"] != 1:
                return await query.edit_text(
                    f"🦙 𝗠𝗼𝗱𝗲𝗹𝗼: {context_db[user_id]['model_name']}\n"
                    f"❌ 𝗔𝗹𝗴𝗼 𝗱𝗲𝘂 𝗲𝗿𝗿𝗼, 𝘁𝗲𝗻𝘁𝗲 𝗻𝗼𝘃𝗮𝗺𝗲𝗻𝘁𝗲 𝗺𝗮𝗶𝘀 𝘁𝗮𝗿𝗱𝗲."
                )

            task_id = request["task_id"]
            request_id = request["request_id"]

            img_urls = []
            images = []
            while True:
                response = await client_async.fetch(
                    url=f"{client_async.url}/models/inference/task",
                    method="POST",
                    json={"task_id": task_id, "request_id": request_id},
                    headers={"content-type": "application/json"},
                )

                print(response)
                if response.get("message") == "finished":
                    img_urls = response["img_urls"]
                    images = response["images"]
                    await client_async.close()
                    break

                await asyncio.sleep(5)
            if not img_urls:
                return await query.edit_text(
                    f"🦙 𝗠𝗼𝗱𝗲𝗹𝗼: {context_db[user_id]['model_name']}\n"
                    f"❌ 𝗔𝗹𝗴𝗼 𝗱𝗲𝘂 𝗲𝗿𝗿𝗼, 𝘁𝗲𝗻𝘁𝗲 𝗻𝗼𝘃𝗮𝗺𝗲𝗻𝘁𝗲 𝗺𝗮𝗶𝘀 𝘁𝗮𝗿𝗱𝗲."
                )

            await app.send_media_group(
                chat_id=callback_query.message.chat.id,
                media=[InputMediaPhoto(media=img) for img in img_urls],
                reply_to_message_id=context_db[user_id]["reply_to_id"],
            )
    except ValueError as e:
        logging.warning(f"ValueError: {e}")
        await query.edit_text("❌ 𝗢𝗰𝗼𝗿𝗿𝗲𝘂 𝗼𝗰𝗼𝗿𝗿𝗲𝘂 𝗮𝗼 𝗽𝗿𝗼𝗰𝗲𝘀𝘀𝗮𝗿 𝗮 𝘀𝗼𝗹𝗶𝗰𝗶𝘁𝗮çã𝗼.")
    except FloodWait as e:
        logging.warning(e)
        await asyncio.sleep(e.value)
    except Exception as e:
        logging.warning(f"Exception: {e}")
        await query.edit_text("❌ 𝗢𝗰𝗼𝗿𝗿𝗲𝘂 𝗼𝗰𝗼𝗿𝗿𝗲𝘂 𝗮𝗼 𝗽𝗿𝗼𝗰𝗲𝘀𝘀𝗮𝗿 𝗮 𝘀𝗼𝗹𝗶𝗰𝗶𝘁𝗮çã𝗼.")


@app.on_callback_query(filters.regex(pattern=r"^draw_cancel_\d+") & ~BANNED_USERS)
async def cancel_draw(_: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.data.split("_")[2])

    if callback_query.from_user.id != user_id:
        return await callback_query.answer("❌ 𝗡𝗮̃𝗼 𝗮𝘂𝘁𝗼𝗿𝗶𝘇𝗮𝗱𝗼.", show_alert=True)

    await callback_query.message.delete()

    try:
        await callback_query.message.reply_to_message.delete()
    except Exception as e:
        logging.warning(e)


def get_prompt(message: Message, prefixes: list[str]) -> None | tuple[str, str] | str:
    text = (
        message.text
        if len(message.text.split()) > 1
        else (message.reply_to_message.text if message.reply_to_message else None)
    )

    if not text:
        return None

    if text.startswith(tuple(prefixes)):
        text = text.split(maxsplit=1)[1]

    negatives = ["-", "--", "|", "||", "_", "—", "/"]
    for neg in negatives:
        if neg in text:
            prompt, negative_prompt = map(str.strip, text.split(neg, 1))
            return normalize_string(prompt), normalize_string(negative_prompt)

    return normalize_string(text), ""


class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other: InlineKeyboardButton):
        return self.text == other.text

    def __lt__(self, other: InlineKeyboardButton):
        return self.text < other.text

    def __gt__(self, other: InlineKeyboardButton):
        return self.text > other.text
