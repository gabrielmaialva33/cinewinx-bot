import string
from typing import Dict

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

RESULTS_PER_PAGE = 5

context_db: Dict[int, Dict] = {}


class ContextManager:
    """Handles storing and retrieving user-specific context."""

    def __init__(self, user_id: int):
        self.user_id = user_id

    def get_context(self) -> Dict:
        return context_db.get(self.user_id, {})

    def update_context(self, **kwargs):
        context = self.get_context()
        context.update(kwargs)
        context_db[self.user_id] = context

    def reset_context(self):
        context_db.pop(self.user_id, None)


@app.on_message(filters.command("test", PREFIXES) & ~BANNED_USERS)
async def search_movies(_client: Client, message: Message):
    query = (
        message.text.split(None, 1)[1].strip()
        if len(message.text.split()) > 1
        else (message.reply_to_message.text if message.reply_to_message else None)
    )

    print("query:", query)

    context_manager = ContextManager(message.from_user.id)
    context_manager.update_context(query=query, page_token=None, page_index=0)

    if not query:
        # await message.reply_text(
        #     "🎬 𝗘𝗻𝗰𝗼𝗻𝘁𝗿𝗲 𝗽𝗼𝗿 𝗹𝗲𝘁𝗿𝗮 𝗼𝘂 𝗻𝘂𝗺é𝗿𝗼:",
        #     reply_markup=years_markup(),
        # )
        result = await AnimiZeY.movie_foder()

        print("result.data.files", result["data"]["files"])
        # result.data.files [{'kind': 'drive#file', 'name': '2023', 'modifiedTime': '2024-03-19T00:47:47.260Z', 'id': '1a9rD/kY+aJG5AQLzXGT57PhSPopwzpsWBr1gyLaIxhnIJQv3yhKTm/MQ0GRSPzg', 'driveId': 'ZqmmsCRkY8O3DfKFgBZzXuWNTtM6aBVpjCWGRoUri2g=', 'mimeType': 'application/vnd.google-apps.folder', 'link': None}, {'kind': 'drive#file', 'name': '2024', 'modifiedTime': '2024-03-18T23:19:50.903Z', 'id': 'o8/xKVxKdp4fTOshjeHdpOW0ZAmneBFF8jKPpTONhPnBaBfVyCkFm6jiRbq/7Ls/', 'driveId': 'ZqmmsCRkY8O3DfKFgBZzXuWNTtM6aBVpjCWGRoUri2g=', 'mimeType': 'application/vnd.google-apps.folder', 'link': None}, {'kind': 'drive#file', 'name': 'Filmes (5519)', 'modifiedTime': '2023-09-15T23:19:47.145Z', 'id': 'nrVmhX+bhjFC6S3nko8tDN816WtcieSOagbzdC693ic1Gk07YsefJ9gR0/VQvx3n', 'driveId': 'ZqmmsCRkY8O3DfKFgBZzXuWNTtM6aBVpjCWGRoUri2g=', 'mimeType': 'application/vnd.google-apps.folder', 'link': None}, {'kind': 'drive#file', 'name': 'Filmes 4k (227)', 'modifiedTime': '2023-09-15T23:19:51.773Z', 'id': 'YPD/B7EgqagjGLrZheKatOK3Uo280ChWxoeZhno7JFQO32NSPWqh9rIwrtNA6x08', 'driveId': 'ZqmmsCRkY8O3DfKFgBZzXuWNTtM6aBVpjCWGRoUri2g=', 'mimeType': 'application/vnd.google-apps.folder', 'link': None}, {'kind': 'drive#file', 'name': 'Filmes Animação (1019)', 'modifiedTime': '2023-09-15T23:19:55.468Z', 'id': 'V4Fa2bGvjprsnRVei+4yuLmBCr5UkwvQOepBRmMls2F9CZ9B+k02uhBD28F0ybp4', 'driveId': 'ZqmmsCRkY8O3DfKFgBZzXuWNTtM6aBVpjCWGRoUri2g=', 'mimeType': 'application/vnd.google-apps.folder', 'link': None}, {'kind': 'drive#file', 'name': 'Filmes Antigos (4054)', 'modifiedTime': '2023-09-15T23:19:57.941Z', 'id': 'D2tpz2aHSJneHeXtzupZs7QUpstUEfkkD6Kh+XgdUH/llNsiRIZaEDRr+8HWIubD', 'driveId': 'ZqmmsCRkY8O3DfKFgBZzXuWNTtM6aBVpjCWGRoUri2g=', 'mimeType': 'application/vnd.google-apps.folder', 'link': None}, {'kind': 'drive#file', 'name': 'Filmes Decênio (2735)', 'modifiedTime': '2023-09-15T23:20:00.437Z', 'id': 'KKVw5qLcqd0al3qb4O01CBdhsYJO6X1YBQNE+LZ/WFXpFTiCpsaF9PmuJPqDBAoZ', 'driveId': 'ZqmmsCRkY8O3DfKFgBZzXuWNTtM6aBVpjCWGRoUri2g=', 'mimeType': 'application/vnd.google-apps.folder', 'link': None}, {'kind': 'drive#file', 'name': 'Filmes orezraey', 'modifiedTime': '2024-02-27T03:01:25.209Z', 'id': '6o+WxdaGN4MWQ9gGYaWhJiSls2swFGuDe2x11Jn4sdn3xHMo50u4tsPzQ5KLGMRt', 'driveId': 'ZqmmsCRkY8O3DfKFgBZzXuWNTtM6aBVpjCWGRoUri2g=', 'mimeType': 'application/vnd.google-apps.folder', 'link': None}, {'kind': 'drive#file', 'name': 'Filmes recentes (2599)', 'modifiedTime': '2023-09-15T23:20:14.517Z', 'id': 'x7180AWUl+I5/cEig1eAyoD4leCyXvUp66xi0uwYH/nkkAMVVXMtsdZR+0J0DkQF', 'driveId': 'ZqmmsCRkY8O3DfKFgBZzXuWNTtM6aBVpjCWGRoUri2g=', 'mimeType': 'application/vnd.google-apps.folder', 'link': None}]

        folders = [
            file
            for file in result["data"]["files"]
            if file["mimeType"] == "application/vnd.google-apps.folder"
        ]

        print("folders", folders)

        markup = folder_markup(folders)

        await message.reply_text("🎬 𝗘𝗻𝗰𝗼𝗻𝘁𝗿𝗲 𝗽𝗼𝗿 𝗳𝗼𝗹𝗱𝗲𝗿:", reply_markup=markup)
    else:
        result = await AnimiZeY.search_movie(query, None)

        print("result.data.files", result["data"]["files"])

        folders = [
            file
            for file in result["data"]["files"]
            if file["mimeType"] == "application/vnd.google-apps.folder"
        ]

        print("folders", folders)


        context_manager.update_context(
            query=query, page_token=result["data"]["nextPageToken"], page_index=0, files=result["data"]["files"]
        )

        await send_results_page(message, message.from_user.id)

def folder_markup(folders: list, page: int = 0) -> InlineKeyboardMarkup:
    """
    Create a list of buttons for the alphabet
    """
    buttons = [
        InlineKeyboardButton(folder["name"], callback_data=f"folder_{folder['id']}")
        for folder in folders
    ]
    pairs = list(zip(buttons[::2], buttons[1::2]))

    if len(buttons) % 2 != 0:
        pairs.append((buttons[-1],))

    column_size = 3
    max_num_pages = ceil(len(pairs) / column_size)
    m_page = page % max_num_pages

    if len(buttons) > column_size:
        pairs = pairs[m_page * column_size : column_size * (m_page + 1)] + [
            (
                InlineKeyboardButton("⬅️", callback_data=f"folder_prev_{m_page}"),
                InlineKeyboardButton("❌ 𝗙𝗲𝗰𝗵𝗮𝗿", callback_data="folder_cancel"),
                InlineKeyboardButton("➡️", callback_data=f"folder_next_{m_page}"),
            )
        ]
    else:
        pairs += [[InlineKeyboardButton("❌ 𝗙𝗲𝗰𝗵𝗮𝗿", callback_data="folder_cancel")]]

    return InlineKeyboardMarkup(pairs)


def alpha_markup(page: int = 0) -> InlineKeyboardMarkup:
    """
    Create a list of buttons for the alphabet
    """
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


def years_markup(page: int = 27) -> InlineKeyboardMarkup:
    """
    Create a list of buttons for years from 1900 to 2023
    """
    buttons = [
        InlineKeyboardButton(str(year), callback_data=f"year_{year}")
        for year in range(1900, 2025)
    ]
    pairs = list(zip(buttons[::3], buttons[1::3], buttons[2::3]))

    if len(buttons) % 3 != 0:
        pairs.append((buttons[-1],))

    column_size = 3
    max_num_pages = ceil(len(pairs) / column_size)
    m_page = page % max_num_pages

    if len(pairs) > column_size:
        pairs = pairs[m_page * column_size : column_size * (m_page + 1)] + [
            (
                InlineKeyboardButton("⬅️", callback_data=f"year_prev_{m_page}"),
                InlineKeyboardButton("❌ 𝗙𝗲𝗰𝗵𝗮𝗿", callback_data="year_cancel"),
                InlineKeyboardButton("➡️", callback_data=f"year_next_{m_page}"),
            )
        ]
    else:
        pairs += [[InlineKeyboardButton("❌ 𝗙𝗲𝗰𝗵𝗮𝗿", callback_data="year_cancel")]]

    return InlineKeyboardMarkup(pairs)


@app.on_callback_query(filters.regex(r"^alpha_[A-Z]$"))
async def alpha(_client: Client, callback_query: CallbackQuery):
    data = callback_query.data.split("_")
    print("callback_query.alpha_", data)
    letter = data[1]

    await callback_query.message.delete()

    context_db[callback_query.from_user.id] = {
        "query": letter,
        "page_token": None,
        "page_index": 0,
    }

    context = context_db[callback_query.from_user.id]

    results = await AnimiZeY.search_movie(context["query"], context["page_token"])
    if not results:
        await callback_query.message.reply_text("🎬 𝗡𝗲𝗻𝗵𝘂𝗺 𝗿𝗲𝘀𝘂𝗹𝘁𝗮𝗱𝗼.")
        return

    context["page_token"] = results["data"]["nextPageToken"]
    context["files"] = [
        file
        for file in results["data"]["files"]
        if file["mimeType"] == "video/x-matroska"
    ]

    # print keys in files
    for key in results["data"]["files"]:
        print(key)

    await send_results_page(callback_query.message, callback_query.from_user.id)


@app.on_callback_query(filters.regex(r"^year_\d{4}$"))
async def years(_client: Client, callback_query: CallbackQuery):
    data = callback_query.data.split("_")
    year = data[1]

    await callback_query.message.delete()

    context_db[callback_query.from_user.id] = {
        "query": year,
        "page_token": None,
        "page_index": 0,
    }

    context = context_db[callback_query.from_user.id]

    results = await AnimiZeY.search_movie(context["query"], context["page_token"])
    print("results", results["data"])
    if not results:
        await callback_query.message.reply_text("🎬 𝗡𝗲𝗻𝗵𝘂𝗺 𝗿𝗲𝘀𝘂𝗹𝘁𝗮𝗱𝗼.")
        return

    context["page_token"] = (
        results["data"]["nextPageToken"] if "nextPageToken" in results["data"] else None
    )
    context["files"] = results["data"]["files"]

    await send_results_page(callback_query.message, callback_query.from_user.id)


@app.on_callback_query
async def send_results_page(message: Message, user_id: int):
    context = context_db[user_id]
    files = context["files"]

    page_index = context["page_index"]
    total_pages = ceil(len(files) / RESULTS_PER_PAGE)

    start = page_index * RESULTS_PER_PAGE
    end = start + RESULTS_PER_PAGE
    files_on_page = files[start:end]

    text = "🎥 <b>Filmes encontrados:</b>\n\n"
    for file in files_on_page:
        name = file.get("name", "<b>Sem título</b>")
        type = file.get("mimeType", None)
        link = file.get("link", "#")
        text += f"📽️ <a href='{AnimiZeY.base_url + link}'>{name}</a>\n"

    markup = InlineKeyboardMarkup(
        [
            [
                (
                    InlineKeyboardButton("⬅️", callback_data="prev_page")
                    if page_index > 0
                    else None
                ),
                (
                    InlineKeyboardButton("➡️", callback_data="next_page")
                    if page_index < total_pages - 1
                    else None
                ),
            ],
            [InlineKeyboardButton("❌", callback_data="alpha_cancel")],
        ]
    )

    markup.inline_keyboard = [list(filter(None, row)) for row in markup.inline_keyboard]

    await message.reply_text(text, reply_markup=markup)


@app.on_callback_query(filters.regex(r"^(prev|next)_page$"))
async def paginate_results(_client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    action = callback_query.data.split("_")[0]

    context = context_db[user_id]

    if action == "prev":
        context["page_index"] -= 1
    elif action == "next":
        context["page_index"] += 1

    await callback_query.message.delete()
    await send_results_page(callback_query.message, user_id)


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


@app.on_callback_query(filters.regex(r"^year_(prev|next)_\d+$"))
async def paginate_years(_client: Client, callback_query: CallbackQuery):
    data = callback_query.data.split("_")
    page = int(data[2])

    if data[1] == "prev":
        page -= 1
    elif data[1] == "next":
        page += 1

    markup = years_markup(page)
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
