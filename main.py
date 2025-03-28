import interactions
from interactions import Client, Intents
from load_modules import load_module
from tokken_setting import discord_token
from rich.console import Console
client = Client(
    intents=Intents.DEFAULT | Intents.MESSAGE_CONTENT | Intents.GUILD_MODERATION,
)
console = Console()
TOKEN = discord_token()


@interactions.listen()
async def on_ready():
    console.log(f"[bold green]We're online! We've logged in as [bold cyan italic]{client.app.name}.")
    console.log(f"[bold green]Our latency is [bold italic red]{round(client.latency, 2)} ms.")


def start():
    load_module(client)
    client.start(TOKEN)

def stop():
    client.stop()

if __name__ == '__main__':
    load_module(client)
    client.start(TOKEN)
