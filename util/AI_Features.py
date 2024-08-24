import time
from os import times

from openai import OpenAI
import asyncio
import keyring

CHAT_GPT_TOKEN = keyring.get_password('discord_bot', 'token_chatGPT')
if CHAT_GPT_TOKEN is None:
    CHAT_GPT_TOKEN = input('Write Token: ')
    keyring.set_password('discord_bot', 'token_chatGPT', CHAT_GPT_TOKEN)
    CHAT_GPT_TOKEN = keyring.get_password('discord_bot', 'token_chatGPT')
client = OpenAI(base_url='https://api.naga.ac/v1', api_key=CHAT_GPT_TOKEN)


async def chat_gpt(prompt: str):
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[{'role': 'user', 'content': prompt}]
    )
    return response.choices[0].message.content


def moderation(text: str):
    response = client.moderations.create(input=text, model='text-moderation-latest')
    print(response.results)
    return response.results[0]


async def main():
    text = '''на днях бомбануло

тот случай когда ты еблан берущий чужие вещи без спроса и при этом не знаешь физику и режешь чужим ножом 20килограмовый замороженный в лед куб слив.масла

самое охуенное тут то что нож был подарком близкого друга а это уже не возместить

не берите чужое чуваки'''
    print('Rus')
    moderation(text)



if __name__ == '__main__':
    asyncio.run(main())
