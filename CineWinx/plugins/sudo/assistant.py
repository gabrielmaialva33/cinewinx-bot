import os
from inspect import getfullargspec

from pyrogram import filters
from pyrogram.types import Message

from CineWinx import app
from CineWinx.misc import SUDOERS
from CineWinx.utils.database import get_client


@app.on_message(filters.command("setpfp", prefixes=".") & SUDOERS)
async def set_pfp(_client: app, message: Message):
    from CineWinx.core.userbot import assistants

    if not message.reply_to_message or not message.reply_to_message.photo:
        return await eor(message, text="Reply to a photo")
    for num in assistants:
        client = await get_client(num)
        photo = await message.reply_to_message.download()
        try:
            await client.set_profile_photo(photo=photo)
            await eor(message, text="Successfully Changed PFP.")
            os.remove(photo)
        except Exception as e:
            await eor(message, text=e)
            os.remove(photo)


@app.on_message(filters.command("setbio", prefixes=".") & SUDOERS)
async def set_bio(client: app, message: Message):
    from CineWinx.core.userbot import assistants

    if len(message.command) == 1:
        return await eor(message, text="Give some text to set as bio.")
    elif len(message.command) > 1:
        for num in assistants:
            client = await get_client(num)
            bio = message.text.split(None, 1)[1]
        try:
            await client.update_profile(bio=bio)
            await eor(message, text="Changed Bio.")
        except Exception as e:
            await eor(message, text=e)
    else:
        return await eor(message, text="Give some text to set as bio.")


@app.on_message(filters.command("setname", prefixes=".") & SUDOERS)
async def set_name(client: app, message: Message):
    from CineWinx.core.userbot import assistants

    if len(message.command) == 1:
        return await eor(message, text="Give some text to set as name.")
    elif len(message.command) > 1:
        for num in assistants:
            client = await get_client(num)
            name = message.text.split(None, 1)[1]
        try:
            await client.update_profile(first_name=name)
            await eor(message, text=f"name Changed to {name} .")
        except Exception as e:
            await eor(message, text=e)
    else:
        return await eor(message, text="Give some text to set as name.")


@app.on_message(filters.command("delpfp", prefixes=".") & SUDOERS)
async def del_pfp(_client: app, message: Message):
    from CineWinx.core.userbot import assistants

    for num in assistants:
        client = await get_client(num)
        photos = [p async for p in client.get_chat_photos("me")]
        try:
            if photos:
                await client.delete_profile_photos(photos[0].file_id)
                await eor(message, text="Successfully deleted photo")
            else:
                await eor(message, text="No profile photos found.")
        except Exception as e:
            await eor(message, text=e)


@app.on_message(filters.command("delallpfp", prefixes=".") & SUDOERS)
async def delall_pfp(_client: app, message: Message):
    from CineWinx.core.userbot import assistants

    for num in assistants:
        client = await get_client(num)
        photos = [p async for p in client.get_chat_photos("me")]
        try:
            if photos:
                await client.delete_profile_photos([p.file_id for p in photos[1:]])
                await eor(message, text="Successfully deleted photos")
            else:
                await eor(message, text="No profile photos found.")
        except Exception as e:
            await eor(message, text=e)


async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})


__MODULE__ = "Assistente"
__HELP__ = """

<u> Comandos do assistente:</u>
.setpfp - Responda com uma foto para definir a imagem de perfil de todos os assistentes do bot [apenas foto] [apenas para usuário sudo]

.setname [texto] - para definir o nome de todos os assistentes [apenas para usuário sudo]

.setbio [texto] - para definir a bio de todos os assistentes [apenas para usuário sudo]


.delpfp - Exclui a foto de perfil dos assistentes [apenas uma foto de perfil será excluída] [apenas para usuário sudo]

.delallpfp - Exclui todas as fotos de perfil dos assistentes [apenas uma foto de perfil permanecerá] [apenas para usuário sudo]

<u> Comandos do assistente de grupo:</u>

/checkassistant - Verifique os detalhes do assistente do seu grupo

/setassistant - Altere o assistente para um assistente específico para o seu grupo

/changeassistant - Altere o assistente do seu grupo para um assistente aleatório disponível nos servidores do bot.
"""
