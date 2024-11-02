from interactions import Extension, listen
from interactions.api.events import MessageCreate
import io
import aiohttp

from util.AI_Features import speach_to_text

class voice_to_text(Extension):
    def __init__(self, client):
        self.client = client

    @listen(MessageCreate)
    async def on_message_create(self, event: MessageCreate):
        if event.message.author.bot:
            return

        if event.message.attachments:
            for attachment in event.message.attachments:
                if attachment.content_type.startswith("audio/ogg") and attachment.filename == 'voice-message.ogg':
                    audio_url = attachment.url
                    holder = await event.message.reply('anti voice message system online')
                    async with aiohttp.ClientSession() as session:
                        async with session.get(audio_url) as resp:
                            if resp.status == 200:
                                audio_data = io.BytesIO(await resp.read())
                                text = await speach_to_text(audio_data)
                                await holder.edit(content=f"Transcribed text: {text}")
                            else:
                                await holder.edit(content="Failed to download the audio file.")


