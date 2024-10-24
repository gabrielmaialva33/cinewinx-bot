import logging

from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultPhoto,
    CallbackQuery,
)
from youtubesearchpython.__future__ import VideosSearch

from CineWinx import app
from CineWinx.utils.inlinequery import answer, sources
from config import BANNED_USERS


@app.on_inline_query(~BANNED_USERS)
async def inline_query_handler(client: app, callback: CallbackQuery):
    text = callback.query.strip().lower()
    answers = []
    if text.strip() == "":
        try:
            inline = await client.answer_inline_query(
                callback.id, results=sources, cache_time=10
            )
            response = await answer(callback)
            if response:
                return response
            return inline

        except Exception as e:
            logging.error(str(e))
            return
    else:
        a = VideosSearch(text, limit=20)
        result = (await a.next()).get("result")
        for x in range(15):
            title = (result[x]["title"]).title()
            duration = result[x]["duration"]
            views = result[x]["viewCount"]["short"]
            thumbnail = result[x]["thumbnails"][0]["url"].split("?")[0]
            channellink = result[x]["channel"]["link"]
            channel = result[x]["channel"]["name"]
            link = result[x]["link"]
            published = result[x]["publishedTime"]
            description = f"{views} | {duration} Mins | {channel}  | {published}"
            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🎥 Ver no YouTube",
                            url=link,
                        )
                    ],
                ]
            )
            searched_text = f"""
❇️<b>Título:</b> [{title}]({link})

⏳<b>Duração:</b> {duration} minutos
👀<b>Visualizações:</b> {views}
⏰<b>Publicado em:</b> {published}
🎥<b>Nome do Canal:</b> {channel}
📎<b>Link do Canal:</b> <a href="{channellink}">veja aqui</a>

<i>Responda com <code>/play</code> nesta mensagem pesquisada para transmitir no chat de voz.</i>

⚡️ <b>Pesquisa inline por {app.mention} </b>"""
            answers.append(
                InlineQueryResultPhoto(
                    photo_url=thumbnail,
                    title=title,
                    thumb_url=thumbnail,
                    description=description,
                    caption=searched_text,
                    reply_markup=buttons,
                )
            )
        try:
            return await client.answer_inline_query(callback.id, results=answers)
        except Exception as e:
            logging.error(str(e))
            return
