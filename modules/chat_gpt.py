from interactions import Extension
from interactions import Modal, ParagraphText, SlashContext, slash_command, ModalContext, Typing

from util.AI_Features import chat_gpt
from load_modules import load_config

def split_text(text, length):
    return [text[i:i + length] for i in range(0, len(text), length)]


class ChatGPT(Extension):
    def __init__(self, client):
        self.client = client

    @slash_command(
        name="ai-chat",
        description="спросить у ИИ",
        options=[
            {
                "name": "ask",
                "description": "Что ты хочешь узнать?",
                "type": 3,
                "required": True
            }
        ]
    )
    async def chatgpt(self, ctx: SlashContext, ask):
        config = load_config()
        if config['chat_gpt']['enabled']:
            model = config['chat_gpt']['model']
            tokens = config['chat_gpt']['max_tokens']
            ephem = config['chat_gpt']['ephemeral']
        else:
            return await ctx.send("This command is currently disabled.", ephemeral=True)

        await ctx.defer(ephemeral=ephem)
        async with Typing(ctx.channel):
            response_msg = await ctx.send('Запрос принят генерирую буковки <:2f40a4ad22784f732cb053a1a69ffedd:>', ephemeral=ephem)
            answer = await chat_gpt(ask, model, tokens)
            if len(answer) > 2000:
                await ctx.send(content='Слишком длинный ответ, отправляю несколькими сообщениями', delete_after=5)
        await response_msg.delete()
        for idx, chunk in enumerate(split_text(answer, 2000)):
            if idx == 0:
                await ctx.send(content=chunk, ephemeral=ephem)
            else:
                await ctx.channel.send(content=chunk, ephemeral=ephem)

