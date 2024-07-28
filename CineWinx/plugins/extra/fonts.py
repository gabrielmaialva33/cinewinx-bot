import logging

import asyncio
from pyrogram import filters, Client
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from CineWinx.utils.winx_font import Fonts
from CineWinx import app
from config import PREFIXES, BANNED_USERS
from strings import get_command

FONT_COMMAND = get_command("FONT_COMMAND")


@app.on_message(filters.command(FONT_COMMAND, PREFIXES) & ~BANNED_USERS)
async def style_buttons(_client: Client, message: Message, cb=False):
    try:
        text = message.text.split(" ", 1)[1]
    except IndexError:
        await message.reply_text("📝 𝗘𝘀𝗰𝗿𝗲𝘃𝗮 𝗼 𝘁𝗲𝘅𝘁𝗼 𝗾𝘂𝗲 𝗱𝗲𝘀𝗲𝗷𝗮 𝗲𝘀𝘁𝗶𝗹𝗶𝘇𝗮𝗿. /font texto")
        return
    buttons = [
        [
            InlineKeyboardButton("𝚃𝚢𝚙𝚎𝚠𝚛𝚒𝚝𝚎𝚛", callback_data="style+typewriter"),
            InlineKeyboardButton("𝕆𝕦𝕥𝕝𝕚𝕟𝕖", callback_data="style+outline"),
            InlineKeyboardButton("𝐒𝐞𝐫𝐢𝐟", callback_data="style+serif"),
        ],
        [
            InlineKeyboardButton("𝑺𝒆𝒓𝒊𝒇", callback_data="style+bold_cool"),
            InlineKeyboardButton("𝑆𝑒𝑟𝑖𝑓", callback_data="style+cool"),
            InlineKeyboardButton("Sᴍᴀʟʟ Cᴀᴘs", callback_data="style+small_cap"),
        ],
        [
            InlineKeyboardButton("𝓈𝒸𝓇𝒾𝓅𝓉", callback_data="style+script"),
            InlineKeyboardButton("𝓼𝓬𝓻𝓲𝓹𝓽", callback_data="style+script_bolt"),
            InlineKeyboardButton("ᵗⁱⁿʸ", callback_data="style+tiny"),
        ],
        [
            InlineKeyboardButton("ᑕOᗰIᑕ", callback_data="style+comic"),
            InlineKeyboardButton("𝗦𝗮𝗻𝘀", callback_data="style+sans"),
            InlineKeyboardButton("𝙎𝙖𝙣𝙨", callback_data="style+slant_sans"),
        ],
        [
            InlineKeyboardButton("𝘚𝘢𝘯𝘴", callback_data="style+slant"),
            InlineKeyboardButton("𝖲𝖺𝗇𝗌", callback_data="style+sim"),
            InlineKeyboardButton("Ⓒ︎Ⓘ︎Ⓡ︎Ⓒ︎Ⓛ︎Ⓔ︎Ⓢ︎", callback_data="style+circles"),
        ],
        [
            InlineKeyboardButton("🅒︎🅘︎🅡︎🅒︎🅛︎🅔︎🅢︎", callback_data="style+circle_dark"),
            InlineKeyboardButton("𝔊𝔬𝔱𝔥𝔦𝔠", callback_data="style+gothic"),
            InlineKeyboardButton("𝕲𝖔𝖙𝖍𝖎𝖈", callback_data="style+gothic_bolt"),
        ],
        [
            InlineKeyboardButton("C͜͡l͜͡o͜͡u͜͡d͜͡s͜͡", callback_data="style+cloud"),
            InlineKeyboardButton("H̆̈ă̈p̆̈p̆̈y̆̈", callback_data="style+happy"),
            InlineKeyboardButton("S̑̈ȃ̈d̑̈", callback_data="style+sad"),
        ],
        [InlineKeyboardButton("𝗖𝗶𝗻𝗲𝗪𝗶𝗻𝘅", callback_data="style+cine")],
        [
            InlineKeyboardButton("❌ 𝗙𝗲𝗰𝗵𝗮𝗿", callback_data="close_reply"),
            InlineKeyboardButton("➡️ 𝗣𝗿𝗼́𝘅𝗶𝗺𝗼", callback_data="nxt"),
        ],
    ]
    if not cb:
        await message.reply_text(
            f"{text}", reply_markup=InlineKeyboardMarkup(buttons), quote=True
        )
    else:
        await message.answer()
        await message.message.edit_reply_markup(InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters.regex("^nxt"))
async def nxt(c, m):
    if m.data == "nxt":
        buttons = [
            [
                InlineKeyboardButton("🇸 🇵 🇪 🇨 🇮 🇦 🇱 ", callback_data="style+special"),
                InlineKeyboardButton("🅂🅀🅄🄰🅁🄴🅂", callback_data="style+squares"),
                InlineKeyboardButton("🆂︎🆀︎🆄︎🅰︎🆁︎🅴︎🆂︎", callback_data="style+squares_bold"),
            ],
            [
                InlineKeyboardButton("ꪖꪀᦔꪖꪶꪊᥴ𝓲ꪖ", callback_data="style+andalucia"),
                InlineKeyboardButton("爪卂几ᘜ卂", callback_data="style+manga"),
                InlineKeyboardButton("S̾t̾i̾n̾k̾y̾", callback_data="style+stinky"),
            ],
            [
                InlineKeyboardButton("B̥ͦu̥ͦb̥ͦb̥ͦl̥ͦe̥ͦs̥ͦ", callback_data="style+bubbles"),
                InlineKeyboardButton("U͟n͟d͟e͟r͟l͟i͟n͟e͟", callback_data="style+underline"),
                InlineKeyboardButton("꒒ꍏꀷꌩꌃꀎꁅ", callback_data="style+ladybug"),
            ],
            [
                InlineKeyboardButton("R҉a҉y҉s҉", callback_data="style+rays"),
                InlineKeyboardButton("B҈i҈r҈d҈s҈", callback_data="style+birds"),
                InlineKeyboardButton("S̸l̸a̸s̸h̸", callback_data="style+slash"),
            ],
            [
                InlineKeyboardButton("s⃠t⃠o⃠p⃠", callback_data="style+stop"),
                InlineKeyboardButton("S̺͆k̺͆y̺͆l̺͆i̺͆n̺͆e̺͆", callback_data="style+skyline"),
                InlineKeyboardButton("A͎r͎r͎o͎w͎s͎", callback_data="style+arrows"),
            ],
            [
                InlineKeyboardButton("ዪሀክቿነ", callback_data="style+qvnes"),
                InlineKeyboardButton("S̶t̶r̶i̶k̶e̶", callback_data="style+strike"),
                InlineKeyboardButton("F༙r༙o༙z༙e༙n༙", callback_data="style+frozen"),
            ],
            [
                InlineKeyboardButton("❌ 𝗙𝗲𝗰𝗵𝗮𝗿", callback_data="close_reply"),
                InlineKeyboardButton("🔙 𝗩𝗼𝗹𝘁𝗮𝗿", callback_data="nxt+0"),
            ],
        ]
        await m.answer()
        try:
            await m.message.edit_reply_markup(InlineKeyboardMarkup(buttons))
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await m.message.edit_reply_markup(InlineKeyboardMarkup(buttons))
        except Exception as e:
            logging.warning(e)
    else:
        await style_buttons(c, m, cb=True)


@app.on_callback_query(filters.regex("^style"))
async def style(_client: Client, message: Message):
    await message.answer()
    cmd, style = message.data.split("+")
    if style == "typewriter":
        cls = Fonts.typewriter
    if style == "outline":
        cls = Fonts.outline
    if style == "serif":
        cls = Fonts.serief
    if style == "bold_cool":
        cls = Fonts.bold_cool
    if style == "cool":
        cls = Fonts.cool
    if style == "small_cap":
        cls = Fonts.smallcap
    if style == "script":
        cls = Fonts.script
    if style == "script_bolt":
        cls = Fonts.bold_script
    if style == "tiny":
        cls = Fonts.tiny
    if style == "comic":
        cls = Fonts.comic
    if style == "sans":
        cls = Fonts.san
    if style == "slant_sans":
        cls = Fonts.slant_san
    if style == "slant":
        cls = Fonts.slant
    if style == "sim":
        cls = Fonts.sim
    if style == "circles":
        cls = Fonts.circles
    if style == "circle_dark":
        cls = Fonts.dark_circle
    if style == "gothic":
        cls = Fonts.gothic
    if style == "gothic_bolt":
        cls = Fonts.bold_gothic
    if style == "cloud":
        cls = Fonts.cloud
    if style == "happy":
        cls = Fonts.happy
    if style == "sad":
        cls = Fonts.sad
    if style == "special":
        cls = Fonts.special
    if style == "squares":
        cls = Fonts.square
    if style == "squares_bold":
        cls = Fonts.dark_square
    if style == "andalucia":
        cls = Fonts.andalucia
    if style == "manga":
        cls = Fonts.manga
    if style == "stinky":
        cls = Fonts.stinky
    if style == "bubbles":
        cls = Fonts.bubbles
    if style == "underline":
        cls = Fonts.underline
    if style == "ladybug":
        cls = Fonts.ladybug
    if style == "rays":
        cls = Fonts.rays
    if style == "birds":
        cls = Fonts.birds
    if style == "slash":
        cls = Fonts.slash
    if style == "stop":
        cls = Fonts.stop
    if style == "skyline":
        cls = Fonts.skyline
    if style == "arrows":
        cls = Fonts.arrows
    if style == "qvnes":
        cls = Fonts.rvnes
    if style == "strike":
        cls = Fonts.strike
    if style == "frozen":
        cls = Fonts.frozen
    if style == "cine":
        cls = Fonts.cine
    new_text = cls(message.message.reply_to_message.text.split(" ", 1)[1])
    try:
        await message.message.edit_text(
            new_text, reply_markup=message.message.reply_markup
        )
    except Exception as e:
        logging.warning(e)


__MODULE__ = "🔠 𝗙𝗼𝗻𝘁𝗲𝘀"
__HELP__ = """
<b>🔠 𝗘𝘀𝗰𝗼𝗹𝗵𝗮 𝗼 𝘁𝗲𝘅𝘁𝗼 𝗾𝘂𝗲 𝗱𝗲𝘀𝗲𝗷𝗮 𝗲𝘀𝘁𝗶𝗹𝗼:</b>

• /font <𝘁𝗲𝘅𝘁𝗼>: 𝗘𝘀𝗰𝗼𝗹𝗵𝗮 𝗼 𝘁𝗲𝘅𝘁𝗼 𝗾𝘂𝗲 𝗱𝗲𝘀𝗲𝗷𝗮 𝗲𝘀𝘁𝗶𝗹𝗼. 🔠
• /fonts <𝘁𝗲𝘅𝘁𝗼>: 𝗘𝘀𝗰𝗼𝗹𝗵𝗮 𝗼 𝘁𝗲𝘅𝘁𝗼 𝗾𝘂𝗲 𝗱𝗲𝘀𝗲𝗷𝗮 𝗲𝘀𝘁𝗶𝗹𝗼. 🔠
"""
