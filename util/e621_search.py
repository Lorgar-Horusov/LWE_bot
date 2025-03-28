import asyncio
from base64 import b64encode

import keyring
import io
from rich.console import Console
import aiohttp
import os


console = Console()
username = keyring.get_password("e621", "username")
api_key = keyring.get_password("e621", "api_key")

if not username or not api_key:
    username = input("E621 login: ")
    api_key = input("E621 API key: ")
    keyring.set_password("e621", "username", username)
    keyring.set_password("e621", "api_key", api_key)

base_url_e621 = "https://e621.net/posts/random.json"


async def search_e621(tags: str) -> tuple[io.BytesIO, str, str] | tuple[None, None, None]:
    params = {
        "tags": tags,
    }
    auth_header = f"{username}:{api_key}"
    encoded_auth_header = b64encode(auth_header.encode()).decode()
    headers = {
        "Authorization": f"Basic {encoded_auth_header}",
        "User-Agent": "MyProject/1.0 (on behalf of user Lorgar Horusov)"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(base_url_e621, params=params, headers=headers) as response:
            response.raise_for_status()
            data = await response.json()
            try:
                # _length = len(data["posts"])
                # _choice = random.randint(0, _length - 1)
                _media_content = data["post"]["file"]["url"]
                _tag = data["post"]["tags"]["general"]
                _tag = ", ".join(_tag)
            except Exception:
                console.log(f'[red]Error: [cyan]{data}')
                return None, None, None

            async with session.get(_media_content) as media_response:
                file_name = os.path.basename(_media_content)
                _, _ext = os.path.splitext(file_name)
                console.log(f'[green]link: [cyan]{_media_content}')
                _content = await media_response.read()
                _content = io.BytesIO(_content)

    return _content, _tag, _ext

if __name__ == '__main__':
    content, tags, ext = asyncio.run(search_e621("reggie_(whygena)"))
    console.print(content, tags, ext)
