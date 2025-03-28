from interactions import (
    Extension,
    SlashContext,
    slash_command,
    Embed,
    Permissions,
    subcommand,
    SlashCommand
)
from rich.console import Console
from load_modules import load_config
from util.db_logic import ModerationDatabase as mdb

console = Console()


class Moderation(Extension):
    def __init__(self, client):
        self.client = client
        self.config = load_config()

    base = SlashCommand(name='warns', description='warns', default_member_permissions=Permissions.ADMINISTRATOR)

    @base.subcommand(
        sub_cmd_name="get",
        sub_cmd_description="Получить предупреждения пользователя",
        options=[
        {
            "name": "user",
            "description": "Пользователь, предупреждения которого нужно получить",
            "type": 6,
            "required": True
        }
    ]
    )
    async def get_warns(self, ctx: SlashContext, user):
        try:
            warns = mdb().get_warns(user.id, ctx.guild.name)
            if warns:
                embed = Embed(
                    title="Предупреждения",
                    color=0x00ff00,
                )
                embed.set_author(
                    name='Legendary Web Enforcer',
                    url='https://github.com/Lorgar-Horusov/LWE_bot',
                    icon_url="https://cdn.discordapp.com/avatars/1269739594736341227/160567261d976bdb1d4bd31745520b77"
                )
                for warn in warns:
                    embed.add_field(
                        name=f"Предупреждение за номером {warn[0]} от {warn[2]}",
                        value=f"Причина: {warn[1]}",
                        inline=False
                    )
                await ctx.send(embed=embed)
            else:
                await ctx.send("Пользователь не имеет предупреждений.")
        except Exception:
            console.print_exception(show_locals=True)

    @base.subcommand(
                sub_cmd_name="add",
                sub_cmd_description="Выдать предупреждение пользователю",
                options=[
                    {
                        "name": "user",
                        "description": "Пользователь, предупреждения которого нужно получить",
                        "type": 6,
                        "required": True
                    },

                    {
                        "name": "reason",
                        "description": "Причина предупреждения",
                        "type": 3,
                        "required": False
                    }
                ]
                )
    async def add_warn(self, ctx: SlashContext, user, reason: str = "Не указана"):
        try:
            member = ctx.guild.get_member(user.id)
            if member:
                await ctx.send(f"{member.mention} было выдано предупреждение по причине: {reason}")
                mdb().add_warn(user.id, reason, ctx.guild.name)
            else:
                await ctx.send("Пользователь не найден в этом сервере.")
        except Exception:
            console.print_exception(show_locals=True)

    @base.subcommand(
        sub_cmd_name="remove",
        sub_cmd_description="Очистить предупреждения пользователя",
        options=[
            {
                "name": "user",
                "description": "Пользователь, предупреждения которого нужно очистить",
                "type": 6,
                "required": True
            },
            {
                "name": "warn_id",
                "description": "Номер предупреждения, которое нужно очистить",
                "type": 4,
                "required": True
            }
        ]
    )
    async def warn_remove(self, ctx: SlashContext, user, warn_id):
        try:
            mdb().delete_warn(user.id, ctx.guild.name, warn_id)
            await ctx.send(f"Предупреждения пользователя {user.mention} были очищены.")
        except Exception:
            console.print_exception(show_locals=True)
            await ctx.send("Ошибка при очистке предупреждений.")
