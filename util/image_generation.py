import asyncio
import time
import random
import io
import aiohttp
from urllib.parse import quote
from openai import OpenAI
import keyring
from enum import Enum
from colorama import Fore, Style, just_fix_windows_console


just_fix_windows_console()
CHAT_GPT_TOKEN = keyring.get_password('discord_bot', 'token_chatGPT')
if CHAT_GPT_TOKEN is None:
    CHAT_GPT_TOKEN = input('Write Token: ')
    keyring.set_password('discord_bot', 'token_chatGPT', CHAT_GPT_TOKEN)
    CHAT_GPT_TOKEN = keyring.get_password('discord_bot', 'token_chatGPT')
client = OpenAI(base_url='https://api.naga.ac/v1', api_key=CHAT_GPT_TOKEN)


def img_gen_NAGA(promt):
    start_time = time.time()
    response = client.images.generate(
        model='kandinsky-3.1',
        prompt=promt
    )
    stop_time = time.time()
    print(f'Time {round((stop_time - start_time), 2)} sec')
    print(response.data)


async def img_gen_prodia(prompt, model, sampler, seed, neg):
    print(f'{Fore.BLUE}{Style.BRIGHT}Модель: {model}{Fore.RESET}{Style.RESET_ALL}')
    for mod in Model:
        if mod.value[1] == model:
            model = mod.value[0]
    print("\033[1;32m(Prodia) Creating image for :\033[0m", prompt)
    start_time = time.time()

    async def create_job(prompt, model, sampler, seed, neg):
        if neg is None:
            negative = '''verybadimagenegative_v1.3, ng_deepnegative_v1_75t, (ugly face:0.8), cross-eyed, sketches,
            (worst quality:2), (low quality:2), (normal quality:2), normal quality, ((monochrome)),
            ((grayscale)), skin spots, acnes, skin blemishes, bad anatomy, DeepNegative, facing away, tilted head,
            {Multiple people}, lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits,
            cropped, worstquality, low quality, normal quality, jpegartifacts, signature, watermark, username, blurry,
            bad feet, cropped, poorly drawn hands, poorly drawn face, mutation, deformed, worst quality, low quality,
            normal quality, jpeg artifacts, signature, watermark, extra fingers, fewer digits, extra limbs,
            extra arms, extra legs, malformed limbs, fused fingers, too many fingers, long neck, cross-eyed, mutated
            hands, polar lowres, bad body, bad proportions, gross proportions, text, error, missing fingers,
            missing arms, missing legs, extra digit, extra arms, extra leg, extra foot, repeating hair,
            [[[[[bad-artist-anime, sketch by bad-artist]]]]], [[[mutation, lowres, bad hands, [text, signature,
            watermark, username], blurry, monochrome, grayscale, realistic, simple background, limited palette]]],
            close-up, (forehead jewel:1.2), (forehead mark:1.5), (bad and mutated hands:1.3), (worst quality:2.0),
            (low quality:2.0), (blurry:2.0), multiple limbs, bad anatomy, (interlocked fingers:1.2),
            (interlocked leg:1.2), Ugly Fingers, (extra digit and hands and fingers and legs and arms:1.4),
            crown braid, (deformed fingers:1.2), (long fingers:1.2)'''
        else:
            negative = neg
        url = 'https://api.prodia.com/generate'
        params = {
            'new': 'true',
            'prompt': f'{quote(prompt)}',
            'model': model,
            'negative_prompt': negative,
            'steps': '100',
            'cfg': '9.5',
            'seed': f'{seed}',
            'sampler': sampler,
            'upscale': 'True',
            'aspect_ratio': 'square'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                data = await response.json()
                return data['job']

    async with aiohttp.ClientSession() as session:
        job_id = await create_job(prompt, model, sampler, seed, neg)
        url = f'https://api.prodia.com/job/{job_id}'
        headers = {
            'authority': 'api.prodia.com',
            'accept': '*/*',
        }

        async with aiohttp.ClientSession() as session:
            while True:
                async with session.get(url, headers=headers) as response:
                    json = await response.json()
                    if json['status'] == 'succeeded':
                        async with session.get(f'https://images.prodia.xyz/{job_id}.png?download=1',
                                               headers=headers) as response:
                            content = await response.content.read()
                            img_file_obj = io.BytesIO(content)
                            duration = time.time() - start_time
                            print(f"\033[1;34m(Prodia) Finished image creation\n\033[0mJob id : {job_id}  Prompt : ",
                                  prompt, "in", duration, "seconds.")
                            return img_file_obj


class Model(Enum):
    ANYTHING_V5 = ("anythingV5_PrtRE.safetensors [893e49b9]", "Anything V5", "03")
    ABYSSORANGEMIX = ("AOM3A3_orangemixs.safetensors [9600da17]", "AbyssOrangeMix V3", "04")
    CHILDERNSTORIES = ("childrensStories_v1ToonAnime.safetensors [2ec7b88b]", "ChildrensStories", "7")
    DELIBERATE = ("deliberate_v2.safetensors [10ec4b29]", "Deliberate V2", "05")
    DREAMLIKE_V2 = ("dreamlike-photoreal-2.0.safetensors [fdcf65e7]", "Dreamlike Diffusion V2", "07")
    DREAMLIKE_V1 = ("dreamlike-anime-1.0.safetensors [4520e090]", "Dreamlike Diffusion V1", "07")
    DREAMSHAPER_8 = ("dreamshaper_8.safetensors [9d40847d]", "Dreamshaper 8", "07")
    ELLDRETHVIVIDMIX = ("elldreths-vivid-mix.safetensors [342d9d26]", "Elldreth's Vivid", "10")
    TOONYOU_6B = ("toonyou_beta6.safetensors [980f6b15]", "toonyou beta6", "11")
    LYRIEL_V16 = ("lyriel_v16.safetensors [68fceea2]", "Lyriel V1.6", "12")
    MEINAMIX = ("meinamix_meinaV11.safetensors [b56ce717]", "MeinaMix V11", "14")
    OPENJOURNEY = ("openjourney_V4.ckpt [ca2f377f]", "Openjourney V4", "15")
    REALISTICVS_V20 = ("Realistic_Vision_V2.0.safetensors [79587710]", "Realistic Vision V2.0", "18")
    REV_ANIMATED = ("revAnimated_v122.safetensors [3f4fefd9]", "ReV Animated V1.2.2", "19")
    PROTOGEN = ("protogenx34.safetensors [5896f8d5]", "Protogenx", "20")
    RUNDIFFUSION = ("rundiffusionFX_v10.safetensors [cd4e694d]", "rundiffusion", "20")
    RUNDIFFUSION_25D = ("rundiffusionFX25D_v10.safetensors [cd12b0ee]]", "rundiffusion_25D", "20")
    SD_V15 = ("v1-5-pruned-emaonly.safetensors [d7049739]", "Stable Diffusion V1.5", "22")
    SBP = ("shoninsBeautiful_v10.safetensors [25d8c546]", "Shonin's Beautiful People V1.0", "23")
    FURRY = ("indigoFurryMix_v75Hybrid.safetensors [91208cbb]", "Furry", "23")
    THEALLYSMIX = ("theallys-mix-ii-churned.safetensors [5d9225a4]", "TheAlly's Mix II", "24")
    TIMELESS = ("timeless-1.0.ckpt [7c4971d4]", "Timeless V1", "25")


if __name__ == '__main__':
    promt = '''A woman with white hair is completely naked, with her left hand holding a part of her breast 
    and with her right hand revealing her vagina, her face is embarrassed and with a slight blush, the girl 
    is sitting on a bench in the village, in anime style, in the frame the girl is completely together with 
    the bench, next to a bush on which the girl's clothes are hanging carelessly, the girl's legs are spread 
    showing her crotch'''
    img = asyncio.run(img_gen_prodia(
        prompt=promt,
        model='Anything V5',
        sampler="Euler a",
        seed=random.randint(1, 10000),
        neg=None))
    print(img)
    # with open('image.png', 'wb') as f:
    #     f.write(img.getvalue())
    # for model in Model:
    #     name = model.name
    #     value = model.value
    #     file_name, display_name, version = value
    #     print('_'*10)
    #     print(f"Model Name: {name}")
    #     print(f"File Name: {file_name}")
    #     print(f"Display Name: {display_name}")
