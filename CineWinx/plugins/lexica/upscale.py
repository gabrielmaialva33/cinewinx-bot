import logging
from math import ceil
import os

import asyncio
from pyrogram import filters, Client
from pyrogram.errors import FloodWait
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegraph.aio import Telegraph

from CineWinx import app
from CineWinx.utils import SessionAsyncClient
from config import PREFIXES, BANNED_USERS, LX_UPS_MODELS
from strings import get_command

import telegraph

UPSCALE_COMMAND = get_command("UPSCALE_COMMAND")

context_db: dict = {}


@app.on_message(filters.command(UPSCALE_COMMAND, PREFIXES) & ~BANNED_USERS)
async def upscale_command(_: Client, message: Message):
    file = await get_file(message)
    if file is None:
        return await message.reply_text(
            "💬 𝗿𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗮 𝘂𝗺𝗮 𝗶𝗺𝗮𝗴𝗲𝗺 𝗽𝗮𝗿𝗮 𝗮𝘂𝗺𝗲𝗻𝘁𝗮𝗿 𝗮 𝗲𝘀𝗰𝗮𝗹𝗮 ✨"
        )

    context_db[message.from_user.id] = {
        "model_id": None,
        "model_name": None,
        "reply_to_id": message.id,
        "file": file,
    }

    markup = upscale_models_markup(message.from_user.id, LX_UPS_MODELS)

    await message.reply_text(
        "💬 𝗲𝗰𝗼𝗹𝗵𝗮 𝘂𝗺 𝗺𝗼𝗱𝗲𝗹𝗼 ✨",
        reply_markup=markup,
    )


def upscale_models_markup(user_id: int, models: list | dict, page: int = 0) -> InlineKeyboardMarkup:
    models = sorted(
        [
            InlineKeyboardButton(
                model["name"],
                callback_data=f"ups_{user_id}_{model['id']}_{model['name']}",
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
                    "❌ 𝗖𝗮𝗻𝗰𝗲𝗹𝗮𝗿", callback_data=f"ups_cancel_{user_id}"
                )
            ]
        ]

    return InlineKeyboardMarkup(pairs)


@app.on_callback_query(filters.regex(pattern=r"^ups_(prev|next)_\d+") & ~BANNED_USERS)
async def paginate_models(_: Client, callback_query: CallbackQuery):
    try:
        data = callback_query.data.split("_")
        page = int(data[2])

        if data[1] == "prev":
            page -= 1
        elif data[1] == "next":
            page += 1

        markup = upscale_models_markup(callback_query.from_user.id, LX_UPS_MODELS, page)

        await callback_query.edit_message_reply_markup(markup)
    except FloodWait as e:
        logging.warning(e)
        await asyncio.sleep(e.value)
    except Exception as e:
        logging.warning(e)


@app.on_callback_query(filters.regex(pattern=r"^ups_\d+_\d+_\w+") & ~BANNED_USERS)
async def select_model(_: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.data.split("_")[1])
    model_id = int(callback_query.data.split("_")[2])
    model_name = callback_query.data.split("_")[3]

    context_db[user_id]["model_id"] = model_id
    context_db[user_id]["model_name"] = model_name

    file = context_db[user_id]["file"]

    call = await callback_query.message.edit("⏳ 𝗮𝗺𝗽𝗹𝗶𝗮𝗻𝗱𝗼 𝗮 𝗶𝗺𝗮𝗴𝗲𝗺 ... ✨", reply_markup=None)
    try:
        with open(file, "rb") as image_file:
            image_bytes = image_file.read()

        upscaled_image = await upscale_image(model_id, image_bytes)
        graph = Telegraph()
        upload_path = await graph.upload_file(upscaled_image)

        with open(upscaled_image, "rb") as upscaled_file:
            await callback_query.message.reply_photo(
                photo=upscaled_file,
                caption=f"🖼️ 𝗠𝗼𝗱𝗲𝗹𝗼: {model_name}\n🌉️ 𝗔𝗺𝗽𝗹𝗶𝗮𝗱𝗼 𝗰𝗼𝗺 𝘀𝘂𝗰𝗲𝘀𝘀𝗼! ⬆️",
                reply_to_message_id=context_db[user_id]["reply_to_id"],
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "🔗 𝗟𝗶𝗻𝗸 𝗻𝗼 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗽𝗵",
                                url=f"https://telegra.ph{upload_path[0]['src']}",
                            )
                        ]
                    ]
                ),
            )

        await call.delete()
    except Exception as e:
        logging.error(str(e))
        await call.edit_text(f"🖼️ 𝗠𝗼𝗱𝗲𝗹𝗼: {model_name}\n❌ 𝗲𝗿𝗿𝗼 𝗮𝗼 𝗮𝗺𝗽𝗹𝗶𝗮𝗿 𝗮 𝗶𝗺𝗮𝗴𝗲𝗺 😕", reply_markup=None)


@app.on_callback_query(filters.regex(pattern=r"^ups_cancel_\d+") & ~BANNED_USERS)
async def cancel_upscale(_: Client, callback_query: CallbackQuery):
    user_id = int(callback_query.data.split("_")[2])

    await callback_query.message.edit("❌ 𝗮𝗺𝗽𝗹𝗶𝗮𝗰̧𝗮̃𝗼 𝗰𝗮𝗻𝗰𝗲𝗹𝗮𝗱𝗮 🚫", reply_markup=None)

    if os.path.exists(context_db[user_id]["file"]):
        os.remove(context_db[user_id]["file"])

    del context_db[user_id]


async def get_file(message):
    if not message.reply_to_message:
        return None
    if (
            message.reply_to_message.document is False
            or message.reply_to_message.photo is False
    ):
        return None
    if (
            message.reply_to_message.document
            and message.reply_to_message.document.mime_type
            in ["image/png", "image/jpg", "image/jpeg"]
            or message.reply_to_message.photo
    ):
        image = await message.reply_to_message.download()
        return image
    else:
        return None


async def upscale_image(model_id: int, image: bytes) -> str:
    try:
        async with SessionAsyncClient() as client_async:
            response = await client_async.upscale(model_id, image)
            upscaled_file_path = "cache/upscaled.png"
            with open(upscaled_file_path, "wb") as output_file:
                output_file.write(response)
            return upscaled_file_path
    except Exception as e:
        logging.error(str(e))
    finally:
        await client_async.close()


__MODULE__ = "🌉 𝗨𝗽𝘀𝗰𝗮𝗹𝗲"
__HELP__ = """
🛠️ 𝗠𝗼́𝗱𝘂𝗹𝗼 𝗱𝗲 𝗨𝗽𝘀𝗰𝗮𝗹𝗲

<b>📝 𝗗𝗲𝘀𝗰𝗿𝗶𝗰̧𝗮̃𝗼:</b>

𝗘𝘀𝘁𝗲 𝗺𝗼́𝗱𝘂𝗹𝗼 𝗽𝗮𝗿𝗮 𝗮𝗺𝗽𝗹𝗶𝗮𝗿 𝗮 𝗲𝘀𝗰𝗮𝗹𝗮 𝗱𝗲 𝗶𝗺𝗮𝗴𝗲𝗺 𝗻𝗼 𝗧𝗲𝗹𝗲𝗴𝗿𝗮𝗽𝗵.

<b>🔖 𝗖𝗼𝗺𝗮𝗻𝗱𝗼:</b>

• <code>/upscale:</code> 𝗔𝗺𝗽𝗹𝗶𝗮𝗿 𝗮 𝗲𝘀𝗰𝗮𝗹𝗮 𝗱𝗲 𝗶𝗺𝗮𝗴𝗲𝗺 𝗽𝗮𝗿𝗮 𝗮𝘂𝗺𝗲𝗻𝘁𝗮𝗿 𝗮 𝗲𝘀𝗰𝗮𝗹𝗮 𝗱𝗲 𝗮𝗺𝗽𝗹𝗶𝗮𝗰̧𝗮̃𝗼.

"""
