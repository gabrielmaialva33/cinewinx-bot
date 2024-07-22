from gpytranslate import Translator
from pyrogram import filters
from pyrogram.types import Message

from CineWinx import app
from config import BANNED_USERS

trans = Translator()


@app.on_message(filters.command("tr") & ~BANNED_USERS)
async def translate(_, message: Message) -> None:
    reply_msg = message.reply_to_message
    if not reply_msg:
        await message.reply_text(
            "𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗿𝗲𝘀𝗽𝗼𝗻𝗱𝗮 𝗮 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗽𝗮𝗿𝗮 𝘁𝗿𝗮𝗱𝘂𝘇𝗶-𝗹𝗮! 🌐"
        )
        return
    if reply_msg.caption:
        to_translate = reply_msg.caption
    elif reply_msg.text:
        to_translate = reply_msg.text
    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source = args.split("//")[0]
            dest = args.split("//")[1]
        else:
            source = await trans.detect(to_translate)
            dest = args
    except IndexError:
        source = await trans.detect(to_translate)
        dest = "pt"
    translation = await trans(to_translate, sourcelang=source, targetlang=dest)
    reply = f"𝗧𝗿𝗮𝗱𝘂𝘇𝗶𝗱𝗼 𝗱𝗲 {source} 𝗽𝗮𝗿𝗮 {dest}:\n\n{translation.text}"
    await message.reply_text(reply)


@app.on_message(filters.command("langcodes") & ~BANNED_USERS)
async def language_codes(_, message):
    languages = """
    🗣️ 𝗖𝗼́𝗱𝗶𝗴𝗼𝘀 𝗱𝗲 𝗜𝗱𝗶𝗼𝗺𝗮:
    en - Inglês
    es - Espanhol
    fr - Francês
    de - Alemão
    it - Italiano
    pt - Português
    ru - Russo
    zh - Chinês
    ar - Árabe
    ja - Japonês
    ko - Coreano
    hi - Hindi
    """
    await message.reply_text(languages)


__MODULE__ = "🌐 𝗧𝗿𝗮𝗱𝘂𝘁𝗼𝗿"
__HELP__ = """
𝗘𝘀𝘁𝗲 𝗺𝗼́𝗱𝘂𝗹𝗼 𝗽𝗿𝗼𝘃𝗲 𝗰𝗼𝗺𝗮𝗻𝗱𝗼𝘀 𝗽𝗮𝗿𝗮 𝘁𝗿𝗮𝗱𝘂𝘇𝗶𝗿 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗻𝘀.

- <code>/tr [código_do_idioma]</code>: 𝗧𝗿𝗮𝗱𝘂𝘇𝗮 𝘂𝗺𝗮 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺. 𝗥𝗲𝘀𝗽𝗼𝗻𝗱𝗮 à 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗺 𝗾𝘂𝗲 𝘃𝗼𝗰𝗲̂ 𝗱𝗲𝘀𝗲𝗷𝗮 𝘁𝗿𝗮𝗱𝘂𝘇𝗶𝗿. 𝗢𝗽𝗰𝗶𝗼𝗻𝗮𝗹𝗺𝗲𝗻𝘁𝗲, 𝗲𝘀𝗽𝗲𝗰𝗶𝗳𝗶𝗾𝘂𝗲 𝗼 𝗰𝗼́𝗱𝗶𝗴𝗼 𝗱𝗼 𝗶𝗱𝗶𝗼𝗺𝗮 𝗱𝗲 𝗱𝗲𝘀𝘁𝗶𝗻𝗼. 𝗦𝗲 𝗻𝗮̃𝗼 𝗲𝘀𝗽𝗲𝗰𝗶𝗳𝗶𝗰𝗮𝗱𝗼, 𝗼 𝗶𝗱𝗶𝗼𝗺𝗮 𝗱𝗲 𝗱𝗲𝘀𝘁𝗶𝗻𝗼 𝘀𝗲𝗿𝗮́ 𝗼 𝗶𝗻𝗴𝗹𝗲̂𝘀 (en).
- <code>/langcodes</code>: 𝗢𝗯𝘁𝗲𝗻𝗵𝗮 𝘂𝗺𝗮 𝗹𝗶𝘀𝘁𝗮 𝗱𝗲 𝗰𝗼́𝗱𝗶𝗴𝗼𝘀 𝗱𝗲 𝗶𝗱𝗶𝗼𝗺𝗮 𝗲 𝘀𝗲𝘂𝘀 𝗶𝗱𝗶𝗼𝗺𝗮𝘀 𝗰𝗼𝗿𝗿𝗲𝘀𝗽𝗼𝗻𝗱𝗲𝗻𝘁𝗲𝘀.
"""
