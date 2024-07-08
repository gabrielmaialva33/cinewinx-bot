from pyrogram.types import InlineKeyboardButton


def telegram_markup(_, chat_id):
    buttons = [
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(text="ᴍᴜᴛᴇ", callback_data=f"ADMIN Mute|{chat_id}"),
            InlineKeyboardButton(
                text="ᴜɴᴍᴜᴛᴇ", callback_data=f"ADMIN Unmute|{chat_id}"
            ),
        ],
        [
            InlineKeyboardButton(text=_["CLOSEMENU_BUTTON"], callback_data="close"),
        ],
    ]
    return buttons


# def stream_markup(_, chat_id):
#     buttons = [
#         [
#             InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}"),
#             InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}"),
#             InlineKeyboardButton(text="↻", callback_data=f"ADMIN Replay|{chat_id}"),
#             InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
#             InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}"),
#         ],
#         [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")],
#     ]
#     return buttons

def stream_markup(_, video_id: str , chat_id: int):
    buttons = [
        [
            InlineKeyboardButton(
                text="ᴀᴅᴅ ᴛᴏ ᴘʟᴀʏʟɪsᴛ", callback_data=f"add_playlist {video_id}"
            ),
        ],
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(text="ᴍᴜᴛᴇ", callback_data=f"ADMIN Mute|{chat_id}"),
            InlineKeyboardButton(
                text="ᴜɴᴍᴜᴛᴇ", callback_data=f"ADMIN Unmute|{chat_id}"
            ),
        ],
        [InlineKeyboardButton(text=_["CLOSEMENU_BUTTON"], callback_data="close")],
    ]
    return buttons
