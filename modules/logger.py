from interactions import Extension, listen
from interactions.api.events import MessageDelete, MessageUpdate

from util.db_logic import ChatLogger


class DiscordLogger(Extension):
    def __init__(self, client):
        self.client = client
        self.chat_logger = ChatLogger()

    @listen(MessageDelete)
    async def on_message_delete(self, event):
        if event.message is None:
            print('Error: event.message is None')
            return

        if event.message.author.bot:
            return
        user = event.message.author
        message = event.message.content
        try:
            self.chat_logger.message_deletion_logger(autor=str(user), message=message, server_id=event.message.guild.id)
        except Extension as e:
            print('Extension error', e)

    @listen(MessageUpdate)
    async def on_message_update(self, event):
        # Проверка на наличие обеих версий сообщения
        if event.before is None or event.after is None:
            print('Error: event.before or event.after is None')
            return

        # Проверка, является ли автор ботом
        if event.before.author.bot:
            return

        user = event.before.author
        original_message = event.before.content
        edited_message = event.after.content

        # Проверка на пустые сообщения
        if original_message and edited_message:
            self.chat_logger.message_edition_logger(
                autor=str(user),
                original_message=original_message,
                edited_message=edited_message,
                server_id=event.before.guild.id
            )