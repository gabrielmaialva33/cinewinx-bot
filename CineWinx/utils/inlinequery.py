from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

answer = []

answer.extend(
    [
        InlineQueryResultArticle(
            title="⏸️ 𝗣𝗮𝘂𝘀𝗮𝗿 𝘀𝘁𝗿𝗲𝗮𝗺",
            description="⏸️ 𝗣𝗮𝘂𝘀𝗮𝗿 𝗮 𝗺ú𝘀𝗶𝗰𝗮 𝗾𝘂𝗲 𝗲𝘀𝘁á 𝘁𝗼𝗰𝗮𝗻𝗱𝗼 𝗮𝘁𝘂𝗮𝗹𝗺𝗲𝗻𝘁𝗲 𝗻𝗼 𝘃𝗼𝗶𝗰𝗲𝗰𝗵𝗮𝘁.",
            thumb_url="https://telegra.ph/file/e553eb0c396d07dff08fe.png",
            input_message_content=InputTextMessageContent("/pause"),
        ),
        InlineQueryResultArticle(
            title="▶️ 𝗥𝗲𝘁𝗼𝗺𝗮𝗿 𝘀𝘁𝗿𝗲𝗮𝗺",
            description="▶️ 𝗥𝗲𝘁𝗼𝗺𝗮𝗿 𝗮 𝗺ú𝘀𝗶𝗰𝗮 𝗽𝗮𝘂𝘀𝗮𝗱𝗮 𝗻𝗼 𝘃𝗼𝗶𝗰𝗲𝗰𝗵𝗮𝘁.",
            thumb_url="https://telegra.ph/file/608698e132af480e04a04.png",
            input_message_content=InputTextMessageContent("/resume"),
        ),
        InlineQueryResultArticle(
            title="🔇 𝗠𝘂𝘁𝗮𝗿 𝘀𝘁𝗿𝗲𝗮𝗺",
            description="🔇 𝗠𝘂𝘁𝗮𝗿 𝗮 𝗺ú𝘀𝗶𝗰𝗮 𝗾𝘂𝗲 𝗲𝘀𝘁á 𝘁𝗼𝗰𝗮𝗻𝗱𝗼 𝗻𝗼 𝘃𝗼𝗶𝗰𝗲𝗰𝗵𝗮𝘁",
            thumb_url="https://telegra.ph/file/3cc6425258e6ba3594ae7.png",
            input_message_content=InputTextMessageContent("/vcmute"),
        ),
        InlineQueryResultArticle(
            title="🔊 𝗗𝗲𝘀𝗺𝘂𝘁𝗮𝗿 𝘀𝘁𝗿𝗲𝗮𝗺",
            description="🔊 𝗗𝗲𝘀𝗺𝘂𝘁𝗮𝗿 𝗮 𝗺ú𝘀𝗶𝗰𝗮 𝗾𝘂𝗲 𝗲𝘀𝘁á 𝘁𝗼𝗰𝗮𝗻𝗱𝗼 𝗻𝗼 𝘃𝗼𝗶𝗰𝗲𝗰𝗵𝗮𝘁",
            thumb_url="https://telegra.ph/file/25c54f307b2b2ee94dd70.png",
            input_message_content=InputTextMessageContent("/vcunmute"),
        ),
        InlineQueryResultArticle(
            title="⏭️ 𝗣𝘂𝗹𝗮𝗿 𝘀𝘁𝗿𝗲𝗮𝗺",
            description="⏭️ 𝗣𝘂𝗹𝗮𝗿 𝗽𝗮𝗿𝗮 𝗮 𝗽𝗿ó𝘅𝗶𝗺𝗮 𝗳𝗮𝗶𝘅𝗮. | 𝗣𝘂𝗹𝗮𝗿 𝗽𝗮𝗿𝗮 𝗮 𝗽𝗿ó𝘅𝗶𝗺𝗮 𝗳𝗮𝗶𝘅𝗮. | 𝗣𝗮𝗿𝗮 𝗳𝗮𝗶𝘅𝗮 𝗲𝘀𝗽𝗲𝗰𝗶́𝗳𝗶𝗰𝗮: /skip [número]",
            thumb_url="https://telegra.ph/file/cd09eef8a10036541f81b.png",
            input_message_content=InputTextMessageContent("/skip"),
        ),
        InlineQueryResultArticle(
            title="🛑 𝗘𝗻𝗰𝗲𝗿𝗿𝗮𝗿 𝘀𝘁𝗿𝗲𝗮𝗺",
            description="🛑 𝗣𝗮𝗿𝗮𝗿 𝗮 𝗺ú𝘀𝗶𝗰𝗮 𝗾𝘂𝗲 𝗲𝘀𝘁á 𝘁𝗼𝗰𝗮𝗻𝗱𝗼 𝗻𝗼 𝘃𝗼𝗶𝗰𝗲𝗰𝗵𝗮𝘁 𝗱𝗼 𝗴𝗿𝘂𝗽𝗼.",
            thumb_url="https://telegra.ph/file/25637e9dc40f742007f72.png",
            input_message_content=InputTextMessageContent("/stop"),
        ),
        InlineQueryResultArticle(
            title="🔀 𝗘𝗺𝗯𝗮𝗿𝗮𝗹𝗵𝗮𝗿 𝘀𝘁𝗿𝗲𝗮𝗺",
            description="🔀 𝗘𝗺𝗯𝗮𝗿𝗮𝗹𝗵𝗮𝗿 𝗮 𝗹𝗶𝘀𝘁𝗮 𝗱𝗲 𝗳𝗮𝗶𝘅𝗮𝘀 𝗻𝗮 𝗳𝗶𝗹𝗮.",
            thumb_url="https://telegra.ph/file/0e2f59db19f95ac8139f8.png",
            input_message_content=InputTextMessageContent("/shuffle"),
        ),
        InlineQueryResultArticle(
            title="⏩ 𝗔𝘃𝗮𝗻ç𝗮𝗿 𝘀𝘁𝗿𝗲𝗮𝗺",
            description="⏩ 𝗔𝘃𝗮𝗻ç𝗮𝗿 𝗻𝗮 𝘀𝘁𝗿𝗲𝗮𝗺 𝗮𝘁𝘂𝗮𝗹 𝗽𝗮𝗿𝗮 𝘂𝗺𝗮 𝗱𝘂𝗿𝗮𝗰̧𝗮̃𝗼 𝗲𝘀𝗽𝗲𝗰𝗶́𝗳𝗶𝗰𝗮.",
            thumb_url="https://telegra.ph/file/284d37d548f3c9745cc6c.png",
            input_message_content=InputTextMessageContent("/seek 10"),
        ),
        InlineQueryResultArticle(
            title="🔁 𝗟𝗼𝗼𝗽 𝘀𝘁𝗿𝗲𝗮𝗺",
            description="🔁 𝗥𝗲𝗽𝗲𝘁𝗶𝗿 𝗮 𝗺ú𝘀𝗶𝗰𝗮 𝗾𝘂𝗲 𝗲𝘀𝘁á 𝘁𝗼𝗰𝗮𝗻𝗱𝗼 𝗮𝘁𝘂𝗮𝗹𝗺𝗲𝗻𝘁𝗲. 𝗨𝘀𝗼: /loop [enable|disable]",
            thumb_url="https://telegra.ph/file/cd9f87e0955c453201a5b.png",
            input_message_content=InputTextMessageContent("/loop 3"),
        ),
    ]
)
