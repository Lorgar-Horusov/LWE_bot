import interactions
from interactions import (
    Extension,
    SlashContext,
    slash_command,
    Embed)
import re
from util.image_generation import ImageGenerator
from load_modules import load_config
from rich.console import Console

console = Console()

def nsfw_checker(data):
    nsfw_words = [
        'nsfw', 'naked', 'undress', 'hentai', 'porn', 'xxx',
        'sex', 'adult', 'erotic', 'fetish', 'boobs', 'ass', 'pussy',
        'dick', 'cum', 'blowjob', 'handjob', 'orgy', 'cumshot', 'sexy',
        'strip', 'masturbate', 'sextape', 'milf', 'gay', 'lesbian', 'tits',
        'vagina', 'penis', 'butt', 'fuck', 'suck', 'hardcore', 'softcore',
        'dildo', 'vibrator', 'bukkake', 'rape', 'swinger', 'brothel',
        'escort', 'nude', 'jizz', 'clit', 'nipple', 'fisting', 'shemale',
        'transgender', 'orgasm', 'kink', 'anal', 'paedophile', 'groping', 'public indecency'
    ]
    for words in nsfw_words:
        if re.search(rf'\b{re.escape(words)}\b', data, re.IGNORECASE):
            return True
    return False


class ImageGeneration(Extension):
    def __init__(self, client):
        self.client = client
        self.generator = ImageGenerator()

    @slash_command(
        name='image_generation',
        description='Сгенерировать изображение',
        options=[
            {
                "name": "prompt",
                "description": "Что сгенерировать",
                "type": 3,
                "required": True
            }
        ]
    )
    async def image_generation(self, ctx: SlashContext, prompt):
        placeholder_msg = await ctx.send('Generating image')
        image = await self.generator.generate(prompt)
        embed = Embed(
            title="Image Generator",
            color=0x00ff00,
        )
        embed.add_field(
            name=f"Prompt",
            value=prompt,
            inline=False
        )
        embed.set_author(
            name='Legendary Web Enforcer',
            url='https://github.com/Lorgar-Horusov/LWE_bot',
            icon_url="https://cdn.discordapp.com/avatars/1269739594736341227/160567261d976bdb1d4bd31745520b77"
        )
        file = interactions.File(image, description='Generated Image', file_name='image.png')
        await ctx.edit(message=placeholder_msg, embed=embed, file=file, content='')
        return


