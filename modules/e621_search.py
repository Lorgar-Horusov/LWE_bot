import interactions
from interactions import Extension, slash_command, SlashContext, slash_option, Embed

from util.e621_search import search_e621 as e621


class E621Search(Extension):
    @slash_command(name="e621", description="Search e621 for media content", nsfw=True)
    @slash_option(name="tags", description="The tags to search for", required=False, opt_type=3)
    async def e621_find(self, ctx: SlashContext, tags= ''):
        if not ctx.channel.nsfw:
            await ctx.send("This content can only be sent in an NSFW channel.")
            return
        message_send = await ctx.send(content='searching UwU')

        media_content, tag, ext = await e621(tags)
        if media_content is None:
            await ctx.edit(message=message_send, content="No content found or content is inappropriate.")
            return
        media_file = interactions.File(media_content, file_name=f"media{ext}", description=tag)
        embed = Embed(
            title="Search from e621",
            color=0x00ff00
        )
        embed.set_author(
            name="Legendary Web Enforcer",
            url="https://github.com/Lorgar-Horusov/LWE_bot",
            icon_url="https://cdn.discordapp.com/avatars/1269739594736341227/160567261d976bdb1d4bd31745520b77"
        )
        embed.add_field(
            name='Tags',
            value=f'> {tag}'
        )
        await ctx.edit(message=message_send, file=media_file, embed=embed)