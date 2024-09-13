import logging

import asyncio
from pyrogram import filters, Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    UserNotParticipant,
    InviteRequestSent,
    UserAlreadyParticipant,
)
from pyrogram.types import Message

from CineWinx import app, ZenoFM
from CineWinx.utils import (
    get_assistant,
)
from config import PREFIXES, BANNED_USERS
from strings import get_command

RADIO_COMMAND = get_command("RADIO_COMMAND")


RADIO_STATION = {
    # "Air Bilaspur": "http://air.pc.cdn.bitgravity.com/air/live/pbaudio110/playlist.m3u8",
    # "Air Raipur": "http://air.pc.cdn.bitgravity.com/air/live/pbaudio118/playlist.m3u8",
    # "Capital FM": "http://media-ice.musicradio.com/CapitalMP3?.mp3&listening-from-radio-garden=1616312105154",
    # "English": "https://hls-01-regions.emgsound.ru/11_msk/playlist.m3u8",
    # "Mirchi": "http://peridot.streamguys.com:7150/Mirchi",
    "galaxie": "http://stream.zenolive.com/ifp2nmjjwojuv",
    "Hits Of Kishore Kumar": "http://stream.zenolive.com/0ghtfp8ztm0uv",
    "Jovem Pan FM": "http://stream.zenolive.com/c45wbq2us3buv",
    "Dance Wave!": "http://stream.zenolive.com/867h0na557zuv",
    "ChillSynth FM": "https://www.youtube.com/watch?v=UedTcufyrHc",
    "METAL 24/7 ": "https://www.youtube.com/watch?v=lCjVa1c5zKw",
    "Chill Radio 24/7": "https://www.youtube.com/watch?v=Ndx2zSuAaRQ",
}

valid_stations = "\n".join(
    [f"<code>{name}</code>" for name in sorted(RADIO_STATION.keys())]
)


@app.on_message(
    filters.command(RADIO_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS
)
async def radio_command(client: Client, message: Message):

    msg = await message.reply_text("⏳ 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗮𝗴𝘂𝗮𝗿𝗱𝗲 𝘂𝗺 𝗺𝗼𝗺𝗲𝗻𝘁𝗼....")

    userbot = await get_assistant(message.chat.id)
    try:
        try:
            get = await app.get_chat_member(message.chat.id, userbot.id)
        except ChatAdminRequired:
            return await msg.edit_text(
                f"𝗡𝗮̃𝗼 𝘁𝗲𝗻𝗵𝗼 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗽𝗮𝗿𝗮 𝗶𝗻𝘃𝗶𝘁𝗮𝗿 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗽𝗼𝗿 𝗹𝗶𝗻𝗸 𝗽𝗮𝗿𝗮 𝗰𝗼𝗻𝘃𝗶𝗱𝗮𝗿 {userbot.mention} 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗽𝗮𝗿𝗮 {message.chat.title}."
            )
        if get.status == ChatMemberStatus.BANNED:
            return await msg.edit_text(
                text=f"{userbot.mention} 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗲𝘀𝘁𝗮́ 𝗯𝗮𝗻𝗶𝗱𝗼 𝗲𝗺 {message.chat.title}\n\n🚫 𝗜𝗗: {userbot.id}\n🆔 𝗡𝗼𝗺𝗲: {userbot.mention}\n👤 𝗨𝘀𝘂𝗮́𝗿𝗶𝗼: @{userbot.username}\n\n𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗱𝗲𝘀𝗯𝗮𝗻𝗲 𝗼 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗲 𝘁𝗲𝗻𝘁𝗲 𝗻𝗼𝘃𝗮𝗺𝗲𝗻𝘁𝗲..."
            )
    except UserNotParticipant:
        if message.chat.username:
            invite_link = message.chat.username
            try:
                await userbot.resolve_peer(invite_link)
            except Exception as ex:
                logging.exception(ex)
        else:
            try:
                invite_link = await client.export_chat_invite_link(message.chat.id)
            except ChatAdminRequired:
                return await msg.edit_text(
                    f"🚫 𝗡𝗮̃𝗼 𝘁𝗲𝗻𝗵𝗼 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗽𝗮𝗿𝗮 𝗶𝗻𝘃𝗶𝘁𝗮𝗿 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗽𝗼𝗿 𝗹𝗶𝗻𝗸 𝗽𝗮𝗿𝗮 𝗰𝗼𝗻𝘃𝗶𝗱𝗮𝗿 {userbot.mention} 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗽𝗮𝗿𝗮 {message.chat.title}."
                )
            except InviteRequestSent:
                try:
                    await app.approve_chat_join_request(message.chat.id, userbot.id)
                except Exception as e:
                    logging.exception(e)
                    return await msg.edit(
                        f"𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗶𝗻𝘃𝗶𝘁𝗮𝗿 {userbot.mention} 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗽𝗮𝗿𝗮 {message.chat.title}.\n\n𝗠𝗼𝘁𝗶𝘃𝗼:{e}` ❌"
                    )
            except Exception as ex:
                if "channels.JoinChannel" in str(ex) or "Username not found" in str(ex):
                    return await msg.edit_text(
                        f"𝗡𝗮̃𝗼 𝘁𝗲𝗻𝗵𝗼 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗽𝗮𝗿𝗮 𝗶𝗻𝘃𝗶𝘁𝗮𝗿 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗽𝗼𝗿 𝗹𝗶𝗻𝗸 𝗽𝗮𝗿𝗮 𝗶𝗻𝘃𝗶𝘁𝗮𝗿 {userbot.mention} 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗽𝗮𝗿𝗮 {message.chat.title}. ❌"
                    )
                else:
                    return await msg.edit_text(
                        f"𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗶𝗻𝘃𝗶𝘁𝗮𝗿 {userbot.mention} 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗽𝗮𝗿𝗮 {message.chat.title}.\n\n𝗠𝗼𝘁𝗶𝘃𝗼: {ex} ⚠️"
                    )
        if invite_link.startswith("https://t.me/+"):
            invite_link = invite_link.replace(
                "https://t.me/+", "https://t.me/joinchat/"
            )
        anon = await msg.edit_text(
            f"⏳ 𝗣𝗼𝗿 𝗳𝗮𝘃𝗼𝗿, 𝗮𝗴𝘂𝗮𝗿𝗱𝗲...\n\n𝗜𝗻𝘃𝗶𝘁𝗮𝗻𝗱𝗼 {userbot.mention} 𝗽𝗮𝗿𝗮 {message.chat.title}."
        )
        try:
            await userbot.join_chat(invite_link)
            await asyncio.sleep(2)
            await msg.edit_text(
                f"{userbot.mention} 𝗲𝗻𝘁𝗿𝗼𝘂 𝗰𝗼𝗺 𝘀𝘂𝗰𝗲𝘀𝘀𝗼,\n\n𝗶𝗻𝗶𝗰𝗶𝗮𝗻𝗱𝗼 𝗮 𝘁𝗿𝗮𝗻𝘀𝗺𝗶𝘀𝘀𝗮̃𝗼... 🎶"
            )
        except UserAlreadyParticipant:
            pass
        except InviteRequestSent:
            try:
                await app.approve_chat_join_request(message.chat.id, userbot.id)
            except Exception as e:
                logging.exception(e)
                return await msg.edit_text(
                    f"𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗶𝗻𝘃𝗶𝘁𝗮𝗿 {userbot.mention} 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗽𝗮𝗿𝗮 {message.chat.title}.\n\n𝗠𝗼𝘁𝗶𝘃𝗼: {e} ⚠️"
                )
        except Exception as ex:
            if "channels.JoinChannel" in str(ex) or "Username not found" in str(ex):
                return await msg.edit_text(
                    f"𝗡𝗮̃𝗼 𝘁𝗲𝗻𝗵𝗼 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗮̃𝗼 𝗽𝗮𝗿𝗮 𝗶𝗻𝘃𝗶𝘁𝗮𝗿 𝘂𝘀𝘂𝗮́𝗿𝗶𝗼𝘀 𝗽𝗼𝗿 𝗹𝗶𝗻𝗸 𝗽𝗮𝗿𝗮 𝗶𝗻𝘃𝗶𝘁𝗮𝗿 {userbot.mention} 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗽𝗮𝗿𝗮 {message.chat.title}. ❌"
                )
            else:
                return await msg.edit_text(
                    f"𝗙𝗮𝗹𝗵𝗮 𝗮𝗼 𝗶𝗻𝘃𝗶𝘁𝗮𝗿 {userbot.mention} 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗽𝗮𝗿𝗮 {message.chat.title}.\n\n𝗠𝗼𝘁𝗶𝘃𝗼: {ex} ⚠️"
                )

        try:
            await userbot.resolve_peer(invite_link)
        except BaseException as e:
            logging.exception(e)
    await msg.delete()

    RADIO_STATION = await ZenoFM.get_radio_stations()

    await message.reply(f"📻 𝗦𝗲𝗹𝗲𝗰𝗶𝗼𝗻𝗲 𝘂𝗺𝗮 𝗿𝗮́𝗱𝗶𝗼", reply_markup=RADIO_STATION)

    # station_name = " ".join(message.command[1:])
    # RADIO_URL = RADIO_STATION.get(station_name)
    # if RADIO_URL:
    #     language = await get_lang(message.chat.id)
    #     _ = get_string(language)
    #     playmode = await get_playmode(message.chat.id)
    #     playty = await get_playtype(message.chat.id)
    #     if playty != "Everyone":
    #         if message.from_user.id not in SUDOERS:
    #             admins = adminlist.get(message.chat.id)
    #             if not admins:
    #                 return await message.reply_text(_["admin_18"])
    #             else:
    #                 if message.from_user.id not in admins:
    #                     return await message.reply_text(_["play_4"])
    #     if message.command[0][0] == "c":
    #         chat_id = await get_cmode(message.chat.id)
    #         if chat_id is None:
    #             return await message.reply_text(_["setting_12"])
    #         try:
    #             chat = await app.get_chat(chat_id)
    #         except BaseException as e:
    #             logging.exception(e)
    #             return await message.reply_text(_["cplay_4"])
    #         channel = chat.title
    #     else:
    #         chat_id = message.chat.id
    #         channel = None
    #
    #     video = None
    #     mystic = await message.reply_text(
    #         _["play_2"].format(channel) if channel else _["play_1"]
    #     )
    #     try:
    #         await stream(
    #             _,
    #             mystic,
    #             message.from_user.id,
    #             RADIO_URL,
    #             chat_id,
    #             message.from_user.mention,
    #             message.chat.id,
    #             video=video,
    #             stream_type="index",
    #         )
    #     except Exception as e:
    #         ex_type = type(e).__name__
    #         err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
    #         return await mystic.edit_text(err)
    #     return await play_logs(message, stream_type="M3u8 or Index Link")
    # else:
    #     await message.reply(
    #         f"📻 𝗗𝗶𝗳𝗶𝘁𝗲 𝘂𝗺 𝗻𝗼𝗺𝗲 𝗱𝗲 𝗲𝘀𝘁𝗮𝗰̧𝗮̃𝗼 𝗽𝗮𝗿𝗮 𝘁𝗼𝗰𝗮𝗿 𝗿𝗮́𝗱𝗶𝗼.\n📋 𝗔𝗯𝗮𝗶𝘅𝗼 𝗲𝘀𝘁𝗮̃𝗼 𝗮𝗹𝗴𝘂𝗻𝘀 𝗻𝗼𝗺𝗲𝘀 𝗱𝗲 𝗲𝘀𝘁𝗮𝗰̧𝗼̃𝗲𝘀:\n{valid_stations}"
    #     )


# [
#     {
#         "url": "https://zeno.fm/radio/melodias-e-momentos/",
#         "name": "Melodias e Momentos",
#         "logo": "https://images.zeno.fm/u7AUniEh6DuhR7kDHtfL56C7u86f62XEr37wRQDSZdg/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zLzcwNzYwNDkxLTU0ZTEtNDAzYS04OThiLTc1NGE2ZWM5Mzg4NS9pbWFnZS8_dXBkYXRlZD0xNzIxODQyNTkxMDAwP3U9NTc1MTEwOQ.webp",
#         "featured": true,
#         "sponsored": true
#     },
#     {
#         "url": "https://zeno.fm/radio/groupe-medialternatif-haiti/",
#         "name": "Groupe Medialternatif - Haiti",
#         "logo": "https://images.zeno.fm/JnYp8CgK3vAjn5hwqQ32WhhaFnMhQshbvf0F6I85pKY/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSUNBb0t5T21na01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSURJdVlHLXdRc01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2NjAyNTA0NzAwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": true
#     },
#     {
#         "url": "https://zeno.fm/radio/radio-buteco-sertanejo/",
#         "name": "Radio Buteco Sertanejo",
#         "logo": "https://images.zeno.fm/Y6LMJnlACVswrA4b-ny-lSeUz5ALokFqbYXfNbDxuxE/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSUNnNV96cnBnc01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSUNnbDh5UHJ3c01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE3MTQ2OTYwNDUwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/amado-batista/",
#         "name": "Rádio Amado Batista",
#         "logo": "https://images.zeno.fm/0lKsmbs8Yg5y3JjImuPPpylH68a-SbACNFB-utm6VB8/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSUNnbmRMWHZBb01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSURnMGRiRWdBc01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2OTUyMjE5ODIwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/sertaneja-fm/",
#         "name": "SERTANEJA FM",
#         "logo": "https://images.zeno.fm/ilVwr34MrGWVbU4YjYq3ZOMT8qoaj-l3muKSPBTdqus/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSURnajZQMHdBa01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSURnOThEcmtRc01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE3MTU4NDUzNTYwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/sertanejo-fm-alta-qualidade/",
#         "name": "Sertanejo FM - Alta qualidade",
#         "logo": "https://images.zeno.fm/EGgdxtOurk-R9Qkmj5hlXole0ERWc1KH5li_a33Gps8/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSURRcGRxWW93c01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSUR3d2V5UjFna01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE3MDQxNDkwNzkwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/tempofm1039/",
#         "name": "Tempo Fm 103.9",
#         "logo": "https://images.zeno.fm/UtCLsFQD1EhJcbq7uzIztztzHJ5D2pgTibeXfuZc530/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSURRLXJPbjVRb01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSURReHJpaW1Rb01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2NjA4NTY0NDUwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/ForroDasAntigas/",
#         "name": "Rádio Forró  Das Antigas",
#         "logo": "https://images.zeno.fm/cUGI-cqliVjtqQs8IFkQGo2ZbPKxag8gz4BrtrSr5YQ/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSURndDRiVHBBa01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSURndDhYeHp3b01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2NjExMjMwMTEwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/bobmarley/",
#         "name": "MARLEY",
#         "logo": "https://images.zeno.fm/vZJvNo9i5XhWUZLgucg7-tX_vAXBsokskNIxPNCgfAk/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSURnek91SHlBb01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSURJeEl5cTNBZ01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE3MDg1NjAxNjEwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/radio-carro-de-boi/",
#         "name": "Radio Carro de Boi",
#         "logo": "https://images.zeno.fm/skABB3iIk5xBwe8KnRU3bUAQeYokzm_oV7VGt3NwGXE/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSUN3aHJuZi1Rc01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSUN3N3JTT3lna01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2ODcyNzUzOTMwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/flashdance90/",
#         "name": "FLASH  DANCE  90",
#         "logo": "https://images.zeno.fm/V6si6afg7KTH4Rdp7IVAlMvXm0C8TpFiuXcbFAZon6k/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSURnek91SHlBb01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSUNRZ09PcHlRZ01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE3MDg1NjAxMDMwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/mega-radio-pagode/",
#         "name": "Mega Radio Pagode",
#         "logo": "https://images.zeno.fm/Zimf0DaD2qEUpqDvaBljZqNQ67-wAdHqPcb9e7lZCVY/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSUNndTd1Z25nZ01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSUNncDRIVXlnc01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2ODYwODYwOTMwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/brega-show-2/",
#         "name": "Rádio Brega Fm",
#         "logo": "https://images.zeno.fm/ubD9ph34AmLqOVqhWI7W1DdIDo1MIs147c8zDMUYSj0/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSUNnbmRMWHZBb01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSURndl91bWdRa01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2ODE3ODE3MzYwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/mega-radio-love/",
#         "name": "Mega Radio Love",
#         "logo": "https://images.zeno.fm/ERsxNDhUoOb6_dNxMkn7mOQCQRxkknXXID5Mr8TmJrg/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSUNndTd1Z25nZ01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSURnNUo3T2lBc01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2ODY3OTgyMjEwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/a-voz-do-gueto/",
#         "name": "Radio Rap a Voz do Gueto",
#         "logo": "https://images.zeno.fm/8MvG6qEwXCha5MY48OVUP6yAVfGglUSdMAK6mpZH6FQ/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSUNnLXNESzdBa01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSUNnLXNENzdnZ01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2NjExNTc3OTEwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/lancamentos-sofrenejo/",
#         "name": "Lançamentos - Sertanejo e Sofrência",
#         "logo": "https://images.zeno.fm/YkAoyTxbKFa6pcnwqF-xTLWkDR8_6ExNMXTuMklYjXA/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSUNnb3RPY3d3Z01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSUNRNGNqNnJRZ01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2NjE2NTQxMTIwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/radio-musica-das-antigas/",
#         "name": "Radio Musica das Antigas",
#         "logo": "https://images.zeno.fm/gUStAZywORyUwzzKVmIQIcG2fYHREI217aId5iD-VHo/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSUNRNl9HVHZBZ01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSUNRNi1lN2xRc01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2NjEzNjA3NDYwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/funk-brasil/",
#         "name": "FUNK BRASIL",
#         "logo": "https://images.zeno.fm/_cZGtqiu2_s9ah3wLL-j5EkgoPLC4cB2iM5UADFDWZw/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSUNnNHZYYXV3Z01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSUNnN3Z6WXJRZ01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2NjE1MDc4NDUwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/jolimpb/",
#         "name": "Joli MPB",
#         "logo": "https://images.zeno.fm/MTY2yml4yf79pCq29yNDDUJeGOGUJyTOQ7FVH8ycxdY/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSUNnNnNiSTFRc01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSUNnbHZ5ZGlBZ01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2NjE3MjQzNjIwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/radio-rock-fm/",
#         "name": "Radio Rock FM",
#         "logo": "https://images.zeno.fm/XfZDKfLMvSlEGL76kymLWvlolbtVaYemvSFcXfVZXPY/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSURBdGZhcy1nb01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSUNBZ0lEeWlBb01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2NzA4MDA0NjQwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/rapsul/",
#         "name": "RAP SUL",
#         "logo": "https://images.zeno.fm/WbtTc3FJkwIhP62v07SqVXJ6L57Gi_rPCjt2dpgWWzc/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSURnLTd1VnRBc01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSURnaF9ISnd3a01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2NjE3MTkwNjMwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/conexaojamaica/",
#         "name": "CONEXÃO JAMAICA",
#         "logo": "https://images.zeno.fm/1Cg6DNE0gK-qakOZ8yudhKkYL-BNW0fVa8_EwmH7lZs/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSURndnNydzJRa01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSUNRMVlQNmpRb01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE3MTEzNDEyNjYwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/forro-das-antigas/",
#         "name": "Radio forró das antigas",
#         "logo": "https://images.zeno.fm/JZlu5amD0lgOLpUyaVGSF0uC4mCnu8AqSvIkvfalV00/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSURBd2NxVDN3c01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSUNnOWRIRzV3b01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE2ODUwMzUxMjYwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     },
#     {
#         "url": "https://zeno.fm/radio/mega-radio-sertanejo/",
#         "name": "Mega Radio Sertanejo",
#         "logo": "https://images.zeno.fm/mQtflodMwj2cyBFiTVTS3XP-3F7DXTX4FvYGuF6Qud4/rs:fit:268:268/g:ce:0:0/aHR0cHM6Ly9zdHJlYW0tdG9vbHMuemVub21lZGlhLmNvbS9jb250ZW50L3N0YXRpb25zL2FneHpmbnBsYm04dGMzUmhkSE55TWdzU0NrRjFkR2hEYkdsbGJuUVlnSUNndTd1Z25nZ01DeElPVTNSaGRHbHZibEJ5YjJacGJHVVlnSURnaE4tOWtBb01vZ0VFZW1WdWJ3L2ltYWdlLz91cGRhdGVkPTE3MTk4NDYxOTUwMDA_dT01NzUxMTA5.webp",
#         "featured": false,
#         "sponsored": false
#     }
# ]


def radio_station_markup(user_id: int, stations: list, page: int = 0):
    pass
