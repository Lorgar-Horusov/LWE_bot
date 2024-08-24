from interactions import Extension
from interactions import Modal, ParagraphText, SlashContext, slash_command, ModalContext, Typing

from util.AI_Features import chat_gpt


class ChatGPT(Extension):
    def __init__(self, client):
        self.client = client

    @slash_command()
    async def chatgpt(self, ctx: SlashContext):
        my_modal = Modal(
            ParagraphText(label="Enter a query", custom_id="long_text"),
            title="My Modal",
            custom_id="my_modal",
        )
        await ctx.send_modal(modal=my_modal)
        modal_ctx: ModalContext = await ctx.bot.wait_for_modal(my_modal)

        long_text = modal_ctx.responses["long_text"]
        async with Typing(ctx.channel):
            response_msg = await modal_ctx.send('Запрос принят ожидайте ответ', ephemeral=True)
            answer = await chat_gpt(long_text)
        await ctx.edit(message=response_msg.id, content=answer)
