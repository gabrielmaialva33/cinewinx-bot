from typing import Union

from pyrogram.types import InlineKeyboardButton

from CineWinx import app
from config import GITHUB_REPO, SUPPORT_CHANNEL, SUPPORT_GROUP


def start_pannel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"],
                url=f"https://t.me/{app.username}?start=help",
            ),
            InlineKeyboardButton(text=_["S_B_2"], callback_data="settings_helper"),
        ],
    ]
    if SUPPORT_CHANNEL and SUPPORT_GROUP:
        buttons.append(
            [
                InlineKeyboardButton(text=_["S_B_4"], url=f"{SUPPORT_CHANNEL}"),
                InlineKeyboardButton(text=_["S_B_3"], url=f"{SUPPORT_GROUP}"),
            ]
        )
    else:
        if SUPPORT_CHANNEL:
            buttons.append(
                [InlineKeyboardButton(text=_["S_B_4"], url=f"{SUPPORT_CHANNEL}")]
            )
        if SUPPORT_GROUP:
            buttons.append(
                [InlineKeyboardButton(text=_["S_B_3"], url=f"{SUPPORT_GROUP}")]
            )
    return buttons


def private_panel(_, bot_username, owner: Union[bool, int] = None):
    buttons = [
        [InlineKeyboardButton(text=_["S_B_8"], callback_data="settings_back_helper")]
    ]
    if SUPPORT_CHANNEL and SUPPORT_GROUP:
        buttons.append(
            [
                InlineKeyboardButton(text=_["S_B_4"], url=f"{SUPPORT_CHANNEL}"),
                InlineKeyboardButton(text=_["S_B_3"], url=f"{SUPPORT_GROUP}"),
            ]
        )
    else:
        if SUPPORT_CHANNEL:
            buttons.append(
                [InlineKeyboardButton(text=_["S_B_4"], url=f"{SUPPORT_CHANNEL}")]
            )
        if SUPPORT_GROUP:
            buttons.append(
                [InlineKeyboardButton(text=_["S_B_3"], url=f"{SUPPORT_GROUP}")]
            )
    buttons.append(
        [
            InlineKeyboardButton(
                text=_["S_B_5"],
                url=f"https://t.me/{bot_username}?startgroup=true",
            )
        ]
    )
    if GITHUB_REPO and owner:
        buttons.append(
            [
                InlineKeyboardButton(text=_["S_B_7"], user_id=owner),
                InlineKeyboardButton(text=_["S_B_6"], url=f"{GITHUB_REPO}"),
            ]
        )
    else:

        if GITHUB_REPO:
            buttons.append(
                [
                    InlineKeyboardButton(text=_["S_B_6"], url=f"{GITHUB_REPO}"),
                ]
            )

        if owner:
            buttons.append(
                [
                    InlineKeyboardButton(text=_["S_B_7"], user_id=owner),
                ]
            )
    buttons.append([InlineKeyboardButton(text=_["ST_B_6"], callback_data="LG")])
    return buttons


def alive_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text="➕𝗺𝗲 𝗮𝗱𝗶𝗰𝗶𝗼𝗻𝗲", url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(text=_["S_B_3"], url=f"{SUPPORT_GROUP}"),
        ],
    ]
    return buttons
