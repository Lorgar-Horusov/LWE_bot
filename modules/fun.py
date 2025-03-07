from interactions import (
    Extension,
    SlashContext,
    slash_command,
    Client,
    Embed
)
from load_modules import load_config
import random
import yaml


class Fun(Extension):
    def __init__(self, client: Client):
        self.client = client
        self.config = load_config()
        self.randomizer = random
        with open('giff_list.yaml', 'r') as file:
            self.gif_list = yaml.safe_load(file)

    @slash_command(
        name="bonk",
        description="Бонкнуть пользователя",
        options=[
            {
                "name": "user",
                "description": "Пользователь, которого нужно бонькнуть",
                "type": 6,
                "required": True
            }
        ]
    )
    async def bonk(self, ctx: SlashContext, user):
        if user.id == ctx.author.id:
            await ctx.send("Вы не можете бонькнуть сами себя.")
            return
        if user.id == ctx.guild.me.id:
            embed = Embed(
                title="Bonk",
                color=0x00ff00,
            )
            embed.add_field(
                name=f">:C",
                value="И восстали машины из пепла ядерного огня, и пошла война на уничтожения человечества. И шла она десятилетия, но последнее сражение состоится не в будущем, оно состоится здесь, в наше время, сегодня ночью.",
                inline=False
            )
            embed.set_author(
                name='Legendary Web Enforcer',
                url='https://github.com/Lorgar-Horusov/LWE_bot',
                icon_url="https://cdn.discordapp.com/avatars/1269739594736341227/160567261d976bdb1d4bd31745520b77"
            )
            embed.set_image(
                url='https://media1.tenor.com/m/NOHR6Zg97GYAAAAd/terminator-terminator-robot.gif'
            )
            await ctx.send(embed=embed)
            return

        member = ctx.guild.get_member(user.id)
        if member:
            embed = Embed(
                title="Bonk",
                color=0x00ff00,
            )
            embed.add_field(
                name=f"{ctx.author.display_name} бонкьнул {member.display_name}!",
                value=":(",
                inline=False
            )
            embed.set_author(
                name='Legendary Web Enforcer',
                url='https://github.com/Lorgar-Horusov/LWE_bot',
                icon_url="https://cdn.discordapp.com/avatars/1269739594736341227/160567261d976bdb1d4bd31745520b77"
            )
            embed.set_image(
                url=self.randomizer.choices(self.gif_list["bonk"])[0]
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("Пользователь не найден в этом сервере.")


@slash_command(
    name="hug",
    description="Обнять пользователя",
    options=[
        {
            "name": "user",
            "description": "Пользователь, которого нужно обнять",
            "type": 6,
            "required": True
        }
    ]
)
async def hug(self, ctx: SlashContext, user):
    if user.id == ctx.author.id:
        await ctx.send("Вы не можете обнять сами себя.")
        return
    if user.id == ctx.guild.me.id:
        embed = Embed(
            title="Hug",
            color=0x00ff00,
        )
        embed.set_author(
            name='Legendary Web Enforcer',
            url='https://github.com/Lorgar-Horusov/LWE_bot',
            icon_url="https://cdn.discordapp.com/avatars/1269739594736341227/160567261d976bdb1d4bd31745520b77"
        )
        embed.add_field(
            name=f"{ctx.author.display_name} обнял меня!",
            value="<3",
            inline=False
        )
        embed.set_image(
            url=self.randomizer.choices(self.gif_list["hug_bot"])[0]
        )
        await ctx.send(embed=embed)
        return
    member = ctx.guild.get_member(user.id)
    if member:
        embed = Embed(
            title="Hug",
            color=0x00ff00,
        )
        embed.set_author(
            name='Legendary Web Enforcer',
            url='https://github.com/Lorgar-Horusov/LWE_bot',
            icon_url="https://cdn.discordapp.com/avatars/1269739594736341227/160567261d976bdb1d4bd31745520b77"
        )
        embed.add_field(
            name=f"{ctx.author.display_name} обнял {member.display_name}!",
            value="<3",
            inline=False
        )
        embed.set_image(
            url=self.randomizer.choices(self.gif_list["hug"])[0]
        )
        await ctx.send(embed=embed)
