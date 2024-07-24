import asyncio

from pyrogram import filters
from pyrogram.types import Message

import speedtest
from CineWinx import app
from CineWinx.misc import SUDOERS
from config import PREFIXES
from strings import get_command

SPEEDTEST_COMMAND = get_command("SPEEDTEST_COMMAND")


def testspeed(m):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = m.edit("⇆ 𝗘𝘅𝗲𝗰𝘂𝘁𝗮𝗻𝗱𝗼 𝘁𝗲𝘀𝘁𝗲 𝗱𝗲 𝘃𝗲𝗹𝗼𝗰𝗶𝗱𝗮𝗱𝗲 𝗱𝗲 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱...")
        test.download()
        m = m.edit("⇆ 𝗘𝘅𝗲𝗰𝘂𝘁𝗮𝗻𝗱𝗼 𝘁𝗲𝘀𝘁𝗲 𝗱𝗲 𝘃𝗲𝗹𝗼𝗰𝗶𝗱𝗮𝗱𝗲 𝗱𝗲 𝘂𝗽𝗹𝗼𝗮𝗱...")
        test.upload()
        test.results.share()
        result = test.results.dict()
        m = m.edit("↻ 𝗖𝗼𝗺𝗽𝗮𝗿𝘁𝗶𝗹𝗵𝗮𝗻𝗱𝗼 𝗿𝗲𝘀𝘂𝗹𝘁𝗮𝗱𝗼 𝗱𝗼 𝘁𝗲𝘀𝘁𝗲 𝗱𝗲 𝘃𝗲𝗹𝗼𝗰𝗶𝗱𝗮𝗱𝗲")
    except Exception as e:
        return m.edit(f"❌ {str(e)}")
    return result


@app.on_message(filters.command(SPEEDTEST_COMMAND, PREFIXES) & SUDOERS)
async def speedtest_function(_client: app, message: Message):
    m = await message.reply_text("🚀 𝗘𝘅𝗲𝗰𝘂𝘁𝗮𝗻𝗱𝗼 𝘁𝗲𝘀𝘁𝗲 𝗱𝗲 𝘃𝗲𝗹𝗼𝗰𝗶𝗱𝗮𝗱𝗲...")
    loop = asyncio.get_event_loop_policy().get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m)
    output = f"""<b>📊 𝗥𝗲𝘀𝘂𝗹𝘁𝗮𝗱𝗼 𝗱𝗼 𝘁𝗲𝘀𝘁𝗲 𝗱𝗲 𝘃𝗲𝗹𝗼𝗰𝗶𝗱𝗮𝗱𝗲 📊</b>

<b><u>👤 𝗖𝗹𝗶𝗲𝗻𝘁𝗲:</u></b>
<b>🏢 𝗜𝗦𝗣:</b> {result['client']['isp']}
<b>🌍 𝗣𝗮𝗶́𝘀:</b> {result['client']['country']}

<b><u>🌐 𝗦𝗲𝗿𝘃𝗶𝗱𝗼𝗿:</u></b>
<b>📌 𝗡𝗼𝗺𝗲:</b> {result['server']['name']}
<b>🌍 𝗣𝗮𝗶́𝘀:</b> {result['server']['country']}, {result['server']['cc']}
<b>🤝 𝗣𝗮𝘁𝗿𝗼𝗰𝗶𝗻𝗮𝗱𝗼𝗿:</b> {result['server']['sponsor']}
<b>⚡ 𝗟𝗮𝘁ê𝗻𝗰𝗶𝗮:</b> {result['server']['latency']} ms
<b>🏓 𝗣𝗶𝗻𝗴:</b> {result['ping']} ms"""

    msg = await app.send_photo(
        chat_id=message.chat.id, photo=result["share"], caption=output
    )
    await m.delete()
