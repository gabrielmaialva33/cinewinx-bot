import asyncio
import logging
from pyrogram import Client as c

API_ID = input("🔑 Enter Your API_ID:\n > ")
API_HASH = input("🔒 Enter Your API_HASH:\n > ")

i = c("cinewinx_string", in_memory=True, api_id=API_ID, api_hash=API_HASH)


async def main():
    await i.start()
    ss = await i.export_session_string()
    print("\n✅ HERE IS YOUR STRING SESSION, COPY IT, DON'T SHARE!!\n")
    print(f"\n🔗 {ss}\n")
    print("🎉 STRING GENERATED\n")
    xx = f"✅ HERE IS YOUR STRING SESSION, COPY IT, DON'T SHARE!!\n\n`{ss}`\n\n🎉 STRING GENERATED"
    try:
        await i.send_message("me", xx)
        print("📩 String session successfully sent to your 'Saved Messages'.")
    except BaseException as e:
        logging.warning(f"⚠️ Error occurred: {e}")


asyncio.run(main())
