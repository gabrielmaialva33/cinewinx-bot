from pyrogram.types import InlineKeyboardButton


def bot_playlist_markup(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["pl_b_1"],
                callback_data="get_playlist_playmode",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["pl_b_12"], callback_data="get_cplaylist_playmode"
            ),
        ],
        [
            InlineKeyboardButton(text=_["pl_b_8"], callback_data="get_top_playlists"),
        ],
        [
            InlineKeyboardButton(text=_["close_btn"], callback_data="close"),
        ],
    ]
    return buttons
