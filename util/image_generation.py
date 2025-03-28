import asyncio
from openai import OpenAI
import keyring
from enum import Enum
from rich.console import Console
import aiohttp
from PIL import Image
from io import BytesIO
from time import time

console = Console()
CHAT_GPT_TOKEN = keyring.get_password('discord_bot', 'token_chatGPT')
if CHAT_GPT_TOKEN is None:
    CHAT_GPT_TOKEN = input('Write Token: ')
    keyring.set_password('discord_bot', 'token_chatGPT', CHAT_GPT_TOKEN)
    CHAT_GPT_TOKEN = keyring.get_password('discord_bot', 'token_chatGPT')
client = OpenAI(base_url='https://api.naga.ac/v1', api_key=CHAT_GPT_TOKEN)


class Models(Enum):
    MIDJOURNEY = ("Flux-Midjourney-Mix2-LoRA", "Midjourney")
    ANIME_SKETCH = ("anime-blockprint-style", "Anime sketch")
    PENCIL_SKETCH = ("shou_xin", "Pencil sketch")
    COLOR_SKETCH = ("Flux-Sketch-Ep-LoRA", "Color sketch")
    VECTOR_SKETCH = ("vector-illustration", "Vector sketch")
    ICONS = ("Flux-Icon-Kit-LoRA", "Icons")
    LOGO = ("FLUX.1-dev-LoRA-Logo-Design", "Logos")
    TARO_CARD = ("flux-tarot-v1", "Taro")


async def download_image(image_url):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(image_url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    image = Image.open(BytesIO(image_data))
                    png_buffer = BytesIO()
                    image.save(png_buffer, format="PNG")
                    png_buffer.seek(0)
                    return png_buffer
                else:
                    console.log(f"Failed to download image. Status code: {response.status}")
                    return None
        except Exception as e:
            console.print_exception(show_locals=True)
            return None

class ImageGenerator:
    def __init__(self):
        self.base_url = "https://fluxai.pro/api/tools/fast"

    async def generate_image(self, prompt):
        payload = {'prompt': prompt}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.base_url, json=payload) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        if 'data' in response_data and 'imageUrl' in response_data['data']:
                            return response_data['data']['imageUrl']
                        else:
                            console.log("Unexpected response structure:", response_data)
                            return None
                    else:
                        console.log(f"Failed to generate image. Status code: {response.status}")
                        return None
            except aiohttp.ClientResponseError as e:
                console.print_exception(show_locals=True)
                return None

    async def generate(self, prompt):
        try:
            start_time = time()
            image_url = await self.generate_image(prompt)
            console.log(f"[green]Image generation took [red]{time() - start_time:.2f} [green]seconds\n [italic cyan]prompt: {prompt}")
            if image_url:
                return await download_image(image_url)
            else:
                return None
        except Exception as e:
            console.print_exception(show_locals=True)
            return None

if __name__ == '__main__':
    async def main():
        image_generator = ImageGenerator()
        image = await image_generator.generate('a cat')
        print(image)

    asyncio.run(main())

