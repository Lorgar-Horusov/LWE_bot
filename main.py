import interactions
from interactions import Client
from load_modules import load_module
from tokken_setting import discord_token

client = Client()

TOKEN = discord_token()


@interactions.listen()
async def on_ready():
    # We can use the client "app" attribute to get information about the bot.
    print(f"We're online! We've logged in as {client.app.name}.")

    # We're also able to use property methods to gather additional data.
    print(f"Our latency is {round(client.latency, 2)} ms.")


@interactions.listen("on_message_create")
async def name_this_however_you_want(message_create: interactions.events.MessageCreate):
    message: interactions.Message = message_create.message
    print(f"We've received a message from {message.author.username}. The message is: {message.content}.")


@interactions.slash_command(name="hello-world", description='A command that says "hello world!"')
async def hello_world(ctx: interactions.SlashContext):
    await ctx.send("hello world!")
    print("we ran.")


if __name__ == '__main__':
    # client.load_extension("interactions.ext.jurigged")
    load_module(client)
    client.start(TOKEN)
