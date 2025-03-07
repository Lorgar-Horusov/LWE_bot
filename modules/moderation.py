from interactions import (
    Extension,
    SlashContext,
    slash_command,
    Client,
    SlashCommandChoice,
    File,
    Embed
)
import datetime
from load_modules import load_config

class Moderation(Extension):
    def __init__(self, client):
        self.client = client
        self.config = load_config()

    @slash_command(
        name="timeout",
        description="Выдать временную мут",
        options=[
            {
                "name": "user",
                "description": "Пользователь, которому выдать мут",
                "type": 6,
                "required": True
            },
            {
                "name": "duration",
                "description": "Продолжительность мута",
                "type": 3,
                "required": True,
                "choices": [
                    SlashCommandChoice(name="1 минута", value="60"),
                    SlashCommandChoice(name="5 минут", value="300"),
                    SlashCommandChoice(name="10 минут", value="600"),
                    SlashCommandChoice(name="1 час", value="3600"),
                    SlashCommandChoice(name="1 день", value="86400"),
                    SlashCommandChoice(name="1 неделя", value="604800")
                ]
            },
            {
                "name": "reason",
                "description": "Причина мута",
                "type": 3,
                "required": False
            }
        ]
    )
    async def timeout(self, ctx: SlashContext, user, duration: int, reason: str = None):
        if not reason:
            reason = "Не указана"
        duration = int(duration)
        try:
            member = ctx.guild.get_member(user.id)
            if member:
                await member.timeout(duration)
                await ctx.send(f"{member.mention} был выдан временный мут на {duration} секунд по причине: {reason}")
            else:
                await ctx.send("Пользователь не найден в этом сервере.")
        except Exception as e:
            await ctx.send(f"Произошла ошибка при выдаче мута: {e}")

    @slash_command(
        name="warn",
        description="Выдать предупреждение",
        options=[
            {
                "name": "user",
                "description": "Пользователь, которому выдать предупреждение",
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
    async def warn(self, ctx: SlashContext, user, reason: str = None):
        if not reason:
            reason = "Не указана"
        try:
            member = ctx.guild.get_member(user.id)
            if member:
                await ctx.send(f"{member.mention} был выдан предупреждение по причине: {reason}")
            else:
                await ctx.send("Пользователь не найден в этом сервере.")
        except Exception as e:
            await ctx.send(f"Произошла ошибка при выдаче предупреждения: {e}")