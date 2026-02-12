from openai import OpenAI
import asyncio
import keyring
import tempfile
import io, os
from typing import List
from rich.console import Console
from rich.markdown import Markdown
from numpy import dot
from numpy.linalg import norm
from pathlib import Path


console = Console()
CHAT_GPT_TOKEN = keyring.get_password('discord_bot', 'token_chatGPT')
if CHAT_GPT_TOKEN is None:
    CHAT_GPT_TOKEN = input('Write Token: ')
    keyring.set_password('discord_bot', 'token_chatGPT', CHAT_GPT_TOKEN)
    CHAT_GPT_TOKEN = keyring.get_password('discord_bot', 'token_chatGPT')
client = OpenAI(base_url='https://api.naga.ac/v1', api_key=CHAT_GPT_TOKEN)

BASE_DIR = Path(__file__).resolve().parent.parent
attitude = 'sci_neko'
attitude_file = BASE_DIR / "util" / "attitude" / f'{attitude}.txt'


async def chat_gpt(prompt: str, model: str, tokens: int):
    with open(attitude_file, 'r', encoding='utf-8') as file:
        system_prompt = file.read()
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt}
            ],
            max_tokens=tokens
        )
        return response.choices[0].message.content
    except Exception:
        console.print_exception(show_locals=True)
        return None

async def speach_to_text(audio_data: io.BytesIO) -> str:
    audio_data.seek(0)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.ogg') as temp_file:
        temp_file.write(audio_data.read())
        temp_file.flush()
        temp_file_name = temp_file.name
    try:
        with open(temp_file_name, 'rb') as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-large",
                file=audio_file
            )
            print(transcription.text)
    except Exception:
        console.print_exception(show_locals=True)
    finally:
        os.remove(temp_file_name)
    text = transcription.text
    return text


async def main():
    respons = await chat_gpt('Привет, Дай небольшой скрипт на пайтон для построчного вывода текста', 'gpt-5-mini-2025-08-07', 100)
    console.print(Markdown(respons))



if __name__ == '__main__':
    asyncio.run(main())
