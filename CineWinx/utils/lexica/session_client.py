import base64
from typing import Union, Dict
import aiohttp
from lexica.constants import BASE_URL, SESSION_HEADERS
from lexica.utils import clean_dict


class SessionAsyncClient:
    def __init__(self):
        """
        Initialize the class
        """
        self.url = BASE_URL
        self.session = None
        self.headers = SESSION_HEADERS
        self.timeout = 60

    async def fetch(self, **kwargs) -> Union[Dict, bytes]:
        if self.session is None:
            raise Exception("Session not initialized. Call __aenter__ first.")

        self.headers.update(kwargs.get("headers", {}))
        contents = {"json": None, "data": None, "files": None}
        for key in contents:
            if key in kwargs:
                contents[key] = clean_dict(kwargs.get(key))

        request_kwargs = {
            "method": kwargs.get("method", "GET"),
            "url": kwargs.get("url"),
            "headers": self.headers,
            "params": kwargs.get("params"),
            "timeout": self.timeout,
        }

        if contents["data"] is not None:
            request_kwargs["data"] = contents["data"]
        elif contents["json"] is not None:
            request_kwargs["json"] = contents["json"]

        async with self.session.request(**request_kwargs) as response:
            if response.status != 200:
                raise Exception(f"api error {await response.text()}")
            if response.headers.get("content-type") in [
                "image/png",
                "image/jpeg",
                "image/jpg",
            ]:
                return await response.read()
            rdata = await response.json()
            if rdata["code"] == 0:
                raise Exception(f"api error {await response.text()}")
            return rdata

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self

    async def close(self) -> None:
        """Close async session"""
        if self.session:
            await self.session.close()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def get_models(self) -> dict:
        response = await self.fetch(url=f"{self.url}/models")
        return response

    async def get_chat_models(self) -> dict:
        response = await self.get_models()
        return response["models"]["chat"]

    async def get_image_models(self) -> dict:
        response = await self.get_models()
        return response["models"]["image"]

    async def get_nsfw_models(self) -> dict:
        response = await self.get_models()
        return response["models"]["AntiNSFW"]

    async def get_custom_gpt_models(self) -> dict:
        response = await self.get_models()
        return response["models"]["customGPTs"]

    async def get_upscale_models(self) -> dict:
        response = await self.get_models()
        return response["models"]["upscale"]

    async def upscale(
        self,
        model_id: int = 37,
        image: bytes = None,
        image_url: str = None,
        f: str = "binary",
    ) -> bytes:
        payload = {"format": f, "model_id": model_id}

        if image is None and image_url is None:
            raise ValueError("Either image or image_url must be provided")
        if image and not image_url:
            payload.setdefault("image_data", base64.b64encode(image).decode("utf-8"))
        elif not image and not image_url:
            raise Exception("No image or image_url provided")
        else:
            payload.setdefault("image_url", image_url)

        response = await self.fetch(
            url=f"{self.url}/upscale", method="POST", json=payload
        )

        return response
