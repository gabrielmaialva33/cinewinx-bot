import base64
from typing import Union, Dict
import aiohttp


class AnimiZeYAPI:
    def __init__(self):
        self.url = 'https://animezey16082023.animezey16082023.workers.dev'
        self.session = None
        self.base_url = "https://animezey16082023.animezey16082023.workers.dev"
        self.session_headers = {
            "Host": "animezey16082023.animezey16082023.workers.dev",
            "Connection": "keep-alive",
            "sec-ch-ua": '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-platform": '"macOS"',
            "DNT": "1",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Origin": "https://animezey16082023.animezey16082023.workers.dev",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://animezey16082023.animezey16082023.workers.dev/0:search?q=a",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cookie": "perf_dv6Tr4n=1",
            "sec-gpc": "1",
        }

        self.download_headers = {
            "Host": "animezey16082023.animezey16082023.workers.dev",
            "Connection": "keep-alive",
            "sec-ch-ua": '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
            "sec-ch-ua-platform": '"macOS"',
            "DNT": "1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,"
                      "*/*;q=0.8,"
                      "application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cookie": "perf_dv6Tr4n=1",
            "sec-gpc": "1"
        }

        self.timeout = 60

    async def request(self, endpoint: str, method: str, data: Union[Dict, None] = None):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(method, self.url + endpoint, headers=self.session_headers,
                                           json=data) as response:
                    content_type = response.headers.get('Content-Type', 'application/json')
                    print("content_type", content_type)
                    if 'application/json' in content_type:
                        return await response.json()
                    else:
                        text = await response.text()
                        print(f"Unexpected content type: {content_type}")
                        print(f"Response text: {text}")
                        return None
            except Exception as e:
                print(e)
                return None

    async def search_anime(self, query: str, page_token: Union[str, None] = None):
        return await self.request('/0:search', 'POST', {
            'q': query,
            'page_token': page_token or None,
            'page_index': 0
        })

    async def search_movie(self, query: str, page_token: Union[str, None] = None):
        print("search_movie", {
            'q': query,
            'page_token': page_token or None,
            'page_index': 0
        })
        return await self.request('/1:search', 'POST', {
            'q': query,
            'page_token': page_token or None,
            'page_index': 0
        })

    async def download(self, file_name: str, link: str):
        sanitized_file_name = file_name.replace(r'[\/\?<>\\:\*\|":]', '_')
        file_path = f'movies/{sanitized_file_name}'
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{self.base_url}{link}', headers=self.download_headers) as response:
                with open(file_path, 'wb') as f:
                    f.write(await response.read())
        return file_path

    async def get_anime(self, query: str):
        response = await self.search_anime(query)
        return response

    async def get_movie(self, query: str):
        response = await self.search_movie(query)
        return response

    async def get_download_link(self, file_name: str, link: str):
        response = await self.download(file_name, link)
        return response

    async def get_animezey(self, query: str):
        response = await self.get_anime(query)
        return response

    async def get_animezey_movie(self, query: str):
        response = await self.get_movie(query)
        return response

    async def get_animezey_download(self, file_name: str, link: str):
        response = await self.get_download_link(file_name, link)
        return response

    async def get_animezey_download_link(self, file_name: str, link: str):
        response = await self.download(file_name, link)
        return response

    async def get_animezey_search_anime(self, query: str, page_token: Union[str, None] = None):
        response = await self.search_anime(query, page_token)
        return response
