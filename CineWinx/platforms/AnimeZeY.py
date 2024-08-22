import json
from typing import Union, Dict, Any, Optional, TypedDict, List
import aiohttp


class FileDict(TypedDict):
    mimeType: str
    name: str
    modifiedTime: str
    id: str
    driveId: str
    link: str


class SearchMovieResponse(TypedDict):
    nextPageToken: Optional[str]
    curPageIndex: int
    data: "DataDict"


class DataDict(TypedDict):
    nextPageToken: Optional[str]
    files: List[FileDict]


class AnimiZeYAPI:
    def __init__(self):
        self.url: str = "https://animezey16082023.animezey16082023.workers.dev"
        self.session: Optional[aiohttp.ClientSession] = None
        self.base_url: str = "https://animezey16082023.animezey16082023.workers.dev"
        self.session_headers: Dict[str, str] = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
            "Content-Type": "application/json",
        }

        self.timeout: int = 60

    async def request(
        self, endpoint: str, method: str, data: Optional[Dict[str, Any]] = None
    ) -> Union[Dict[str, Any], str, None]:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.request(
                    method, self.url + endpoint, headers=self.session_headers, json=data
                ) as response:
                    content_type: str = response.headers.get("Content-Type", "")
                    if "application/json" in content_type:
                        return await response.json()
                    else:
                        text: str = await response.text()
                        try:
                            return json.loads(text)
                        except json.JSONDecodeError:
                            return text
            except Exception as e:
                print(e)
                return None

    async def search_anime(
        self, query: str, page_token: Optional[str] = None
    ) -> Union[Dict[str, Any], str, None]:
        return await self.request(
            "/0:search", "POST", {"q": query, "page_token": page_token, "page_index": 0}
        )

    async def search_movie(
        self, query: str, page_token: Optional[str] = None
    ) -> Optional[SearchMovieResponse]:
        response: Optional[SearchMovieResponse] = await self.request(
            "/1:search",
            "POST",
            {
                "q": query,
                "page_token": page_token,
                "page_index": 0,
            },
        )
        return response

    async def download(self, file_name: str, link: str) -> str:
        sanitized_file_name: str = file_name.replace(r'[\/\?<>\\:\*\|":]', "_")
        file_path: str = f"movies/{sanitized_file_name}"
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}{link}", headers=self.session_headers
            ) as response:
                with open(file_path, "wb") as f:
                    f.write(await response.read())
        return file_path

    async def movie_foder(self) -> Union[Dict[str, Any], str, None]:
        return await self.request(
            "/1:/Filmes/",
            "POST",
            {
                "id": "",
                "type": "folder",
                "password": "",
                "page_token": "",
                "page_index": 0,
            },
        )

    async def navigate_folder(self, id: str) -> Union[Dict[str, Any], str, None]:
        return await self.request(
            "/1:/Filmes/",
            "POST",
            {
                "id": id,
                "type": "folder",
                "password": "",
                "page_token": "",
                "page_index": 0,
            },
        )
