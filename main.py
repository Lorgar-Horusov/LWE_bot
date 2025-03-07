import interactions
from interactions import Client, Intents
from load_modules import load_module
from tokken_setting import discord_token

client = Client(
    intents=Intents.DEFAULT | Intents.MESSAGE_CONTENT | Intents.GUILD_MODERATION,
)

TOKEN = discord_token()
            

@interactions.listen()
async def on_ready():
    print(f"We're online! We've logged in as {client.app.name}.")
    print(f"Our latency is {round(client.latency, 2)} ms.")


def start():
    load_module(client)
    client.start(TOKEN)

def stop():
    client.stop()

if __name__ == '__main__':
    load_module(client)
    client.start(TOKEN)
