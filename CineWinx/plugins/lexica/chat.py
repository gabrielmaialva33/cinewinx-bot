import re
import unicodedata

from pyrogram import filters, Client
from pyrogram.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)

from CineWinx import app
from CineWinx.utils import LexicaClient
from config import PREFIXES, BANNED_USERS
from strings import get_command

LLM_COMMAND = get_command("LLM_COMMAND")

prompt_db: dict = {}

client = LexicaClient()

main_prompt = (
    "Você é a AI do CineWinx. Ao responder, por favor, chame o usuário pelo nome. {0}\n\n"
    "A seguir está o prompt que um usuário enviou para você:\n\n{1}"
)


@app.on_message(filters.command(LLM_COMMAND, PREFIXES) & ~BANNED_USERS)
async def llm(_client: Client, message: Message):
    prompt = (
        message.text.split(None, 1)[1].strip()
        if len(message.text.split()) > 1
        else (message.reply_to_message.text if message.reply_to_message else None)
    )
    reply_to_id = (
        message.reply_to_message.id if message.reply_to_message else message.id
    )

    user_name = message.from_user.first_name
    user_name = normalize_username(user_name)
    if user_name == "":
        user_name = "User"

    prompt_db[message.from_user.id] = {
        "prompt": prompt,
        "reply_to_id": reply_to_id,
        "user_name": user_name,
        "model_id": None,
        "model_name": None,
    }

    models = client.get_chats_model()

    page = 0
    markup = chat_markup(message.from_user.id, models, page)

    await message.reply_text(
        f"🦙 𝗦𝗲𝗹𝗲𝗰𝗶𝗼𝗻𝗲 𝘂𝗺 𝗺𝗼𝗱𝗲𝗹𝗼 𝗟𝗟𝗠 👇",
        reply_markup=markup,
    )


def chat_markup(
    user_id: int, models: list | dict, page: int = 0
) -> InlineKeyboardMarkup:
    # number of models per page
    models_per_page = 4
    start_index = page * models_per_page
    end_index = start_index + models_per_page

    # select models for the current page
    current_models = models[start_index:end_index]

    # create buttons for models
    buttons = []
    for model in current_models:
        buttons.append(
            InlineKeyboardButton(
                text=model["name"],
                callback_data=f"llm_{user_id}_{model['id']}_{model['name']}",
            )
        )

    # organize buttons in 2x2 grid
    keyboard = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]

    # add navigation buttons
    navigation_buttons = []
    if start_index > 0:
        navigation_buttons.append(
            InlineKeyboardButton(text="⬅️ 𝗔𝗻𝘁𝗲𝗿𝗶𝗼𝗿", callback_data=f"llm_prev_{page}")
        )
    if end_index < len(models):
        navigation_buttons.append(
            InlineKeyboardButton(text="➡️ 𝗣𝗿𝗼́𝘅𝗶𝗺𝗼", callback_data=f"llm_next_{page}")
        )

    if navigation_buttons:
        keyboard.append(navigation_buttons)

    return InlineKeyboardMarkup(keyboard)


@app.on_callback_query(filters.regex(pattern=r"^llm_(prev|next)_\d+"))
async def paginate_models(_, callback_query: CallbackQuery):
    models = client.get_chats_model()
    data = callback_query.data.split("_")
    page = int(data[2])

    if data[1] == "prev":
        page -= 1
    elif data[1] == "next":
        page += 1

    markup = chat_markup(callback_query.from_user.id, models, page)

    await callback_query.edit_message_reply_markup(markup)


@app.on_callback_query(filters.regex(pattern=r"^llm_\d+_\d+_\w+") & ~BANNED_USERS)
async def select_model(_, callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id

    user_id = int(callback_query.data.split("_")[1])
    model_id = int(callback_query.data.split("_")[2])
    model_name = callback_query.data.split("_")[3]

    # check if the user is the same as the one who initiated the command
    if callback_query.from_user.id != user_id:
        return await callback_query.answer("❌ 𝗡ã𝗼 𝗮𝘂𝘁𝗼𝗿𝗶𝘇𝗮𝗱𝗼.", show_alert=True)

    prompt_db[user_id]["model_id"] = model_id
    prompt_db[user_id]["model_name"] = model_name

    prompt = main_prompt.format(
        prompt_db[user_id]["user_name"], prompt_db[user_id]["prompt"]
    )
    params = {
        "prompt": prompt,
        "model_id": prompt_db[user_id]["model_id"],
    }

    response = client.fetch(
        url=f"{client.url}/models",
        method="POST",
        params=params,
        json={},
        headers={"content-type": "application/json"},
    )

    if response["code"] != 2:
        return await callback_query.edit_message_text(
            f"🦙 𝗠𝗼𝗱𝗲𝗹𝗼: {prompt_db[user_id]['model_name']}\n"
            f"❌ 𝗔𝗹𝗴𝗼 𝗱𝗲𝘂 𝗲𝗿𝗿𝗼, 𝘁𝗲𝗻𝘁𝗲 𝗻𝗼𝘃𝗮𝗺𝗲𝗻𝘁𝗲 𝗺𝗮𝗶𝘀 𝘁𝗮𝗿𝗱𝗲."
        )

    await callback_query.message.delete()
    await callback_query.message.reply_to_message.reply_text(
        f"📝 <u>𝗣𝗿𝗼𝗺𝗽𝘁</u>: {prompt_db[user_id]['prompt']}"
        f"\n🦙 <u>𝗠𝗼𝗱𝗲𝗹𝗼</u>: {prompt_db[user_id]['model_name']}"
        f"\n📬 <u>𝗥𝗲𝘀𝗽𝗼𝘀𝘁𝗮</u>: \n\n"
        f"<i>{response['content']}</i>",
        reply_to_message_id=prompt_db[user_id]["reply_to_id"],
    )


def normalize_username(username: str) -> str:
    normalized = unicodedata.normalize("NFKC", username)
    normalized = re.sub(r"\W+", "", normalized)
    return normalized


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
