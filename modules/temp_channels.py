from interactions import Extension, SlashContext, slash_command, ActionRow, Button, ButtonStyle
from interactions.api.events import Component
from interactions.models.discord.channel import PermissionOverwrite, OverwriteType
from interactions.models.discord.enums import Permissions
from interactions.models.discord.channel import VoiceChannel
import asyncio
from load_modules import load_config


class TemporallyChannels(Extension):
    def __init__(self, client):
        self.client = client
        self.selected_count = None
        self.selected_type = None
        self.active_channels = {}

    async def schedule_channel_deletion(self, channel: VoiceChannel, timeout: int):
        self.active_channels[channel.id] = True
        try:
            while len(channel.voice_members) > 0:
                await asyncio.sleep(10)
            await asyncio.sleep(timeout * 60)
            if len(channel.voice_members) == 0:
                try:
                    await channel.delete()
                    print(f"Channel {channel.name} deleted due to inactivity.")
                except Exception as e:
                    print(f"Failed to delete channel {channel.name}: {e}")
        except asyncio.CancelledError:
            print(f"Channel {channel.name} deletion task was cancelled.")
        finally:
            self.active_channels.pop(channel.id, None)

    @slash_command(description="Create a temporary voice channel")
    async def create_voice(self, ctx: SlashContext):
        config = load_config()
        if config["temp_channels"]["enabled"] is False:
            return await ctx.send("Temporary channels are disabled.", ephemeral=True)
        time_to_deletion = config["temp_channels"]["time_to_deletion"]
        count_buttons = ActionRow(
            Button(
                style=ButtonStyle.GREEN,
                label="2 Members",
                custom_id="count_2",
            ),
            Button(
                style=ButtonStyle.GREEN,
                label="4 Members",
                custom_id="count_4",
            ),
            Button(
                style=ButtonStyle.GREEN,
                label="6 Members",
                custom_id="count_6",
            ),
            Button(
                style=ButtonStyle.GREEN,
                label="Unlimited",
                custom_id="count_unlim",
            ),
        )

        type_channel = ActionRow(
            Button(
                style=ButtonStyle.GREEN,
                label="Private",
                custom_id="type_private",
            ),
            Button(
                style=ButtonStyle.GREEN,
                label="Public",
                custom_id="type_public",
            ),
        )
        message = await ctx.send(
            "Choose the number of participants for the temporary voice channel:",
            components=[count_buttons], ephemeral=True
        )

        async def check(component: Component):
            if component.ctx.author == ctx.author and component.ctx.message == message:
                return True
            else:
                await component.ctx.send("This is not your message to react to!", ephemeral=True)
                return False

        try:
            user_component: Component = await self.client.wait_for_component(components=count_buttons, timeout=60,
                                                                             check=check)
        except TimeoutError:
            await message.edit(content="Time out! No selection made.", components=[])
            return
        else:
            selected_count = user_component.ctx.custom_id.split("_")[1]
            await user_component.ctx.defer(edit_origin=True)
            await user_component.ctx.edit(message=message,
                                          content=f"You selected {selected_count} members. Now choose the type of channel:",
                                          components=[type_channel])
        try:
            user_component: Component = await self.client.wait_for_component(components=type_channel, timeout=60,
                                                                             check=check)
        except TimeoutError:
            await message.edit(content="Time out! No selection made.", components=[])
            return
        else:
            selected_type = "Private" if user_component.ctx.custom_id == "type_private" else "Public"
            await user_component.ctx.defer(edit_origin=True)
            await user_component.ctx.edit(
                content=f"Creating a {selected_type} channel for {selected_count} participants...",
                components=[],
            )
            user_limit = None if selected_count == "unlim" else int(selected_count)
            private = selected_type == "Private"
            await self.create_voice_channel(ctx, f"{ctx.author.display_name} Voice Channel", user_limit, private,
                                            timeout=time_to_deletion)

    async def create_voice_channel(self, ctx: SlashContext, channel_name: str, user_limit: int, private: bool,
                                   timeout: int = 1):
        category = ctx.guild.get_channel(ctx.channel.parent_id) if ctx.channel.parent_id else None
        permission_overwrites = []
        if private:
            permission_overwrites.append(
                PermissionOverwrite(
                    id=ctx.guild.default_role.id,
                    type=OverwriteType.ROLE,
                    deny=Permissions.VIEW_CHANNEL,
                )
            )
            permission_overwrites.append(
                PermissionOverwrite(
                    id=ctx.author.id,
                    type=OverwriteType.MEMBER,
                    allow=Permissions.VIEW_CHANNEL | Permissions.CONNECT | Permissions.MOVE_MEMBERS,
                )
            )
            permission_overwrites.append(
                PermissionOverwrite(
                    id=ctx.guild.me.id,
                    type=OverwriteType.MEMBER,
                    allow=Permissions.VIEW_CHANNEL | Permissions.CONNECT | Permissions.MOVE_MEMBERS,
                )
            )
        new_channel = await ctx.guild.create_voice_channel(
            name=channel_name,
            user_limit=user_limit,
            category=category,
            permission_overwrites=permission_overwrites,
        )
        await ctx.send(f"Voice channel **{new_channel.name}** created!", ephemeral=True)
        asyncio.create_task(self.schedule_channel_deletion(new_channel, timeout))
