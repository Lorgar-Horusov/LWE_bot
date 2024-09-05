from interactions import Extension, listen, slash_command, SlashContext, slash_option, Embed
from interactions_lavalink import Lavalink, Player
from interactions_lavalink.events import TrackStart
import validators

from load_modules import load_config


def search_embed(track: str, url: str, requester: int, duration: int, image: str):
    embed = Embed(
        title="Now playing",
        description=f'[{track}]({url})',
        color=0x00ff00
    )
    embed.set_author(
        name='Legendary Web Enforcer',
        url='https://github.com/Lorgar-Horusov/LWE_bot',
        icon_url="https://cdn.discordapp.com/avatars/1269739594736341227/160567261d976bdb1d4bd31745520b77"
    )
    embed.add_field(
        name='requester',
        value=f'<@{requester}>',
        inline=True
    )
    embed.add_field(
        name='duration',
        value=f'{duration // 60}:{duration % 60:02d}',
        inline=True
    )
    embed.set_image(
        url=image
    )
    return embed


def add_queue_embed(track: str, url: str, requester: int, image: str):
    embed = Embed(
        title="Added to queue",
        description=f'[{track}]({url})',
        color=0x00ff00
    )
    embed.set_author(
        name="Legendary Web Enforcer",
        url="https://github.com/Lorgar-Horusov/LWE_bot",
        icon_url="https://cdn.discordapp.com/avatars/1269739594736341227/160567261d976bdb1d4bd31745520b77"
    )
    embed.add_field(
        name='requester',
        value=f'<@{requester}>',
        inline=True
    )
    embed.set_thumbnail(
        url=image
    )
    return embed


class Music(Extension):
    def __init__(self, client):
        self.client = client
        self.lavalink: Lavalink | None = None

    @listen()
    async def on_startup(self):
        self.lavalink: Lavalink = Lavalink(self.client)
        self.lavalink.add_node("127.0.0.1", 43421, "Wufflies_CUM", "eu")

    @listen()
    async def on_track_start(self, event: TrackStart):
        print("Track started", event.track.title)

    @slash_command(description='Play music')
    @slash_option("query", "The search query or url", opt_type=3, required=True)
    async def play(self, ctx: SlashContext, query: str):
        await ctx.defer()
        config = load_config()
        if not config.get('music', False):
            return await ctx.send("Music module is disabled")

        voice_state = ctx.author.voice
        if not voice_state or not voice_state.channel:
            return await ctx.send("You're not connected to the voice channel!")

        player = await self.lavalink.connect(voice_state.guild.id, voice_state.channel.id)
        search_msg = await ctx.send('Searching for music 🔍')

        if validators.url(query):
            try:
                tracks = await player.node.get_tracks(query)
                track = tracks.tracks[0]
            except (IndexError, Exception) as e:
                print(e)
                return await ctx.edit(message=search_msg, content='Music not found or failed to retrieve from URL')
        else:
            tracks = await player.search_youtube(query)
            search_msg = await ctx.edit(message=search_msg, content='Search in YouTube 🔍')
            try:
                track = tracks[0]
            except IndexError:
                tracks = await player.search_soundcloud(query)
                await ctx.edit(message=search_msg, content='Search in soundCloud 🔍')
                try:
                    track = tracks[0]
                except IndexError:
                    return await ctx.edit(message=search_msg, content='Music not a found')

        player.add(requester=int(ctx.author.id), track=track)

        if player.is_playing:
            embed = add_queue_embed(track.title, track.uri, int(ctx.author.id), track.artwork_url)
            return await ctx.edit(message=search_msg, content='', embed=embed)
        await player.play()

        embed = search_embed(
            track.title,
            player.current.uri,
            int(ctx.author.id),
            int(player.current.duration / 1000),
            player.current.artwork_url)
        await ctx.edit(message=search_msg, content='', embed=embed)

    @slash_command(description='Show the current playing song')
    async def now_playing(self, ctx: SlashContext):
        player: Player = self.lavalink.get_player(ctx.guild.id)

        if not player or not player.is_playing:
            return await ctx.send("Nothing is playing")

        track = player.current.title
        track_url = player.current.uri
        track_img = player.current.artwork_url
        position = player.position / 1000
        duration = player.current.duration / 1000
        quantity = 15
        blocks = round((position / duration) * quantity)
        blocks = min(blocks, quantity)
        time = f"{int(position // 60)}:{int(position % 60):02d}-{int(duration // 60)}:{int(duration % 60):02d}"
        progressbar = ''.join(['▰' if i <= blocks else '▱' for i in range(quantity)])

        embed = Embed(
            title=track,
            url=track_url,
            description=f"『{progressbar}』 {time}",
            color=0x00ffff
        )
        embed.set_author(
            name="Legendary Web Enforcer",
            url='https://github.com/Lorgar-Horusov/LWE_bot',
            icon_url='https://cdn.discordapp.com/avatars/1269739594736341227/160567261d976bdb1d4bd31745520b77'
        )
        embed.set_image(
            url=track_img
        )
        await ctx.send(embeds=embed)

    @slash_command()
    async def leave(self, ctx: SlashContext):
        await self.lavalink.disconnect(ctx.guild.id)
        await ctx.send("Bluetooth device disconnected", ephemeral=True)

    @slash_command()
    async def queue(self, ctx: SlashContext):
        player: Player = self.lavalink.get_player(ctx.guild.id)

        if not player or not player.queue:
            return await ctx.send("Queue is empty")

        queue_description = ''
        queue = player.queue
        embed = Embed(
            title="Queue",
            color=0x00ffff
        )
        for i, track in enumerate(queue, start=1):
            track_duration = f"{track.duration // 60000}:{(track.duration // 1000) % 60:02d}"
            queue_description += f"{i}. [{track.title}]({track.uri}) | `{track_duration}` | Requested by: <@{track.requester}>\n"
        embed.description = queue_description

        embed.set_author(
            name="Legendary Web Enforcer",
            url='https://github.com/Lorgar-Horusov/LWE_bot',
            icon_url='https://cdn.discordapp.com/avatars/1269739594736341227/160567261d976bdb1d4bd31745520b77'
        )

        await ctx.send(embed=embed)
