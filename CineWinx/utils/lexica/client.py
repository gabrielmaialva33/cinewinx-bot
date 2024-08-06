import logging
from typing import Union, Dict

import httpx
from lexica.constants import BASE_URL, SESSION_HEADERS
from lexica.utils import clean_dict


class LexicaClient:
    def __init__(self: "LexicaClient"):
        self.url = BASE_URL
        self.session = httpx.Client(http2=True)
        self.timeout = 60
        self.headers = SESSION_HEADERS
        self.models = self.get_models()

    def fetch(self: "LexicaClient", **kwargs) -> Union[Dict, bytes]:
        self.headers.update(kwargs.get("headers", {}))
        contents = {"json": {}, "data": {}, "files": {}}
        for i in list(contents):
            if i in kwargs:
                contents[i] = clean_dict(kwargs.get(i))
        response = self.session.request(
            method=kwargs.get("method", "GET"),
            url=kwargs.get("url"),
            headers=self.headers,
            params=kwargs.get("params"),
            data=contents.get("data"),
            json=contents.get("json"),
            files=contents.get("files"),
            timeout=self.timeout,
        )
        if response.status_code != 200:
            logging.error(f"api error {response.text}")
            return response.json()
        if response.headers.get("content-type") in [
            "image/png",
            "image/jpeg",
            "image/jpg",
        ]:
            return response.content
        rdata = response.json()
        if rdata["code"] == 0:
            logging.error(f"api error {response.text}")
            return rdata
        return rdata

    def get_models(self) -> dict:
        response = self.fetch(url=f"{self.url}/models")
        return response

    def get_chat_models(self) -> dict:
        response = self.get_models()
        return response["models"]["chat"]

    def get_image_models(self) -> dict:
        response = self.get_models()
        return response["models"]["image"]

    def anti_nsfw_model(self) -> dict:
        response = self.get_models()
        return response["models"]["AntiNSFW"]

    def custom_gpt_model(self) -> dict:
        response = self.get_models()
        return response["models"]["customGPTs"]

    def upscale_model(self) -> dict:
        response = self.get_models()
        return response["models"]["upscale"]
