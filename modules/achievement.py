from io import BytesIO
from random import choices
from string import ascii_letters, digits

from interactions import (
    Extension,
    SlashContext,
    slash_command,
    Client,
    Embed,
    File,
    Permissions,
    Modal,
    ShortText,
    ModalContext,
    subcommand,
    SlashCommand,
)
from rich.console import Console

from load_modules import load_config
from util.achievements_API import AchievementGenerator
from util.db_logic import AchievementsDataBase

console = Console()


class Achievements(Extension):
    def __init__(self, client: Client):
        self.client = client
        self.config = load_config()
        self.achievement_generator = AchievementGenerator()
        self.db = AchievementsDataBase()

    @slash_command(
        name="custom_achievement",
        description="Выдать кастомное достижение",
        options=[
            {
                "name": "achievement_name",
                "description": "Достижение, которое нужно получить",
                "type": 3,
                "required": True
            },

            {
                "name": "achievement_description",
                "description": "Описание достижения",
                "type": 3,
                "required": True
            },
            {
                "name": "user",
                "description": "Кому выдать достижения",
                "type": 6,
                "required": True
            }
        ]
    )
    async def custom_achievement(self, ctx: SlashContext, achievement_name: str, achievement_description: str, user):
        if user.id == ctx.guild.me.id:
            await ctx.send("Вы не можете выдать достижение боту.")
            return
        try:
            achievement_image: BytesIO = self.achievement_generator.generate(
                achievement_name,
                achievement_description
            )
            achievement_image.seek(0)
            filename = f"{achievement_name}.png"
            file = File(file=achievement_image, file_name=filename)
            embed = Embed(
                title="Выдано достижение",
                color=0x00ff00,
            )
            embed.set_image(url=f"attachment://{filename}")  # Must match file_name exactly
            embed.set_author(
                name='Legendary Web Enforcer',
                url='https://github.com/Lorgar-Horusov/LWE_bot',
                icon_url="https://cdn.discordapp.com/avatars/1269739594736341227/160567261d976bdb1d4bd31745520b77"
            )
            embed.add_field(
                name="Пользователь:",
                value=user.mention,
                inline=False
            )
            embed.add_field(
                name=f"Достижение: {achievement_name}",
                value=f"Описание: {achievement_description}",
                inline=False
            )
            await ctx.send(files=[file], embed=embed)


        except Exception:
            console.print_exception(show_locals=True)
            await ctx.send("Ошибка при выдаче достижения.")

    achievement_base = SlashCommand(name='achievement', description='Достижения', default_member_permissions=Permissions.ADMINISTRATOR)
    @achievement_base.subcommand(
        sub_cmd_name="add",
        sub_cmd_description="Выдать достижение",
        options=[
            {
                "name": "achievement_name",
                "description": "Достижение, которое нужно получить",
                "type": 3,
                "required": True
            },

            {
                "name": "achievement_description",
                "description": "Описание достижения",
                "type": 3,
                "required": True
            },
            {
                "name": "user",
                "description": "Кому выдать достижения",
                "type": 6,
                "required": True
            }
        ]
    )
    async def add_achievement(self, ctx: SlashContext, achievement_name: str, achievement_description: str, user):
        if user.id == ctx.guild.me.id:
            await ctx.send("Вы не можете выдать достижение боту.")
            return
        try:
            achievement_image: BytesIO = self.achievement_generator.generate(
                achievement_name,
                achievement_description
            )
            achievement_image.seek(0)
            filename = f"{achievement_name}.png"
            file = File(file=achievement_image, file_name=filename)
            embed = Embed(
                title="Выдано достижение",
                color=0x00ff00,
            )
            embed.set_image(url=f"attachment://{filename}")  # Must match file_name exactly
            embed.set_author(
                name='Legendary Web Enforcer',
                url='https://github.com/Lorgar-Horusov/LWE_bot',
                icon_url="https://cdn.discordapp.com/avatars/1269739594736341227/160567261d976bdb1d4bd31745520b77"
            )
            embed.add_field(
                name="Пользователь:",
                value=user.mention,
                inline=False
            )
            embed.add_field(
                name=f"Достижение: {achievement_name}",
                value=f"Описание: {achievement_description}",
                inline=False
            )
            await ctx.send(files=[file], embed=embed)

            self.db.add_achievement(user.id, achievement_name, achievement_description, ctx.guild.name)
        except Exception:
            console.print_exception(show_locals=True)
            await ctx.send("Ошибка при выдаче достижения.")

    @slash_command(
        name='achievements',
        description='Показать достижения пользователя',
        options=[
            {
                "name": "user",
                "description": "Пользователь",
                "type": 6,
                "required": False
            }
        ]
    )
    async def achievements(self, ctx: SlashContext, user=None):
        if user is None:
            user = ctx.author
        achievements = self.db.get_achievements(user.id, ctx.guild.name)
        if achievements is None:
            await ctx.send("У пользователя нет достижений.")
            return
        embed = Embed(
            title=f"Достижения пользователя {user.display_name}",
            color=0x00ff00,
        )
        embed.set_author(
            name='Legendary Web Enforcer',
            url='https://github.com/Lorgar-Horusov/LWE_bot',
            icon_url="https://cdn.discordapp.com/avatars/1269739594736341227/160567261d976bdb1d4bd31745520b77"
        )
        for achievement in achievements:
            embed.add_field(
                name=f"Достижение: {achievement[0]}",
                value=f"Описание: {achievement[1]}",
                inline=False
            )
        await ctx.send(embed=embed)

    @achievement_base.subcommand(
        sub_cmd_name="clear",
        sub_cmd_description="Очистить достижения пользователя",
        options=[
            {
                "name": "user",
                "description": "Пользователь",
                "type": 6,
                "required": True
            }
        ]
    )
    async def clear_achievements(self, ctx: SlashContext, user):
        password = ''.join(choices(ascii_letters + digits, k=5))
        modal = Modal(
            ShortText(
                label=f"Внимание! Пароль для удаления: {password}",
                placeholder=f"Введите пароль для очистки достижений пользователя {ctx.user.display_name}",
                custom_id="password"
            ),
            title=f"Удалить все достижения {ctx.user.display_name}",
            custom_id="clear_achievements"
        )
        await ctx.send_modal(modal)
        try:
            modal_ctx: ModalContext = await ctx.bot.wait_for_modal(modal, timeout=30)
        except TimeoutError:
            await ctx.send("Время ожидания истекло.", ephemeral=True)
            return
        if modal_ctx.responses["password"] == password:
            try:
                self.db.clear_achievements(user.id, ctx.guild.name)
                await modal_ctx.send("Достижения очищены.",  ephemeral=True)
            except Exception:
                console.print_exception(show_locals=True)
                await modal_ctx.send("Ошибка при очистке достижений.", ephemeral=True)
        else:
            await modal_ctx.send("Неверный пароль.", ephemeral=True)

    @achievement_base.subcommand(
        sub_cmd_name="delete",
        sub_cmd_description="Удалить достижение пользователя",
        options=[
            {
                "name": "achievement_name",
                "description": "Достижение, которое нужно удалить",
                "type": 3,
                "required": True
            },
            {
                "name": "user",
                "description": "Пользователь",
                "type": 6,
                "required": True
            }
        ]
    )
    async def delete_achievement(self, ctx: SlashContext, achievement_name: str, user):
        try:
            self.db.remove_achievement(user.id, achievement_name, ctx.guild.name)
            await ctx.send(f"Достижение {achievement_name} удалено у пользователя {user.name}.")
        except Exception:
            console.print_exception(show_locals=True)
            await ctx.send("Ошибка при удалении достижения.")
