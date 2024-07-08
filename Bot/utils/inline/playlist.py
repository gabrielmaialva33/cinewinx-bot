from pyrogram.types import InlineKeyboardButton


def bot_playlist_markup(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["PL_B_1"],
                callback_data="get_playlist_playmode",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["PL_B_12"], callback_data="get_cplaylist_playmode"
            ),
        ],
        [
            InlineKeyboardButton(text=_["PL_B_8"], callback_data="get_top_playlists"),
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
        ],
    ]
    return buttons