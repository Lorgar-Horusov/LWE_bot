import os
import sys

import interactions
from interactions import Client
from load_modules import load_module
from tokken_setting import discord_token

client = Client()

TOKEN = discord_token()


@interactions.listen()
async def on_ready():
    print(f"We're online! We've logged in as {client.app.name}.")
    print(f"Our latency is {round(client.latency, 2)} ms.")


@interactions.slash_command(name="hello-world", description='A command that says "hello world!"')
async def hello_world(ctx: interactions.SlashContext):
    await ctx.send("hello world!")
    print("we ran.")


def start():
    load_module(client)
    client.start(TOKEN)

def stop():
    client.stop()

if __name__ == '__main__':
    # client.load_extension("interactions.ext.jurigged")
    load_module(client)
    client.start(TOKEN)
