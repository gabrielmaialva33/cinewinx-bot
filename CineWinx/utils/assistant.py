import logging

from CineWinx.utils.database import get_client


async def get_assistant_details():
    msg = (
        "<b>🛠️ 𝗨𝘀𝗼</b>: <code>/setassistant [𝗻ú𝗺𝗲𝗿𝗼 𝗱𝗼 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲]</code> 𝗽𝗮𝗿𝗮 "
        "𝗮𝗹𝘁𝗲𝗿𝗮𝗿 𝗲 𝗱𝗲𝗳𝗶𝗻𝗶𝗿 𝗺𝗮𝗻𝘂𝗮𝗹𝗺𝗲𝗻𝘁𝗲 𝗼 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗱𝗼 "
        "𝗴𝗿𝘂𝗽𝗼\n𝗔𝗯𝗮𝗶𝘅𝗼 𝗲𝘀𝘁ã𝗼 𝗮𝗹𝗴𝘂𝗻𝘀 𝗱𝗲𝘁𝗮𝗹𝗵𝗲𝘀 𝗱𝗼𝘀 𝗮𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲𝘀 "
        "𝗱𝗶𝘀𝗽𝗼𝗻𝗶́𝘃𝗲𝗶𝘀\n"
    )
    try:
        a = await get_client(1)
        msg += (
            f"𝗔𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗻ú𝗺𝗲𝗿𝗼: 1\n👤 𝗡𝗼𝗺𝗲: [{a.name}](https://t.me/{a.username})\n🏷️ "
            f"𝗨𝘀𝘂á𝗿𝗶𝗼: @{a.username}\n🆔 𝗜𝗗: {a.id}\n\n"
        )
    except Exception as e:
        logging.exception(e)

    try:
        b = await get_client(2)
        msg += (
            f"𝗔𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗻ú𝗺𝗲𝗿𝗼: 2\n👤 𝗡𝗼𝗺𝗲: <a href='https://t.me/{b.username}'>{b.name}</a>\n"
            f"🏷️ 𝗨𝘀𝘂á𝗿𝗶𝗼: @{b.username}\n🆔 𝗜𝗗: {b.id}\n"
        )
    except Exception as e:
        logging.exception(e)

    try:
        c = await get_client(3)
        msg += (
            f"𝗔𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗻ú𝗺𝗲𝗿𝗼: 3\n👤 𝗡𝗼𝗺𝗲: <a href='https://t.me/{c.username}'>{c.name}</a>\n"
            f"🏷️ 𝗨𝘀𝘂á𝗿𝗶𝗼: @{c.username}\n🆔 𝗜𝗗: {c.id}\n"
        )
    except Exception as e:
        logging.exception(e)

    try:
        d = await get_client(4)
        msg += (
            f"𝗔𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗻ú𝗺𝗲𝗿𝗼: 4\n👤 𝗡𝗼𝗺𝗲: <a href='https://t.me/{d.username}'>{d.name}</a>\n"
            f"🏷️ 𝗨𝘀𝘂á𝗿𝗶𝗼: @{d.username}\n🆔 𝗜𝗗: {d.id}\n"
        )
    except Exception as e:
        logging.exception(e)

    try:
        e = await get_client(5)
        msg += (
            f"𝗔𝘀𝘀𝗶𝘀𝘁𝗲𝗻𝘁𝗲 𝗻ú𝗺𝗲𝗿𝗼: 5\n👤 𝗡𝗼𝗺𝗲: <a href='https://t.me/{e.username}'>{e.name}</a>\n"
            f"🏷️ 𝗨𝘀𝘂á𝗿𝗶𝗼: @{e.username}\n🆔 𝗜𝗗: {e.id}\n"
        )
    except Exception as e:
        pass

    return msg


async def is_avl_assistant():
    from config import STRING1, STRING2, STRING3, STRING4, STRING5

    filled_count = sum(
        1
        for var in [STRING1, STRING2, STRING3, STRING4, STRING5]
        if var and var.strip()
    )
    if filled_count == 1:
        return True
    else:
        return False
