import asyncio

from pyrogram import filters
from pyrogram.types import Message

import speedtest
from CineWinx import app
from CineWinx.misc import SUDOERS
from strings import get_command

SPEEDTEST_COMMAND = get_command("SPEEDTEST_COMMAND")


def testspeed(m):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = m.edit("⇆ Executando teste de velocidade de download...")
        test.download()
        m = m.edit("⇆ Executando teste de velocidade de upload...")
        test.upload()
        test.results.share()
        result = test.results.dict()
        m = m.edit("↻ Compartilhando resultado do teste de velocidade")
    except Exception as e:
        return m.edit(e)
    return result


@app.on_message(filters.command(SPEEDTEST_COMMAND) & SUDOERS)
async def speedtest_function(_client: app, message: Message):
    m = await message.reply_text("Executando teste de velocidade")
    loop = asyncio.get_event_loop_policy().get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m)
    output = f"""**Resultado do teste de velocidade**

<u>**Cliente:**</u>
**ISP:** {result['client']['isp']}
**País:** {result['client']['country']}

<u>**Servidor:**</u>
**Nome:** {result['server']['name']}
**País:** {result['server']['country']}, {result['server']['cc']}
**Patrocinador:** {result['server']['sponsor']}
**Latência:** {result['server']['latency']}  
**Ping:** {result['ping']}"""

    msg = await app.send_photo(
        chat_id=message.chat.id, photo=result["share"], caption=output
    )
    await m.delete()
