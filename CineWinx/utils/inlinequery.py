from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

answer = []

answer.extend(
    [
        InlineQueryResultArticle(
            title="pausar stream",
            description="pausar a música que está tocando atualmente no voicechat.",
            thumb_url="https://telegra.ph/file/e553eb0c396d07dff08fe.png",
            input_message_content=InputTextMessageContent("/pause"),
        ),
        InlineQueryResultArticle(
            title="retomar stream",
            description="retomar a música pausada no voicechat.",
            thumb_url="https://telegra.ph/file/608698e132af480e04a04.png",
            input_message_content=InputTextMessageContent("/resume"),
        ),
        InlineQueryResultArticle(
            title="mutar stream",
            description="mutar a música que está tocando no voicechat",
            thumb_url="https://telegra.ph/file/3cc6425258e6ba3594ae7.png",
            input_message_content=InputTextMessageContent("/vcmute"),
        ),
        InlineQueryResultArticle(
            title="desmutar stream",
            description="desmutar a música que está tocando no voicechat",
            thumb_url="https://telegra.ph/file/25c54f307b2b2ee94dd70.png",
            input_message_content=InputTextMessageContent("/vcunmute"),
        ),
        InlineQueryResultArticle(
            title="pular stream",
            description="pular para a próxima faixa. | pular para a próxima faixa. | para faixa específica: /skip ["
            "número]",
            thumb_url="https://telegra.ph/file/cd09eef8a10036541f81b.png",
            input_message_content=InputTextMessageContent("/skip"),
        ),
        InlineQueryResultArticle(
            title="encerrar stream",
            description="parar a música que está tocando no voicechat do grupo.",
            thumb_url="https://telegra.ph/file/25637e9dc40f742007f72.png",
            input_message_content=InputTextMessageContent("/stop"),
        ),
        InlineQueryResultArticle(
            title="embaralhar stream",
            description="embaralhar a lista de faixas na fila.",
            thumb_url="https://telegra.ph/file/0e2f59db19f95ac8139f8.png",
            input_message_content=InputTextMessageContent("/shuffle"),
        ),
        InlineQueryResultArticle(
            title="avançar stream",
            description="avançar na stream atual para uma duração específica.",
            thumb_url="https://telegra.ph/file/284d37d548f3c9745cc6c.png",
            input_message_content=InputTextMessageContent("/seek 10"),
        ),
        InlineQueryResultArticle(
            title="loop stream",
            description="repetir a música que está tocando atualmente. uso: /loop [enable|disable]",
            thumb_url="https://telegra.ph/file/cd9f87e0955c453201a5b.png",
            input_message_content=InputTextMessageContent("/loop 3"),
        ),
    ]
)
