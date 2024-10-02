from interactions import Extension, Embed, SlashContext, slash_command, slash_option
from interactions.ext.paginators import Paginator

from util.lib_search_API import search_manga


def embed_generator(manga_list):
    embeds = []
    for manga in manga_list:
        embed = Embed(
            title=f'{manga["name"]} / {manga["rus_name"]}',
            url=manga['href'],
            description=manga['summary'],
            color=0xff8000
        ).set_image(
            url=manga['coverImage']
        ).set_author(
            name='Legendary Web Enforcer',
            url='https://github.com/Lorgar-Horusov/LWE_bot',
            icon_url="https://cdn.discordapp.com/avatars/1269739594736341227/160567261d976bdb1d4bd31745520b77"
        )
        embeds.append(embed)
    return embeds


class GetManga(Extension):

    @slash_command(name="manga", description="Get a manga from Mangalib")
    @slash_option(name="manga", description="Manga name", required=True, opt_type=3)
    async def getmanga(self, ctx: SlashContext, manga: str):
        wait_massage = await ctx.send(content="Searching...", silent=True)
        manga = await search_manga(manga)
        if not manga:
            return await ctx.send(content="No manga found", silent=True)
        manga_embeds = embed_generator(manga)
        paginator = Paginator.create_from_embeds(self.bot, *manga_embeds)
        paginator.wrong_user_message = "It's not your button"
        paginator.hide_buttons_on_stop = True
        paginator.timeout_interval = 60

        await wait_massage.delete()
        await paginator.send(ctx)
