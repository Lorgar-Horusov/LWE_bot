import interactions
from interactions import Extension, StringSelectMenu, \
    Modal, ParagraphText, SlashContext, slash_command, ModalContext, Embed
from interactions.client.errors import HTTPException
from interactions.api.events import Component
from interactions.client.utils.formatting import spoiler
import random
import re
from util.image_generation import Model, img_gen_prodia


def nsfw_checker(data):
    nsfw_words = [
        'nsfw', 'naked', 'undress', 'hentai', 'porn', 'xxx',
        'sex', 'adult', 'erotic', 'fetish', 'boobs', 'ass', 'pussy',
        'dick', 'cum', 'blowjob', 'handjob', 'orgy', 'cumshot', 'sexy',
        'strip', 'masturbate', 'sextape', 'milf', 'gay', 'lesbian', 'tits',
        'vagina', 'penis', 'butt', 'fuck', 'suck', 'hardcore', 'softcore',
        'dildo', 'vibrator', 'bukkake', 'rape', 'swinger', 'brothel',
        'escort', 'nude', 'jizz', 'clit', 'nipple', 'fisting', 'shemale',
        'transgender', 'orgasm', 'kink', 'anal', 'paedophile', 'groping'
    ]
    for words in nsfw_words:
        if re.search(rf'\b{words}\b', data, re.IGNORECASE):
            return True
    return False


def load_models():
    model = []
    for models in Model:
        value = models.value
        _, display_name, _ = value
        model.append(display_name)
    return model


class ImageGeneration(Extension):
    def __init__(self, client):
        self.client = client

    @slash_command()
    async def image_generation(self, ctx: SlashContext):
        try:
            my_modal = Modal(
                ParagraphText(label="Enter a prompt", custom_id="long"),
                title="Image generations",
                custom_id="my_modal",
            )
            await ctx.send_modal(modal=my_modal)
            modal_ctx: ModalContext = await ctx.bot.wait_for_modal(my_modal)
            prompt = modal_ctx.responses["long"]
            models = load_models()
            components = StringSelectMenu(
                models,
                placeholder="choose model",
                min_values=1,
                max_values=1,
                custom_id='model_name'
            )
            message = await modal_ctx.send(components=components, ephemeral=True)
        except HTTPException:
            return None
        try:
            nsfw = nsfw_checker(prompt)
            used_component: Component = await ctx.bot.wait_for_component(components=components)
            model = used_component.ctx.values[0]
            components.disabled = True
            await ctx.delete(message)
            working_message = await ctx.send(content='Generating', ephemeral=True)

            img = await img_gen_prodia(
                prompt=prompt,
                model=model,
                sampler="Euler a",
                seed=random.randint(1, 100_000),
                neg=None)

            if nsfw:
                img_photo = interactions.File(file=img, file_name='image.png', description=prompt)
                prompt = spoiler(prompt)
            else:
                img_photo = interactions.File(file=img, file_name='image.png', description=prompt)

            embed = Embed(
                title='Image generation',
                description=prompt,
                color=0x00ff00,
            )
            embed.set_author(
                name='LWE',
                icon_url='https://images-ext-1.discordapp.net/external/HbRcL0HMIy6Cy-sSHD29qPKAdKDIkWkWxRKIUftSKjM'
                         '/https/cdn.discordapp.com/avatars/1269739594736341227/160567261d976bdb1d4bd31745520b77'
                         '?format=webp'
            )
            embed.add_field(
                name='Model',
                value=model
            )
            await ctx.delete(working_message)
            await ctx.send(file=img_photo, embed=embed, silent=True)
        except TimeoutError:
            components.disabled = True
            await ctx.edit(message)
            print("Timed Out!")
