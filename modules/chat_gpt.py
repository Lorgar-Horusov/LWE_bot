from interactions import Extension
from interactions import Modal, ParagraphText, SlashContext, slash_command, ModalContext, Typing

from util.AI_Features import chat_gpt
from load_modules import load_config

class ChatGPT(Extension):
    def __init__(self, client):
        self.client = client

    @slash_command()
    async def chatgpt(self, ctx: SlashContext):
        config = load_config()
        if config['chat_gpt']['enabled']:
            model = config['chat_gpt']['model']
            tokens = config['chat_gpt']['max_tokens']
        else:
            return await ctx.send("This command is currently disabled.", ephemeral=True)

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
            answer = await chat_gpt(long_text, model, tokens)
        await ctx.edit(message=response_msg.id, content=answer)
