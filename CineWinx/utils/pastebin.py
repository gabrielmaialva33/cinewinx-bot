import logging

import aiohttp

BASE = "https://batbin.me/"


async def post(url: str, *args: list, **kwargs: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, *args, **kwargs) as resp:
            try:
                data = await resp.json()
            except Exception as e:
                logging.exception(e)
                data = await resp.text()
        return data


async def winx_bin(text: str):
    resp = await post(f"{BASE}api/v2/paste", data=text)
    if not resp["success"]:
        return
    link = BASE + resp["message"]
    return link
