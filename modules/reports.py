import datetime
from typing import List, Dict
from load_modules import load_config
from interactions import (
    Extension, SlashContext,
    slash_command, Client,
    SlashCommandChoice,
    File,
    Embed
)
from interactions.models.discord.channel import OverwriteType, PermissionOverwrite
from interactions.models.discord.enums import Permissions, ChannelType
import io
from util.attorney import MilesEdgeworth
import asyncio


def convert_seconds(seconds):
    days = seconds // 86400
    seconds %= 86400
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return f"{days} дн, {hours} ч, {minutes} мин, {seconds} сек"


def report_embed(case_id, reporter, accused, reason, time, ai_analysis=None):
    _analysis_part = ''
    if ai_analysis:
        _analysis_part = split_text(ai_analysis, 1024)
    embed = Embed(
        title="Система подачи жалоб",
        color=0x00ff00,
        timestamp=time
    )
    embed.set_author(
        name='Legendary Web Enforcer',
        url='https://github.com/Lorgar-Horusov/LWE_bot',
        icon_url="https://cdn.discordapp.com/avatars/1269739594736341227/160567261d976bdb1d4bd31745520b77"
    )
    embed.add_field(
        name="Новая жалоба:",
        value=case_id,
        inline=True
    )
    embed.add_field(
        name='Истец',
        value=f'<@{reporter}>',
        inline=True
    )
    embed.add_field(
        name="Обвиняемый:",
        value=f'<@{accused}>',
        inline=True
    )
    embed.add_field(
        name="Причина:",
        value=reason,
        inline=True
    )
    if not ai_analysis:
        embed.add_field(
            name=f"Анализ ИмИна для жалобы {case_id}",
            value="В процессе",
            inline=False
        )
    else:
        for idx, part in enumerate(_analysis_part, 1):
            if idx == 1:
                name = f"Анализ ИмИна для жалобы {case_id}"
            else:
                name = " "
            embed.add_field(name=name, value=part, inline=False)
    embed.set_footer(
        text="Примечание: Это анализ, сгенерированный ИИ. Окончательное решение остается за администрацией."
    )
    embed.set_image(
        url="https://i.ibb.co/66h37hP/Bratsworth.webp")
    return embed


def split_text(text, length):
    return [text[i:i + length] for i in range(0, len(text), length)]


class Reports(Extension):
    def __init__(self, client: Client):
        self.client = client
        self.attorney = MilesEdgeworth()
        self.config = load_config()

    async def collect_user_interactions(self, channel_id, reporter_id, reported_id) -> List[Dict]:
        logs_level = self.config["reports"]["logs_level"]
        """Collect messages between two users from the past 2 days"""
        channel = await self.client.fetch_channel(channel_id)

        two_days_ago = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=logs_level)

        collected_messages = []
        last_message_id = None

        while True:
            # Fetch messages
            if last_message_id:
                messages = await channel.fetch_messages(before=last_message_id, limit=100)
            else:
                messages = await channel.fetch_messages(limit=100)

            if not messages:
                break

            last_message_id = messages[-1].id

            for msg in messages:
                # Check if message is from either user and within the time range
                message_time = msg.timestamp
                if message_time < two_days_ago:
                    return collected_messages

                if msg.author.id in [reporter_id, reported_id]:
                    collected_messages.append({
                        "id": msg.id,
                        "author_id": msg.author.id,
                        "author_name": msg.author.username,
                        "content": msg.content,
                        "timestamp": msg.timestamp.isoformat(),
                        "attachments": [a.url for a in msg.attachments]
                    })

        return collected_messages

    @staticmethod
    def format_messages_for_file(messages: List[Dict]) -> str:
        """Format collected messages into a readable text format"""
        output = "ДИАЛОГ МЕЖДУ ПОЛЬЗОВАТЕЛЯМИ\n"
        output += "=" * 50 + "\n\n"

        # Sort messages by timestamp
        messages.sort(key=lambda x: x["timestamp"])

        for msg in messages:
            timestamp = datetime.datetime.fromisoformat(msg["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
            output += f"[{timestamp}] {msg['author_name']} ({msg['author_id']}):\n"
            output += f"{msg['content']}\n"

            if msg["attachments"]:
                output += "Вложения:\n"
                for url in msg["attachments"]:
                    output += f"- {url}\n"

            output += "\n" + "-" * 40 + "\n\n"

        return output

    @slash_command(
        name="report",
        description="Пожаловаться на пользователя",
        options=[
            {
                "name": "user",
                "description": "Пользователь, на которого вы жалуетесь",
                "type": 6,
                "required": True
            },
            {
                "name": "reason",
                "description": "Причина жалобы",
                "type": 3,
                "required": True
            }
        ]
    )
    async def report_user(self, ctx: SlashContext, user, reason):
        if self.config["reports"]["enabled"] is False:
            return await ctx.send("функция репортов отключена в файлах конфигурации.", ephemeral=True)

        await ctx.defer(ephemeral=True)
        temp_message = await ctx.send("Жалоба в обработке")
        # Extract the reported user from context
        reported_user = user
        guild = ctx.guild
        reporter_id = ctx.author.id
        reported_id = reported_user.id

        # Create unique case ID
        case_id = f"case-{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}"

        # Create permission overwrites - FIX: Use IDs instead of Role objects
        overwrites = [PermissionOverwrite(
            id=guild.default_role.id,
            type=OverwriteType.ROLE,
            deny=Permissions.VIEW_CHANNEL
        ), PermissionOverwrite(
            id=ctx.guild.me.id,
            type=OverwriteType.MEMBER,
            allow=Permissions.VIEW_CHANNEL | Permissions.SEND_MESSAGES
        )]

        # Add default role overwrite (deny view for everyone)

        # Create private admin channel
        case_channel = await guild.create_channel(
            name=case_id,
            channel_type=ChannelType.GUILD_TEXT.value,
            permission_overwrites=overwrites
        )

        # Collect messages between the reporter and reported user
        messages = await self.collect_user_interactions(ctx.channel_id, reporter_id, reported_id)

        # Format messages for the file
        file_content = self.format_messages_for_file(messages)

        file = File(
            file_name="dialog_history.txt",
            file=io.BytesIO(file_content.encode('utf-8'))
        )

        # Send initial information to case channel
        embed_message = report_embed(
            case_id,
            ctx.author.id,
            reported_user.id,
            reason,
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )

        await case_channel.send(files=file)
        embed_message_send = await case_channel.send(embed=embed_message)
        message_id = embed_message_send.id
        ai_analysis = self.attorney.judge(reporter_id, reported_id, file_content, reason)

        embed_message_new = report_embed(
            case_id,
            ctx.author.id,
            reported_user.id,
            reason,
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            ai_analysis
        )
        message_to_edit = await case_channel.fetch_message(message_id)
        await message_to_edit.edit(embed=embed_message_new)

        await ctx.edit(
            message=temp_message,
            content=f"Ваша жалоба на {reported_user.username} отправлена. ID жалобы: {case_id}",
        )

    @slash_command(
        name="close_case",
        description="Закрыть рассмотрение жалобы",
        options=[
            {
                "name": "decision",
                "description": "Решение модерации",
                "type": 3,
                "required": True,
                "choices": [
                    SlashCommandChoice(name="Нарушений не обнаружено", value="no_action"),
                    SlashCommandChoice(name="Предупреждение", value="warning"),
                    SlashCommandChoice(name="Временный мут", value="temp_mute"),
                    SlashCommandChoice(name="Временный бан", value="temp_ban"),
                    SlashCommandChoice(name="Перманентный бан", value="perm_ban")
                ]
            },
            {
                "name": "notes",
                "description": "Дополнительные заметки к решению",
                "type": 3,
                "required": False
            }
        ]
    )
    async def close_case(self, ctx: SlashContext, decision, notes=None):
        # Verify this is a case channel
        if not ctx.channel.name.startswith("case-"):
            await ctx.send("Эта команда может использоваться только в каналах рассмотрения жалоб", ephemeral=True)
            return

        # Verify the user has admin permissions
        member = await ctx.guild.fetch_member(ctx.author.id)
        is_admin = any(role.permissions.ADMINISTRATOR for role in member.roles)

        if not is_admin:
            await ctx.send("Только администраторы могут закрывать жалобы", ephemeral=True)
            return

        # Format the decision
        decision_map = {
            "no_action": "Нарушений не обнаружено",
            "warning": "Предупреждение",
            "temp_mute": "Временный мут",
            "temp_ban": "Временный бан",
            "perm_ban": "Перманентный бан"
        }

        decision_text = decision_map.get(decision, decision)
        time_to_deletion = self.config["reports"]["time_to_delete"]
        time_to_deletion_converted = convert_seconds(time_to_deletion)
        # Send a closure message
        closure_message = (
            f"**Жалоба {ctx.channel.name} - ЗАКРЫТА**\n\n"
            f"**Решение:** {decision_text}\n"
            f"**Модератор:** {ctx.author.mention}\n"
            f"**Время закрытия:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Канал будет удален через {time_to_deletion_converted}"
        )

        await ctx.channel.send(closure_message)
        if notes:
            closure_message += f"\n**Заметки:** {notes}\n"
        await ctx.send("Жалоба успешно закрыта", ephemeral=True)
        await asyncio.sleep(time_to_deletion)
        try:
            await ctx.channel.delete()
        except Exception as e:
            print(f"Error deleting channel: {e}")
