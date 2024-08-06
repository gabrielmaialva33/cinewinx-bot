from typing import Union, Dict

from httpx import AsyncClient
from lexica.constants import BASE_URL, SESSION_HEADERS
from lexica.utils import clean_dict


class LexicaAsyncClient:
    def __init__(
        self: "LexicaAsyncClient",
    ):
        """
        Initialize the class
        """
        self.url = BASE_URL
        self.session = AsyncClient(
            http2=True,
            verify=False,
            timeout=60,
            headers=SESSION_HEADERS,
        )
        self.headers = SESSION_HEADERS
        self.timeout = 60

    async def fetch(self: "LexicaAsyncClient", **kwargs) -> Union[Dict, bytes]:
        self.headers.update(kwargs.get("headers", {}))
        contents = {"json": {}, "data": {}, "files": {}}
        for i in list(contents):
            if i in kwargs:
                contents[i] = clean_dict(kwargs.get(i))
        response = await self.session.request(
            method=kwargs.get("method", "GET"),
            url=kwargs.get("url"),
            headers=self.headers,
            content=kwargs.get("content"),
            params=kwargs.get("params"),
            data=contents.get("data"),
            json=contents.get("json"),
            files=contents.get("files"),
            timeout=self.timeout,
        )
        if response.status_code != 200:
            raise Exception(f"api error {response.text}")
        if response.headers.get("content-type") in [
            "image/png",
            "image/jpeg",
            "image/jpg",
        ]:
            return response.content
        rdata = response.json()
        if rdata["code"] == 0:
            raise Exception(f"api error {response.text}")
        return rdata

    async def __aenter__(self):
        return self

    async def close(self) -> None:
        """Close async session"""
        return await self.session.aclose()

    async def get_models(self) -> dict:
        resp = await self.fetch(url=f"{self.url}/models")
        return resp

    async def get_chat_models(self) -> dict:
        response = await self.get_models()
        return response["models"]["chat"]

    async def get_image_models(self) -> dict:
        response = await self.get_models()
        return response["models"]["image"]

    async def get_nsfw_model(self) -> dict:
        response = await self.get_models()
        return response["models"]["AntiNSFW"]

    async def get_custom_gpt_model(self) -> dict:
        response = await self.get_models()
        return response["models"]["customGPTs"]

    async def get_upscale_model(self) -> dict:
        response = await self.get_models()
        return response["models"]["upscale"]
