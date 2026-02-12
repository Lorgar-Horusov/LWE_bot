from interactions import (
Extension,
SlashContext,
slash_command,
Client,
)
from load_modules import load_config

from interactions.models.discord.components import (
ContainerComponent,
SectionComponent,
Button
)

class Activities(Extension):
    def __init__(self, client: Client):
        self.client = client
        self.config = load_config()

    @slash_command(
        name="vote",
        description = "",
        options=[
            {
                "name": "question",
                "description": "test",
                "type": 6,
                "required": True
            }
        ]
    )
    async def vote(self, ctx: SlashContext, question):
        pass

