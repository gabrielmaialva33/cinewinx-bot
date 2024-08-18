import logging

from pyrogram import filters, Client
from pyrogram.enums import ChatType
from pyrogram.errors import MessageNotModified
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from CineWinx import app
from CineWinx.utils.database import (
    add_nonadmin_chat,
    get_aud_bit_name,
    cleanmode_off,
    cleanmode_on,
    commanddelete_off,
    commanddelete_on,
    get_authuser,
    get_authuser_names,
    get_playmode,
    get_playtype,
    get_vid_bit_name,
    is_nonadmin_chat,
    is_cleanmode_on,
    is_commanddelete_on,
    remove_nonadmin_chat,
    save_audio_bitrate,
    save_video_bitrate,
    set_playmode,
    set_playtype,
)
from CineWinx.utils.decorators.admins import actual_admin_cb
from CineWinx.utils.decorators.language import language, language_cb
from CineWinx.utils.inline.settings import (
    audio_quality_markup,
    auth_users_markup,
    cleanmode_settings_markup,
    playmode_users_markup,
    setting_markup,
    video_quality_markup,
)
from CineWinx.utils.inline.start import private_panel
from config import BANNED_USERS, CLEANMODE_DELETE_MINS, OWNER_ID, PREFIXES
from strings import get_command

SETTINGS_COMMAND = get_command("SETTINGS_COMMAND")


@app.on_message(
    filters.command(SETTINGS_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS
)
@language
async def settings_mar(client: Client, message: Message, _):
    me = await client.get_me()
    pic = await client.download_media(me.photo.big_file_id) if me.photo else None
    buttons = setting_markup(_)
    chat_id = message.chat.id
    await message.reply_photo(
        photo=pic,
        caption=_["setting_1"].format(message.chat.title, chat_id),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("settings_helper") & ~BANNED_USERS)
@language_cb
async def settings_cb(_client: Client, callback_query: CallbackQuery, _):
    try:
        await callback_query.answer(_["set_cb_8"])
    except Exception as e:
        logging.error(e)
    buttons = setting_markup(_)

    return await callback_query.edit_message_text(
        _["setting_1"].format(
            callback_query.message.chat.title,
            callback_query.message.chat.id,
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("settingsback_helper") & ~BANNED_USERS)
@language_cb
async def settings_back_markup(client: Client, callback_query: CallbackQuery, _):
    try:
        await callback_query.answer()
    except Exception as e:
        print(f"An error occurred: {e}")

    if callback_query.message.chat.type == ChatType.PRIVATE:
        try:
            await app.resolve_peer(OWNER_ID[0])
            owner = OWNER_ID[0]
        except:
            owner = None
        buttons = private_panel(_, app.username, owner)
        try:
            me = await client.get_me()
            pic = await client.download_media(me.photo.big_file_id) if me.photo else None
            await callback_query.edit_message_text(
                _["start_1"].format(app.mention),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        except MessageNotModified:
            pass
    else:
        buttons = setting_markup(_)
        try:
            await callback_query.edit_message_reply_markup(
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except MessageNotModified:
            pass


## Audio and Video Quality
async def gen_buttons_aud(_, aud: str):
    if aud == "STUDIO":
        buttons = audio_quality_markup(_, STUDIO=True)
    elif aud == "HIGH":
        buttons = audio_quality_markup(_, HIGH=True)
    elif aud == "MEDIUM":
        buttons = audio_quality_markup(_, MEDIUM=True)
    elif aud == "LOW":
        buttons = audio_quality_markup(_, LOW=True)
    return buttons


async def gen_buttons_vid(_, aud: str):
    if aud == "UHD_4K":
        buttons = video_quality_markup(_, UHD_4K=True)
    elif aud == "QHD_2K":
        buttons = video_quality_markup(_, QHD_2K=True)
    elif aud == "FHD_1080p":
        buttons = video_quality_markup(_, FHD_1080p=True)
    elif aud == "HD_720p":
        buttons = video_quality_markup(_, HD_720p=True)
    elif aud == "SD_480p":
        buttons = video_quality_markup(_, SD_480p=True)
    elif aud == "SD_360p":
        buttons = video_quality_markup(_, SD_360p=True)
    return buttons


# without admin rights


@app.on_callback_query(
    filters.regex(
        pattern=r"^(SEARCHANSWER|PLAYMODEANSWER|PLAYTYPEANSWER|AUTHANSWER|CMANSWER|COMMANDANSWER|CM|AQ|VQ|PM|AU)$"
    )
    & ~BANNED_USERS
)
@language_cb
async def without_Admin_rights(_client: app, callback_query: CallbackQuery, _):
    command = callback_query.matches[0].group(1)
    if command == "SEARCHANSWER":
        try:
            return await callback_query.answer(_["setting_3"], show_alert=True)
        except:
            return
    if command == "PLAYMODEANSWER":
        try:
            return await callback_query.answer(_["setting_10"], show_alert=True)
        except:
            return
    if command == "PLAYTYPEANSWER":
        try:
            return await callback_query.answer(_["setting_11"], show_alert=True)
        except:
            return
    if command == "AUTHANSWER":
        try:
            return await callback_query.answer(_["setting_4"], show_alert=True)
        except:
            return
    if command == "CMANSWER":
        try:
            return await callback_query.answer(
                _["setting_9"].format(CLEANMODE_DELETE_MINS),
                show_alert=True,
            )
        except:
            return
    if command == "COMMANDANSWER":
        try:
            return await callback_query.answer(_["setting_14"], show_alert=True)
        except:
            return
    if command == "CM":
        try:
            await callback_query.answer(_["set_cb_5"], show_alert=True)
        except:
            pass
        sta = None
        cle = None
        if await is_cleanmode_on(callback_query.message.chat.id):
            cle = True
        if await is_commanddelete_on(callback_query.message.chat.id):
            sta = True
        buttons = cleanmode_settings_markup(_, status=cle, dels=sta)

    if command == "AQ":
        try:
            await callback_query.answer(_["set_cb_1"], show_alert=True)
        except:
            pass
        aud = await get_aud_bit_name(callback_query.message.chat.id)
        buttons = await gen_buttons_aud(_, aud)
    if command == "VQ":
        try:
            await callback_query.answer(_["set_cb_2"], show_alert=True)
        except:
            pass
        aud = await get_vid_bit_name(callback_query.message.chat.id)
        buttons = await gen_buttons_vid(_, aud)
    if command == "PM":
        try:
            await callback_query.answer(_["set_cb_4"], show_alert=True)
        except:
            pass
        playmode = await get_playmode(callback_query.message.chat.id)
        if playmode == "Direct":
            Direct = True
        else:
            Direct = None
        is_non_admin = await is_nonadmin_chat(callback_query.message.chat.id)
        if not is_non_admin:
            Group = True
        else:
            Group = None
        playty = await get_playtype(callback_query.message.chat.id)
        if playty == "Everyone":
            Playtype = None
        else:
            Playtype = True
        buttons = playmode_users_markup(_, Direct, Group, Playtype)
    if command == "AU":
        try:
            await callback_query.answer(_["set_cb_3"], show_alert=True)
        except:
            pass
        is_non_admin = await is_nonadmin_chat(callback_query.message.chat.id)
        if not is_non_admin:
            buttons = auth_users_markup(_, True)
        else:
            buttons = auth_users_markup(_)
    try:
        return await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


# Audio Video Quality


@app.on_callback_query(
    filters.regex(
        pattern=r"^(LOW|MEDIUM|HIGH|STUDIO|SD_360p|SD_480p|HD_720p|FHD_1080p|QHD_2K|UHD_4K)$"
    )
    & ~BANNED_USERS
)
@actual_admin_cb
async def aud_vid_cb(_client: app, callback_query: CallbackQuery, _):
    command = callback_query.matches[0].group(1)
    try:
        await callback_query.answer(_["set_cb_6"], show_alert=True)
    except:
        pass
    if command == "LOW":
        await save_audio_bitrate(callback_query.message.chat.id, "LOW")
        buttons = audio_quality_markup(_, LOW=True)
    if command == "MEDIUM":
        await save_audio_bitrate(callback_query.message.chat.id, "MEDIUM")
        buttons = audio_quality_markup(_, MEDIUM=True)
    if command == "HIGH":
        await save_audio_bitrate(callback_query.message.chat.id, "HIGH")
        buttons = audio_quality_markup(_, HIGH=True)
    if command == "STUDIO":
        await save_audio_bitrate(callback_query.message.chat.id, "STUDIO")
        buttons = audio_quality_markup(_, STUDIO=True)
    if command == "SD_360p":
        await save_video_bitrate(callback_query.message.chat.id, "SD_360p")
        buttons = video_quality_markup(_, SD_360p=True)
    if command == "SD_480p":
        await save_video_bitrate(callback_query.message.chat.id, "SD_480p")
        buttons = video_quality_markup(_, SD_480p=True)
    if command == "HD_720p":
        await save_video_bitrate(callback_query.message.chat.id, "HD_720p")
        buttons = video_quality_markup(_, HD_720p=True)
    if command == "FHD_1080p":
        await save_video_bitrate(callback_query.message.chat.id, "FHD_1080p")
        buttons = video_quality_markup(_, FHD_1080p=True)
    if command == "QHD_2K":
        await save_video_bitrate(callback_query.message.chat.id, "QHD_2K")
        buttons = video_quality_markup(_, QHD_2K=True)
    if command == "UHD_4K":
        await save_video_bitrate(callback_query.message.chat.id, "UHD_4K")
        buttons = video_quality_markup(_, UHD_4K=True)
    try:
        return await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


@app.on_callback_query(
    filters.regex(pattern=r"^(CLEANMODE|COMMANDELMODE)$") & ~BANNED_USERS
)
@actual_admin_cb
async def cleanmode_mark(_client: Client, callback_query: CallbackQuery, _):
    command = callback_query.matches[0].group(1)
    try:
        await callback_query.answer(_["set_cb_6"], show_alert=True)
    except:
        pass
    if command == "CLEANMODE":
        sta = None
        if await is_commanddelete_on(callback_query.message.chat.id):
            sta = True
        cle = None
        if await is_cleanmode_on(callback_query.message.chat.id):
            await cleanmode_off(callback_query.message.chat.id)
        else:
            await cleanmode_on(callback_query.message.chat.id)
            cle = True
        buttons = cleanmode_settings_markup(_, status=cle, dels=sta)
        return await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    if command == "COMMANDELMODE":
        cle = None
        sta = None
        if await is_cleanmode_on(callback_query.message.chat.id):
            cle = True
        if await is_commanddelete_on(callback_query.message.chat.id):
            await commanddelete_off(callback_query.message.chat.id)
        else:
            await commanddelete_on(callback_query.message.chat.id)
            sta = True
        buttons = cleanmode_settings_markup(_, status=cle, dels=sta)
    try:
        return await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


# Play Mode Settings
@app.on_callback_query(
    filters.regex(pattern=r"^(|MODECHANGE|CHANNELMODECHANGE|PLAYTYPECHANGE)$")
    & ~BANNED_USERS
)
@actual_admin_cb
async def playmode_ans(_client: app, callback_query: CallbackQuery, _):
    command = callback_query.matches[0].group(1)
    if command == "CHANNELMODECHANGE":
        is_non_admin = await is_nonadmin_chat(callback_query.message.chat.id)
        if not is_non_admin:
            await add_nonadmin_chat(callback_query.message.chat.id)
            Group = None
        else:
            await remove_nonadmin_chat(callback_query.message.chat.id)
            Group = True
        playmode = await get_playmode(callback_query.message.chat.id)
        if playmode == "Direct":
            Direct = True
        else:
            Direct = None
        playty = await get_playtype(callback_query.message.chat.id)
        if playty == "Everyone":
            Playtype = None
        else:
            Playtype = True
        buttons = playmode_users_markup(_, Direct, Group, Playtype)
    if command == "MODECHANGE":
        try:
            await callback_query.answer(_["set_cb_6"], show_alert=True)
        except:
            pass
        playmode = await get_playmode(callback_query.message.chat.id)
        if playmode == "Direct":
            await set_playmode(callback_query.message.chat.id, "Inline")
            Direct = None
        else:
            await set_playmode(callback_query.message.chat.id, "Direct")
            Direct = True
        is_non_admin = await is_nonadmin_chat(callback_query.message.chat.id)
        if not is_non_admin:
            Group = True
        else:
            Group = None
        playty = await get_playtype(callback_query.message.chat.id)
        if playty == "Everyone":
            Playtype = False
        else:
            Playtype = True
        buttons = playmode_users_markup(_, Direct, Group, Playtype)
    if command == "PLAYTYPECHANGE":
        try:
            await callback_query.answer(_["set_cb_6"], show_alert=True)
        except:
            pass
        playty = await get_playtype(callback_query.message.chat.id)
        if playty == "Everyone":
            await set_playtype(callback_query.message.chat.id, "Admin")
            Playtype = False
        else:
            await set_playtype(callback_query.message.chat.id, "Everyone")
            Playtype = True
        playmode = await get_playmode(callback_query.message.chat.id)
        if playmode == "Direct":
            Direct = True
        else:
            Direct = None
        is_non_admin = await is_nonadmin_chat(callback_query.message.chat.id)
        if not is_non_admin:
            Group = True
        else:
            Group = None
        buttons = playmode_users_markup(_, Direct, Group, Playtype)
    try:
        return await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


# Auth Users Settings
@app.on_callback_query(filters.regex(pattern=r"^(AUTH|AUTHLIST)$") & ~BANNED_USERS)
@actual_admin_cb
async def authusers_mar(client: app, callback_query: CallbackQuery, _):
    command = callback_query.matches[0].group(1)
    if command == "AUTHLIST":
        _authusers = await get_authuser_names(callback_query.message.chat.id)
        if not _authusers:
            try:
                return await callback_query.answer(_["setting_5"], show_alert=True)
            except:
                return
        else:
            try:
                await callback_query.answer(_["set_cb_7"], show_alert=True)
            except:
                pass
            j = 0
            await callback_query.edit_message_text(_["auth_6"])
            msg = _["auth_7"]
            for note in _authusers:
                _note = await get_authuser(callback_query.message.chat.id, note)
                user_id = _note["auth_user_id"]
                admin_id = _note["admin_id"]
                admin_name = _note["admin_name"]
                try:
                    user = await client.get_users(user_id)
                    user = user.first_name
                    j += 1
                except Exception:
                    continue
                msg += f"{j}➤ {user}[`{user_id}`]\n"
                msg += f"   {_['auth_8']} {admin_name}[{admin_id}]\n\n"
            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=_["BACK_BUTTON"], callback_data=f"AU"
                        ),
                        InlineKeyboardButton(
                            text=_["CLOSE_BUTTON"],
                            callback_data=f"close",
                        ),
                    ]
                ]
            )
            try:
                return await callback_query.edit_message_text(msg, reply_markup=upl)
            except MessageNotModified:
                return
    try:
        await callback_query.answer(_["set_cb_6"], show_alert=True)
    except:
        pass
    if command == "AUTH":
        is_non_admin = await is_nonadmin_chat(callback_query.message.chat.id)
        if not is_non_admin:
            await add_nonadmin_chat(callback_query.message.chat.id)
            buttons = auth_users_markup(_)
        else:
            await remove_nonadmin_chat(callback_query.message.chat.id)
            buttons = auth_users_markup(_, True)
    try:
        return await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


__MODULE__ = "𝗖𝗼𝗻𝗳𝗶𝗴 ⚙️"
__HELP__ = """

✅<u>𝗖𝗼𝗻𝗳𝗶𝗴𝘂𝗿𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗼 𝗚𝗿𝘂𝗽𝗼:</u>

⚙️ /settings - 𝗢𝗯𝘁𝗲𝗻𝗵𝗮 𝗮𝘀 𝗰𝗼𝗻𝗳𝗶𝗴𝘂𝗿𝗮𝗰̧𝗼̃𝗲𝘀 𝗰𝗼𝗺𝗽𝗹𝗲𝘁𝗮𝘀 𝗱𝗼 𝗴𝗿𝘂𝗽𝗼 𝗰𝗼𝗺 𝗯𝗼𝘁𝗼̃𝗲𝘀 𝗶𝗻𝗹𝗶𝗻𝗲

🔗 <u>𝗢𝗽𝗰̧𝗼̃𝗲𝘀 𝗻𝗮𝘀 𝗖𝗼𝗻𝗳𝗶𝗴𝘂𝗿𝗮𝗰̧𝗼̃𝗲𝘀:</u>

1️⃣ 𝗩𝗼𝗰𝗲̂ 𝗽𝗼𝗱𝗲 𝗱𝗲𝗳𝗶𝗻𝗶𝗿 𝗮 𝗤𝘂𝗮𝗹𝗶𝗱𝗮𝗱𝗲 𝗱𝗼 𝗔́𝘂𝗱𝗶𝗼
2️⃣ 𝗩𝗼𝗰𝗲̂ 𝗽𝗼𝗱𝗲 𝗱𝗲𝗳𝗶𝗻𝗶𝗿 𝗮 𝗤𝘂𝗮𝗹𝗶𝗱𝗮𝗱𝗲 𝗱𝗼 𝗩𝗶́𝗱𝗲𝗼
3️⃣ <b>👥 𝗨𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗔𝘂𝘁𝗼𝗿𝗶𝘇𝗮𝗱𝗼𝘀</b>: 𝗩𝗼𝗰𝗲̂ 𝗽𝗼𝗱𝗲 𝗺𝘂𝗱𝗮𝗿 𝗼 𝗺𝗼𝗱𝗼 𝗱𝗲 𝗰𝗼𝗺𝗮𝗻𝗱𝗼𝘀 𝗱𝗲 𝗮𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿 𝗽𝗮𝗿𝗮 𝘁𝗼𝗱𝗼𝘀 𝗼𝘂 𝗮𝗽𝗲𝗻𝗮𝘀 𝗮𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿𝗲𝘀.
4️⃣ <b>🧹 𝗠𝗼𝗱𝗼 𝗟𝗶𝗺𝗽𝗼</b>: 𝗢 𝗯𝗼𝘁 𝗮𝗽𝗮𝗴𝗮 𝗮𝘀 𝗺𝗲𝗻𝘀𝗮𝗴𝗲𝗻𝘀 𝗱𝗼 𝗯𝗼𝘁 𝗮𝗽𝗼́𝘀 5 𝗺𝗶𝗻𝘂𝘁𝗼𝘀 𝗱𝗼 𝘀𝗲𝘂 𝗴𝗿𝘂𝗽𝗼 𝗽𝗮𝗿𝗮 𝗴𝗮𝗿𝗮𝗻𝘁𝗶𝗿 𝗾𝘂𝗲 𝘀𝗲𝘂 𝗰𝗵𝗮𝘁 𝗽𝗲𝗿𝗺𝗮𝗻𝗲𝗰̧𝗮 𝗹𝗶𝗺𝗽𝗼 𝗲 𝗼𝗿𝗴𝗮𝗻𝗶𝘇𝗮𝗱𝗼.
5️⃣ <b>🗑️ 𝗟𝗶𝗺𝗽𝗲𝘇𝗮 𝗱𝗲 𝗖𝗼𝗺𝗮𝗻𝗱𝗼𝘀</b>: 𝗤𝘂𝗮𝗻𝗱𝗼 𝗮𝘁𝗶𝘃𝗮𝗱𝗼, 𝗼 𝗯𝗼𝘁 𝗮𝗽𝗮𝗴𝗮𝗿𝗮́ 𝗶𝗺𝗲𝗱𝗶𝗮𝘁𝗮𝗺𝗲𝗻𝘁𝗲 𝗼𝘀 𝗰𝗼𝗺𝗮𝗻𝗱𝗼𝘀 𝗲𝘅𝗲𝗰𝘂𝘁𝗮𝗱𝗼𝘀.

<b><u>▶️ 𝗖𝗼𝗻𝗳𝗶𝗴𝘂𝗿𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗲 𝗥𝗲𝗽𝗿𝗼𝗱𝘂𝗰̧𝗮̃𝗼:</u></b>
⚙️ /playmode - 𝗢𝗯𝘁𝗲𝗻𝗵𝗮 𝘂𝗺 𝗽𝗮𝗶𝗻𝗲𝗹 𝗰𝗼𝗺𝗽𝗹𝗲𝘁𝗼 𝗱𝗲 𝗰𝗼𝗻𝗳𝗶𝗴𝘂𝗿𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗲 𝗿𝗲𝗽𝗿𝗼𝗱𝘂𝗰̧𝗮̃𝗼 𝗰𝗼𝗺 𝗯𝗼𝘁𝗼̃𝗲𝘀 𝗼𝗻𝗱𝗲 𝘃𝗼𝗰𝗲̂ 𝗽𝗼𝗱𝗲 𝗱𝗲𝗳𝗶𝗻𝗶𝗿 𝗮𝘀 𝗰𝗼𝗻𝗳𝗶𝗴𝘂𝗿𝗮𝗰̧𝗼̃𝗲𝘀 𝗱𝗲 𝗿𝗲𝗽𝗿𝗼𝗱𝘂𝗰̧𝗮̃𝗼 𝗱𝗼 𝘀𝗲𝘂 𝗴𝗿𝘂𝗽𝗼.

<b><u>🔧 𝗢𝗽𝗰̧𝗼𝗲𝘀 𝗻𝗼 𝗠𝗼𝗱𝗼 𝗱𝗲 𝗥𝗲𝗽𝗿𝗼𝗱𝘂𝗰̧𝗮̃𝗼:</u></b>
1️⃣ <b>🔎 𝗠𝗼𝗱𝗼 𝗱𝗲 𝗕𝘂𝘀𝗰𝗮</b> [𝗗𝗶𝗿𝗲𝘁𝗼 𝗼𝘂 𝗜𝗻𝗹𝗶𝗻𝗲] - 𝗔𝗹𝘁𝗲𝗿𝗮 𝗼 𝘀𝗲𝘂 𝗺𝗼𝗱𝗼 𝗱𝗲 𝗯𝘂𝘀𝗰𝗮 𝗲𝗻𝗾𝘂𝗮𝗻𝘁𝗼 𝘃𝗼𝗰𝗲̂ 𝘂𝘀𝗮 /playmode
2️⃣ <b>👮‍♂️ 𝗖𝗼𝗺𝗮𝗻𝗱𝗼𝘀 𝗱𝗲 𝗔𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿</b> [𝗧𝗼𝗱𝗼𝘀 𝗼𝘂 𝗔𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿𝗲𝘀] - 𝗦𝗲 𝗳𝗼𝗿 𝘁𝗼𝗱𝗼𝘀, 𝗾𝘂𝗮𝗹𝗾𝘂𝗲𝗿 𝘂𝗺 𝗻𝗼 𝘀𝗲𝘂 𝗴𝗿𝘂𝗽𝗼 𝗽𝗼𝗱𝗲𝗿𝗮́ 𝘂𝘀𝗮𝗿 𝗰𝗼𝗺𝗮𝗻𝗱𝗼𝘀 𝗱𝗲 𝗮𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿 (𝗰𝗼𝗺𝗼 /skip, /stop 𝗲𝘁𝗰)
3️⃣ <b>🔄 𝗧𝗶𝗽𝗼 𝗱𝗲 𝗥𝗲𝗽𝗿𝗼𝗱𝘂𝗰̧𝗮̃𝗼</b> [𝗧𝗼𝗱𝗼𝘀 𝗼𝘂 𝗔𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿𝗲𝘀] - 𝗦𝗲 𝗳𝗼𝗿 𝗮𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿𝗲𝘀, 𝗮𝗽𝗲𝗻𝗮𝘀 𝗼𝘀 𝗮𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗱𝗼𝗿𝗲𝘀 𝗱𝗼 𝗴𝗿𝘂𝗽𝗼 𝗽𝗼𝗱𝗲𝗿𝗮̃𝗼 𝗿𝗲𝗽𝗿𝗼𝗱𝘂𝘇𝗶𝗿 𝗺𝘂́𝘀𝗶𝗰𝗮 𝗻𝗼 𝗰𝗵𝗮𝘁 𝗱𝗲 𝘃𝗼𝘇.
"""
