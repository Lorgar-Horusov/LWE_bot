from openai import OpenAI
import asyncio
import keyring
import tempfile
import io, os
from typing import List, Dict
import json
import sqlite3
from numpy import dot
from numpy.linalg import norm

CHAT_GPT_TOKEN = keyring.get_password('discord_bot', 'token_chatGPT')
if CHAT_GPT_TOKEN is None:
    CHAT_GPT_TOKEN = input('Write Token: ')
    keyring.set_password('discord_bot', 'token_chatGPT', CHAT_GPT_TOKEN)
    CHAT_GPT_TOKEN = keyring.get_password('discord_bot', 'token_chatGPT')
client = OpenAI(base_url='https://api.naga.ac/v1', api_key=CHAT_GPT_TOKEN)


async def embedding_generate(text: str) -> List[float]:
    text = text.replace("\n", " ")
    response = client.embeddings.create(
        input=[text],
        model='text-embedding-ada-002',
    )
    return response.data[0].embedding

def cosine_similarity(vector1, vector2):
    return dot(vector1, vector2) / (norm(vector1) * norm(vector2))


def need_update(new_embedding: List[float], old_embedding: List[float], threshold: float = 0.8):
    if old_embedding is None:
        return True
    similarity = cosine_similarity(new_embedding, old_embedding)
    return similarity < threshold


async def chat_gpt(prompt: str, model: str, tokens: int):
    response = client.chat.completions.create(
        model=model,
        messages=[{'role': 'user', 'content': prompt}],
        max_tokens=tokens
    )
    return response.choices[0].message.content


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
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Удаляем временный файл
        os.remove(temp_file_name)
    text = transcription.text
    return text


async def main():
    # respons = await chat_gpt('Привет', 'llama-3.2-90b-vision-instruct', 100)
    # print(respons)
    resp = await embedding_generate('just a lot of letters for a test')
    print(resp)


if __name__ == '__main__':
    asyncio.run(main())
