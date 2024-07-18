import asyncio
import logging
import os
from random import randint

import requests
from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    CallbackQuery,
)
from youtube_search import YoutubeSearch

from CineWinx import Carbon, app
from CineWinx.utils.database import (
    delete_playlist,
    get_assistant,
    get_playlist,
    get_playlist_names,
    save_playlist,
)
from CineWinx.utils.decorators.language import language, language_cb
from CineWinx.utils.inline.playlist import (
    botplaylist_markup,
    get_cplaylist_markup,
    get_playlist_markup,
    warning_markup,
)
from CineWinx.utils.pastebin import winx_bin
from CineWinx.utils.stream.stream import stream
from config import BANNED_USERS, SERVER_PLAYLIST_LIMIT


@app.on_message(filters.command(["playlist"]) & ~BANNED_USERS)
@language
async def check_playlist(_client: app, message: Message, _):
    _playlist = await get_playlist_names(message.from_user.id)
    if _playlist:
        get = await message.reply_text(_["playlist_2"])
    else:
        return await message.reply_text(_["playlist_3"])
    msg = _["playlist_4"]
    count = 0
    for ptlist in _playlist:
        _note = await get_playlist(message.from_user.id, ptlist)
        title = _note["title"]
        title = title.title()
        duration = _note["duration"]
        count += 1
        msg += f"\n\n{count}- {title[:70]}\n"
        msg += _["playlist_5"].format(duration)
    link = await winx_bin(msg)
    lines = msg.count("\n")
    if lines >= 17:
        car = os.linesep.join(msg.split(os.linesep)[:17])
    else:
        car = msg
    carbon = await Carbon.generate(car, randint(100, 10000000000))
    await get.delete()
    await message.reply_photo(carbon, caption=_["playlist_15"].format(link))


async def get_keyboard(_, user_id: int):
    keyboard = InlineKeyboard(row_width=5)
    _playlist = await get_playlist_names(user_id)
    count = len(_playlist)
    for x in _playlist:
        _note = await get_playlist(user_id, x)
        title = _note["title"]
        title = title.title()
        keyboard.row(
            InlineKeyboardButton(
                text=title,
                callback_data=f"del_playlist {x}",
            )
        )
    keyboard.row(
        InlineKeyboardButton(
            text=_["PL_B_5"],
            callback_data=f"delete_warning",
        ),
        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"close"),
    )
    return keyboard, count


@app.on_message(
    filters.command(["deleteplaylist", "delplaylist"]) & filters.group & ~BANNED_USERS
)
@language
async def del_group_message(_client: app, message: Message, _):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["PL_B_6"],
                    url=f"https://t.me/{app.username}?start=delplaylists",
                ),
            ]
        ]
    )
    await message.reply_text(_["playlist_6"], reply_markup=upl)


async def get_keyboard(_, user_id: int):
    keyboard = InlineKeyboard(row_width=5)
    _playlist = await get_playlist_names(user_id)
    count = len(_playlist)
    for x in _playlist:
        _note = await get_playlist(user_id, x)
        title = _note["title"]
        title = title.title()
        keyboard.row(
            InlineKeyboardButton(
                text=title,
                callback_data=f"del_playlist {x}",
            )
        )
    keyboard.row(
        InlineKeyboardButton(
            text=_["PL_B_5"],
            callback_data=f"delete_warning",
        ),
        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"close"),
    )
    return keyboard, count


@app.on_message(
    filters.command(["deleteplaylist", "delplaylist"]) & filters.private & ~BANNED_USERS
)
@language
async def del_plist_msg(_client: app, message: Message, _):
    _playlist = await get_playlist_names(message.from_user.id)
    if _playlist:
        get = await message.reply_text(_["playlist_2"])
    else:
        return await message.reply_text(_["playlist_3"])
    keyboard, count = await get_keyboard(_, message.from_user.id)
    await get.edit_text(_["playlist_7"].format(count), reply_markup=keyboard)


@app.on_callback_query(filters.regex("play_playlist") & ~BANNED_USERS)
@language_cb
async def play_playlist(client: app, callback_query: CallbackQuery, _):
    userbot = await get_assistant(callback_query.message.chat.id)
    try:
        try:
            get = await app.get_chat_member(callback_query.message.chat.id, userbot.id)
        except ChatAdminRequired:
            return await callback_query.answer(
                f"Não tenho permissão para convidar usuários por link para adicionar o assistente ao {callback_query.message.chat.title}.",
                show_alert=True,
            )
        if get.status == ChatMemberStatus.BANNED:
            return await callback_query.answer(
                text=f"»Assistente está banido em {callback_query.message.chat.title}",
                show_alert=True,
            )
    except UserNotParticipant:
        if callback_query.message.chat.username:
            invitelink = callback_query.message.chat.username
            try:
                await userbot.resolve_peer(invitelink)
            except Exception as ex:
                logging.exception(ex)
        else:
            try:
                invitelink = await client.export_chat_invite_link(
                    callback_query.message.chat.id
                )
            except ChatAdminRequired:
                return await callback_query.answer(
                    f"Não tenho permissões para convidar usuários por link "
                    f"para adicionar o assistente ao {callback_query.message.chat.title}.",
                    show_alert=True,
                )
            except InviteRequestSent:
                try:
                    await app.approve_chat_join_request(
                        callback_query.message.chat.id, userbot.id
                    )
                except Exception as e:
                    return await callback_query.message.reply_text(
                        f"Falha ao convidar o assistente para {callback_query.message.chat.title}\nMotivo: {e}"
                    )
            except Exception as ex:
                if "channels.JoinChannel" in str(ex) or "Username not found" in str(ex):
                    return await callback_query.answer(
                        f"Não tenho permissão para convidar usuários por link "
                        f"para adicionar o assistente ao {callback_query.message.chat.title}.",
                        show_alert=True,
                    )
                else:
                    return await callback_query.message.reply_text(
                        f"Falha ao convidar o assistente para {callback_query.message.chat.title}.\n\n<b>Motivo:</b> `{ex}`"
                    )
        if invitelink.startswith("https://t.me/+"):
            invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
        try:
            await userbot.join_chat(invitelink)
            await asyncio.sleep(2)
        except UserAlreadyParticipant:
            pass
        except InviteRequestSent:
            try:
                await app.approve_chat_join_request(
                    callback_query.message.chat.id, userbot.id
                )
            except Exception as e:
                if "messages.HideChatJoinRequest" in str(e):
                    return await callback_query.answer(
                        f"Não tenho permissão para convidar usuários por link para adicionar o assistente ao {callback_query.message.chat.title}.",
                        show_alert=True,
                    )
                else:
                    return await callback_query.message.reply_text(
                        f"Falha ao convidar o assistente para {callback_query.message.chat.title}.\n\nMotivo: {e}"
                    )
        except Exception as ex:
            if "channels.JoinChannel" in str(ex) or "Username not found" in str(ex):
                return await callback_query.answer(
                    f"Não tenho permissão para convidar usuários por link para adicionar o assistente ao {callback_query.message.chat.title}.",
                    show_alert=True,
                )
            else:
                return await callback_query.message.reply_text(
                    f"Falha ao convidar o assistente para {callback_query.message.chat.title}.\n\nMotivo: {ex}"
                )

        try:
            await userbot.resolve_peer(invitelink)
        except:
            pass

    callback_data = callback_query.data.strip()
    mode = callback_data.split(None, 1)[1]
    user_id = callback_query.from_user.id
    _playlist = await get_playlist_names(user_id)
    if not _playlist:
        try:
            return await callback_query.answer(
                _["playlist_3"],
                show_alert=True,
            )
        except:
            return
    chat_id = callback_query.message.chat.id
    user_name = callback_query.from_user.first_name
    await callback_query.message.delete()
    result = []
    try:
        await callback_query.answer()
    except:
        pass
    video = True if mode == "v" else None
    mystic = await callback_query.message.reply_text(_["play_1"])
    for vidids in _playlist:
        result.append(vidids)
    try:
        await stream(
            _,
            mystic,
            user_id,
            result,
            chat_id,
            user_name,
            callback_query.message.chat.id,
            video,
            streamtype="playlist",
        )
    except Exception as e:
        ex_type = type(e).__name__
        err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
        return await mystic.edit_text(err)
    return await mystic.delete()


@app.on_message(
    filters.command(["playplaylist", "vplayplaylist"]) & ~BANNED_USERS & filters.group
)
@language_cb
async def play_playlist_command(client: app, message: Message, _):
    msg = await message.reply_text("Aguarde um momento...")
    try:
        try:
            userbot = await get_assistant(message.chat.id)
            get = await app.get_chat_member(message.chat.id, userbot.id)
        except ChatAdminRequired:
            return await msg.edit_text(
                f"Não tenho permissão para convidar usuários por link para adicionar o assistente {userbot.mention} ao {message.chat.title}."
            )
        if get.status == ChatMemberStatus.BANNED:
            return await msg.edit_text(
                text=f"O assistente {userbot.mention} está banido em {message.chat.title}\n\n𖢵 ID: `{userbot.id}`\n𖢵 Nome: {userbot.mention}\n𖢵 Nome de usuário: @{userbot.username}\n\nPor favor, remova o banimento do assistente e tente novamente..."
            )
    except UserNotParticipant:
        if message.chat.username:
            invitelink = message.chat.username
            try:
                await userbot.resolve_peer(invitelink)
            except Exception as ex:
                logging.exception(ex)
        else:
            try:
                invitelink = await client.export_chat_invite_link(message.chat.id)
            except ChatAdminRequired:
                return await msg.edit_text(
                    f"Não tenho permissão para convidar usuários por link para adicionar o assistente {userbot.mention} ao {message.chat.title}."
                )
            except InviteRequestSent:
                try:
                    await app.approve_chat_join_request(message.chat.id, userbot.id)
                except Exception as e:
                    return await msg.edit(
                        f"Falha ao convidar o assistente {userbot.mention} para {message.chat.title}.\n\n<b>Motivo:</b> `{e}`"
                    )
            except Exception as ex:
                if "channels.JoinChannel" in str(ex) or "Username not found" in str(ex):
                    return await msg.edit_text(
                        f"Não tenho permissão para convidar usuários por link para adicionar o assistente {userbot.mention} ao {message.chat.title}."
                    )
                else:
                    return await msg.edit_text(
                        f"Falha ao convidar o assistente {userbot.mention} para {message.chat.title}.\n\n<b>Motivo:</b> `{ex}`"
                    )
        if invitelink.startswith("https://t.me/+"):
            invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
        anon = await msg.edit_text(
            f"Por favor, aguarde...\n\nConvidando {userbot.mention} para {message.chat.title}."
        )
        try:
            await userbot.join_chat(invitelink)
            await asyncio.sleep(2)
            await msg.edit_text(
                f"{userbot.mention} entrou com sucesso,\n\niniciando transmissão..."
            )
        except UserAlreadyParticipant:
            pass
        except InviteRequestSent:
            try:
                await app.approve_chat_join_request(message.chat.id, userbot.id)
            except Exception as e:
                return await msg.edit(
                    f"Falha ao convidar o assistente {userbot.mention} para {message.chat.title}.\n\n<b>Motivo:</b> `{ex}`"
                )
        except Exception as ex:
            if "channels.JoinChannel" in str(ex) or "Username not found" in str(ex):
                return await msg.edit_text(
                    f"Não tenho permissão para convidar usuários por link para adicionar o assistente {userbot.mention} ao {message.chat.title}."
                )
            else:
                return await msg.edit_text(
                    f"Falha ao convidar o assistente {userbot.mention} para {message.chat.title}.\n\n<b>Motivo:</b> `{ex}`"
                )

        try:
            await userbot.resolve_peer(invitelink)
        except:
            pass
    await msg.delete()
    mode = message.command[0][0]
    user_id = message.from_user.id
    _playlist = await get_playlist_names(user_id)
    if not _playlist:
        try:
            return await message.reply(
                _["playlist_3"],
                quote=True,
            )
        except:
            return

    chat_id = message.chat.id
    user_name = message.from_user.first_name

    try:
        await message.delete()
    except:
        pass

    result = []
    video = True if mode == "v" else None
    mystic = await message.reply_text(_["play_1"])

    for vidids in _playlist:
        result.append(vidids)

    try:
        await stream(
            _,
            mystic,
            user_id,
            result,
            chat_id,
            user_name,
            message.chat.id,
            video,
            streamtype="playlist",
        )
    except Exception as e:
        ex_type = type(e).__name__
        err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
        return await mystic.edit_text(err)

    return await mystic.delete()


@app.on_callback_query(filters.regex("play_cplaylist") & ~BANNED_USERS)
@language_cb
async def play_playlist(_client: app, callback_query: CallbackQuery, _):
    callback_data = callback_query.data.strip()
    mode = callback_data.split(None, 1)[1]
    user_id = callback_query.from_user.id
    _playlist = await get_playlist_names(callback_query.message.chat.id)
    if not _playlist:
        try:
            return await callback_query.answer(
                _["playlist_19"],
                show_alert=True,
            )
        except:
            return
    chat_id = callback_query.message.chat.id
    user_name = callback_query.from_user.first_name
    await callback_query.message.delete()
    result = []
    try:
        await callback_query.answer()
    except:
        pass
    video = True if mode == "v" else None
    mystic = await callback_query.message.reply_text(_["play_1"])
    for vidids in _playlist:
        result.append(vidids)
    try:
        await stream(
            _,
            mystic,
            user_id,
            result,
            chat_id,
            user_name,
            callback_query.message.chat.id,
            video,
            streamtype="playlist",
        )
    except Exception as e:
        ex_type = type(e).__name__
        err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
        return await mystic.edit_text(err)
    return await mystic.delete()


@app.on_message(
    filters.command(["playgplaylist", "vplaygplaylist"]) & ~BANNED_USERS & filters.group
)
@language_cb
async def play_playlist_command(_client: app, message: Message, _):
    mode = message.command[0][0]
    user_id = message.from_user.id
    _playlist = await get_playlist_names(message.chat.id)
    if not _playlist:
        try:
            return await message.reply(
                _["playlist_3"],
                quote=True,
            )
        except:
            return

    chat_id = message.chat.id
    user_name = message.from_user.first_name

    try:
        await message.delete()
    except:
        pass

    result = []
    video = True if mode == "v" else None
    mystic = await message.reply_text(_["play_1"])

    for vidids in _playlist:
        result.append(vidids)

    try:
        await stream(
            _,
            mystic,
            user_id,
            result,
            chat_id,
            user_name,
            message.chat.id,
            video,
            streamtype="playlist",
        )
    except Exception as e:
        ex_type = type(e).__name__
        err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
        return await mystic.edit_text(err)

    return await mystic.delete()


@app.on_message(filters.command(["addplaylist"]) & ~BANNED_USERS)
@language
async def add_playlist(_client: app, message: Message, _):
    if len(message.command) < 2:
        return await message.reply_text(
            "<b>Por favor, me forneça um nome de música, um link de música ou um link de playlist do YouTube após o "
            "comando.</b>\n\n<b>Exemplos:</b>\n\n▷ `/addplaylist Ram siya ram` (insira o nome de uma música "
            "específica)\n\n▷ /addplaylist [link da playlist do YouTube] (para adicionar todas as músicas de uma "
            "playlist do YouTube à playlist do bot.)"
        )

    query = message.command[1]

    # Check if the provided input is a YouTube playlist link
    if "youtube.com/playlist" in query:
        adding = await message.reply_text(
            "<b>Adicionando músicas à playlist, por favor aguarde...</b>"
        )
        try:
            from pytube import Playlist, YouTube

            playlist = Playlist(query)
            video_urls = playlist.video_urls

        except Exception as e:
            return await message.reply_text(f"Error: {e}")

        if not video_urls:
            return await message.reply_text(
                "<b>Nenhuma música encontrada nos links da playlist.</b>\n\n<b>Tente outro link de playlist</b>"
            )

        user_id = message.from_user.id
        for video_url in video_urls:
            video_id = video_url.split("v=")[-1]

            try:
                yt = YouTube(video_url)
                title = yt.title
                duration = yt.length
            except Exception as e:
                return await message.reply_text(
                    f"Erro ao obter informações do vídeo: {e}"
                )

            plist = {
                "videoid": video_id,
                "title": title,
                "duration": duration,
            }

            await save_playlist(user_id, video_id, plist)

        keyboardes = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="๏ Deseja remover alguma música? ๏",
                        url=f"https://t.me/{app.username}?start=delplaylists",
                    ),
                ]
            ]
        )
        await adding.delete()
        return await message.reply_text(
            text="<b>Todas as músicas da sua playlist do YouTube foram adicionadas com sucesso!</b>\n\n<b>Para remover "
                 "alguma música, clique no botão abaixo.</b>",
            reply_markup=keyboardes,
        )
    if "youtube.com/@" in query:
        addin = await message.reply_text(
            "<b>Adicionando músicas à playlist, por favor aguarde...</b>"
        )
        try:
            from pytube import YouTube

            videos = YouTube_videos(f"{query}/videos")
            video_urls = [video["url"] for video in videos]

        except Exception as e:
            return await message.reply_text(f"Error: {e}")

        if not video_urls:
            return await message.reply_text(
                "<b>Nenhuma música encontrada no link da playlist.</b>\n\n<b>Tente outro link do YouTube</b>"
            )

        user_id = message.from_user.id
        for video_url in video_urls:
            video_id = query.split("/")[-1].split("?")[0]

            try:
                yt = YouTube(f"https://youtu.be/{video_id}")
                title = yt.title
                duration = yt.length
            except Exception as e:
                return await message.reply_text(
                    f"Erro ao buscar informações do vídeo: {e}"
                )

            plist = {
                "videoid": video_id,
                "title": title,
                "duration": duration,
            }

            await save_playlist(user_id, video_id, plist)
        keyboardes = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="๏ Deseja remover alguma música? ๏",
                        url=f"https://t.me/{app.username}?start=delplaylists",
                    ),
                ]
            ]
        )
        await addin.delete()
        return await message.reply_text(
            text="<b>Todas as músicas da sua playlist do YouTube foram adicionadas com sucesso!</b>\n\n<b>Para remover "
                 "alguma música, clique no botão abaixo.</b>",
            reply_markup=keyboardes,
        )
    # Check if the provided input is a YouTube video link
    if "https://youtu.be" in query:
        try:
            add = await message.reply_text(
                "<b>Adicionando músicas à playlist, por favor aguarde...</b>"
            )
            from pytube import Playlist, YouTube

            # Extract video ID from the YouTube lin
            videoid = query.split("/")[-1].split("?")[0]
            user_id = message.from_user.id
            thumbnail = f"https://img.youtube.com/vi/{videoid}/maxresdefault.jpg"
            _check = await get_playlist(user_id, videoid)
            if _check:
                try:
                    await add.delete()
                    return await message.reply_photo(thumbnail, caption=_["playlist_8"])
                except KeyError:
                    pass

            _count = await get_playlist_names(user_id)
            count = len(_count)
            if count == SERVER_PLAYLIST_LIMIT:
                try:
                    return await message.reply_text(
                        _["playlist_9"].format(SERVER_PLAYLIST_LIMIT)
                    )
                except KeyError:
                    pass

            try:
                yt = YouTube(f"https://youtu.be/{videoid}")
                title = yt.title
                duration = yt.length
                thumbnail = f"https://img.youtube.com/vi/{videoid}/maxresdefault.jpg"
                plist = {
                    "videoid": videoid,
                    "title": title,
                    "duration": duration,
                }
                await save_playlist(user_id, videoid, plist)

                await add.delete()
                await message.reply_photo(
                    thumbnail, caption="<b>Música adicionada à sua playlist do bot</b>"
                )
            except Exception as e:
                print(f"Error: {e}")
                await message.reply_text(str(e))
        except Exception as e:
            return await message.reply_text(str(e))
    else:
        from CineWinx import YouTube

        # Add a specific song by name
        query = " ".join(message.command[1:])
        print(query)

        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            link = f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]["title"][:40]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f"{title}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, "wb").write(thumb.content)
            duration = results[0]["duration"]
            videoid = results[0]["id"]
            # Add these lines to define views and channel_name
            results[0]["views"]
            results[0]["channel"]

            user_id = message.from_user.id
            _check = await get_playlist(user_id, videoid)
            if _check:
                try:
                    return await message.reply_photo(thumbnail, caption=_["playlist_8"])
                except KeyError:
                    pass

            _count = await get_playlist_names(user_id)
            count = len(_count)
            if count == SERVER_PLAYLIST_LIMIT:
                try:
                    return await message.reply_text(
                        _["playlist_9"].format(SERVER_PLAYLIST_LIMIT)
                    )
                except KeyError:
                    pass

            m = await message.reply("<b>Adicionando, por favor aguarde...</b>")
            title, duration_min, _, _, _ = await YouTube.details(videoid, True)
            title = (title[:50]).title()
            plist = {
                "videoid": videoid,
                "title": title,
                "duration": duration_min,
            }

            await save_playlist(user_id, videoid, plist)
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "๏ Remover da playlist ๏",
                            callback_data=f"remove_playlist {videoid}",
                        )
                    ]
                ]
            )

            await m.delete()
            await message.reply_photo(
                thumbnail,
                caption="<b>Música adicionada à sua playlist do bot</b>",
                reply_markup=keyboard,
            )

        except KeyError:
            return await message.reply_text("<b>Formato de data inválido.</b>")
        except Exception:
            pass


@app.on_callback_query(filters.regex("remove_playlist") & ~BANNED_USERS)
@language_cb
async def del_plist(_client: app, callback_query: CallbackQuery, _):
    callback_data = callback_query.data.strip()
    videoid = callback_data.split(None, 1)[1]
    callback_query.from_user.id
    deleted = await delete_playlist(callback_query.from_user.id, videoid)
    if deleted:
        try:
            await callback_query.answer(_["playlist_11"], show_alert=True)
        except:
            pass
    else:
        try:
            return await callback_query.answer(_["playlist_12"], show_alert=True)
        except:
            return
    keyboards = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "๏ Recuperar sua música ๏",
                    callback_data=f"recover_playlist {videoid}",
                )
            ]
        ]
    )
    return await callback_query.edit_message_text(
        text="<b>Sua música foi removida da sua playlist do bot</b>\n\n<b>"
             "Para recuperar sua música na playlist, clique no botão abaixo.</b>",
        reply_markup=keyboards,
    )


@app.on_callback_query(filters.regex("recover_playlist") & ~BANNED_USERS)
@language_cb
async def add_playlist(_client: app, callback_query: CallbackQuery, _):
    from CineWinx import YouTube

    callback_data = callback_query.data.strip()
    videoid = callback_data.split(None, 1)[1]
    user_id = callback_query.from_user.id
    _check = await get_playlist(user_id, videoid)
    if _check:
        try:
            return await callback_query.answer(_["playlist_8"], show_alert=True)
        except:
            return
    _count = await get_playlist_names(user_id)
    count = len(_count)
    if count == SERVER_PLAYLIST_LIMIT:
        try:
            return await callback_query.answer(
                _["playlist_9"].format(SERVER_PLAYLIST_LIMIT),
                show_alert=True,
            )
        except:
            return
    (
        title,
        duration_min,
        duration_sec,
        thumbnail,
        vidid,
    ) = await YouTube.details(videoid, True)
    title = (title[:50]).title()
    plist = {
        "videoid": vidid,
        "title": title,
        "duration": duration_min,
    }
    await save_playlist(user_id, videoid, plist)
    try:
        title = (title[:30]).title()
        return await callback_query.edit_message_text(
            text="<b>Música recuperada na sua playlist</b>",
        )
    except:
        return


@app.on_callback_query(filters.regex("remove_playlist") & ~BANNED_USERS)
@language_cb
async def del_plist(_client: app, callback_query: CallbackQuery, _):
    callback_data = callback_query.data.strip()
    videoid = callback_data.split(None, 1)[1]
    callback_query.from_user.id
    deleted = await delete_playlist(callback_query.from_user.id, videoid)
    if deleted:
        try:
            await callback_query.answer(_["playlist_11"], show_alert=True)
        except:
            pass
    else:
        try:
            return await callback_query.answer(_["playlist_12"], show_alert=True)
        except:
            return

    return await callback_query.edit_message_text(
        text="<b>Sua música foi removida da sua playlist do bot</b>"
    )


@app.on_callback_query(filters.regex("add_playlist") & ~BANNED_USERS)
@language_cb
async def add_playlist(_client: app, callback_query: CallbackQuery, _):
    try:
        from CineWinx import YouTube
    except ImportError as e:
        print(f"ERROR {e}")
        return

    callback_data = callback_query.data.strip()
    videoid = callback_data.split(None, 1)[1]
    user_id = callback_query.from_user.id
    _check = await get_playlist(user_id, videoid)
    if _check:
        try:
            return await callback_query.answer(_["playlist_8"], show_alert=True)
        except:
            return
    _count = await get_playlist_names(user_id)
    count = len(_count)
    if count == SERVER_PLAYLIST_LIMIT:
        try:
            return await callback_query.answer(
                _["playlist_9"].format(SERVER_PLAYLIST_LIMIT),
                show_alert=True,
            )
        except:
            return
    (
        title,
        duration_min,
        duration_sec,
        thumbnail,
        vidid,
    ) = await YouTube.details(videoid, True)
    title = (title[:50]).title()
    plist = {
        "videoid": vidid,
        "title": title,
        "duration": duration_min,
    }
    await save_playlist(user_id, videoid, plist)
    try:
        title = (title[:30]).title()
        return await callback_query.answer(
            _["playlist_10"].format(title), show_alert=True
        )
    except:
        return


@app.on_callback_query(filters.regex("group_addplaylist") & ~BANNED_USERS)
@language_cb
async def add_playlist(_client: app, callback_query: CallbackQuery, _):
    try:
        from CineWinx import YouTube
    except ImportError as e:
        print(f"ERROR {e}")
        return

    callback_data = callback_query.data.strip()
    videoid = callback_data.split(None, 1)[1]
    user_id = callback_query.from_user.id
    _check = await get_playlist(callback_query.message.chat.id, videoid)
    if _check:
        try:
            return await callback_query.answer(
                "Já existe\n\nEsta faixa já existe na playlist do grupo.",
                show_alert=True,
            )
        except:
            return
    _count = await get_playlist_names(callback_query.message.chat.id)
    count = len(_count)
    if count == SERVER_PLAYLIST_LIMIT:
        try:
            return await callback_query.answer(
                _["playlist_9"].format(SERVER_PLAYLIST_LIMIT),
                show_alert=True,
            )
        except:
            return
    (
        title,
        duration_min,
        duration_sec,
        thumbnail,
        vidid,
    ) = await YouTube.details(videoid, True)
    title = (title[:50]).title()
    plist = {
        "videoid": vidid,
        "title": title,
        "duration": duration_min,
    }
    await save_playlist(callback_query.message.chat.id, videoid, plist)
    try:
        title = (title[:30]).title()
        return await callback_query.answer(
            _["playlist_10"].format(title), show_alert=True
        )
    except:
        return


@app.on_callback_query(filters.regex("del_playlist") & ~BANNED_USERS)
@language_cb
async def del_plist(_client: app, callback_query: CallbackQuery, _):
    pass

    callback_data = callback_query.data.strip()
    videoid = callback_data.split(None, 1)[1]
    user_id = callback_query.from_user.id
    deleted = await delete_playlist(callback_query.from_user.id, videoid)
    if deleted:
        try:
            await callback_query.answer(_["playlist_11"], show_alert=True)
        except:
            pass
    else:
        try:
            return await callback_query.answer(_["playlist_12"], show_alert=True)
        except:
            return
    keyboard, count = await get_keyboard(_, user_id)
    return await callback_query.edit_message_reply_markup(reply_markup=keyboard)


@app.on_callback_query(filters.regex("del_cplaylist") & ~BANNED_USERS)
@language_cb
async def del_plist(_client: app, callback_query: CallbackQuery, _):
    pass

    callback_data = callback_query.data.strip()
    videoid = callback_data.split(None, 1)[1]
    user_id = callback_query.from_user.id
    deleted = await delete_playlist(callback_query.message.chat.id, videoid)
    if deleted:
        try:
            await callback_query.answer(_["playlist_11"], show_alert=True)
        except:
            pass
    else:
        try:
            return await callback_query.answer(_["playlist_12"], show_alert=True)
        except:
            return
    keyboard, count = await get_keyboard(_, callback_query.message.chat.id)
    return await callback_query.edit_message_reply_markup(reply_markup=keyboard)


@app.on_callback_query(filters.regex("delete_whole_playlist") & ~BANNED_USERS)
@language_cb
async def del_whole_playlist(_client: app, callback_query: CallbackQuery, _):
    pass

    _playlist = await get_playlist_names(callback_query.from_user.id)
    for x in _playlist:
        await callback_query.answer(
            "Por favor, aguarde.\nExcluindo sua playlist...", show_alert=True
        )
        await delete_playlist(callback_query.from_user.id, x)
    return await callback_query.edit_message_text(_["playlist_13"])


@app.on_callback_query(filters.regex("get_cplaylist_playmode") & ~BANNED_USERS)
@app.on_callback_query(filters.regex("get_playlist_playmode") & ~BANNED_USERS)
@language_cb
async def get_playlist_playmode_(_client: app, callback_query: CallbackQuery, _):
    try:
        await callback_query.answer()
    except:
        pass
    if callback_query.data.startswith("get_playlist_playmode"):
        buttons = get_playlist_markup(_)
        return await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    if callback_query.data.startswith("get_cplaylist_playmode"):
        buttons = get_cplaylist_markup(_)
        return await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )


@app.on_callback_query(filters.regex("delete_warning") & ~BANNED_USERS)
@language_cb
async def delete_warning_message(_client: app, callback_query: CallbackQuery, _):
    pass

    try:
        await callback_query.answer()
    except:
        pass
    upl = warning_markup(_)
    return await callback_query.edit_message_text(_["playlist_14"], reply_markup=upl)


@app.on_callback_query(filters.regex("home_play") & ~BANNED_USERS)
@language_cb
async def home_play_(_client: app, callback_query: CallbackQuery, _):
    pass

    try:
        await callback_query.answer()
    except:
        pass
    buttons = botplaylist_markup(_)
    return await callback_query.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex("del_back_playlist") & ~BANNED_USERS)
@language_cb
async def del_back_playlist(_client: app, callback_query: CallbackQuery, _):
    pass

    user_id = callback_query.from_user.id
    _playlist = await get_playlist_names(user_id)
    if _playlist:
        try:
            await callback_query.answer(_["playlist_2"], show_alert=True)
        except:
            pass
    else:
        try:
            return await callback_query.answer(_["playlist_3"], show_alert=True)
        except:
            return
    keyboard, count = await get_keyboard(_, user_id)
    return await callback_query.edit_message_text(
        _["playlist_7"].format(count), reply_markup=keyboard
    )


__MODULE__ = "Playlist"
__HELP__ = """❀ Funcionalidades de Playlist para você:
/playlist - Verifique sua playlist salva nos servidores.
/delplaylist - Exclua qualquer música salva em sua playlist.
/play - Comece a reproduzir sua playlist salva dos servidores.
/playplaylist - Comece a reproduzir diretamente sua playlist salva dos servidores [apenas áudio, sem vídeo].

/vplayplaylist - Comece a reproduzir diretamente sua playlist salva dos servidores [áudio com vídeo].
/addplaylist - [link do vídeo do YouTube] ou [link da playlist do YouTube] ou [nome da música] para adicionar à sua playlist do bot."""
