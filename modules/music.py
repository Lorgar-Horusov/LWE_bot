from interactions import Extension, listen, slash_command, SlashContext, slash_option
from interactions_lavalink import Lavalink
from interactions_lavalink.events import TrackStart


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

    @slash_command()
    @slash_option("query", "The search query or url", opt_type=3, required=True)
    async def play(self, ctx: SlashContext, query: str):
        await ctx.defer()

        voice_state = ctx.author.voice
        if not voice_state or not voice_state.channel:
            return await ctx.send("You're not connected to the voice channel!")

        player = await self.lavalink.connect(voice_state.guild.id, voice_state.channel.id)
        tracks = await player.search_youtube(query)
        search_msg = await ctx.send('Search in YouTube 🔍')
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
            return await ctx.send(f"Added to queue: {track.title}")

        await player.play()
        await ctx.send(f"Now playing: {track.title}")

    @slash_command()
    async def leave(self, ctx: SlashContext):
        await self.lavalink.disconnect(ctx.guild.id)
        await ctx.send("Disconnected", ephemeral=True)
