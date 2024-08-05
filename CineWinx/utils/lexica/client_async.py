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
        )
        self.headers = SESSION_HEADERS
        self.timeout = 60

    async def _request(self: "LexicaAsyncClient", **kwargs) -> Union[Dict, bytes]:
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
            raise Exception(f"API error {response.text}")
        if response.headers.get("content-type") in [
            "image/png",
            "image/jpeg",
            "image/jpg",
        ]:
            return response.content
        rdata = response.json()
        if rdata["code"] == 0:
            raise Exception(f"API error {response.text}")
        return rdata

    async def get_models(self) -> dict:
        resp = await self._request(url=f"{self.url}/models")
        return resp

    async def __aenter__(self):
        return self

    async def close(self) -> None:
        """Close async session"""
        return await self.session.aclose()

    def get_chats_model(self) -> dict:
        response = self.get_models()
        return response["chats"]
