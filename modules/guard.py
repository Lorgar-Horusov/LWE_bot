from urllib.parse import urlparse

from rich.console import Console
from interactions import Extension, listen, Embed
from interactions.api.events import MessageCreate

from util.virustotal_API import VirusTotal
import validators
from load_modules import load_config
from util.db_logic import ModerationDatabase

console = Console()


class Guard(Extension):
    def __init__(self, client):
        self.client = client
        self.virus_Total = VirusTotal()
        self.load_config = load_config()
        self.message_logs = {}

    @listen(MessageCreate)
    async def url_checker(self, event):
        if event.message.author.bot or not validators.url(event.message.content):
            return
        if self.check_url(event.message.content):
            console.log(f"URL whitelisted: {urlparse(event.message.content).netloc}")
            return
        console.log(f"Start checking url: {event.message.content}")
        virus_total_result = await self.virus_Total.url_scan(event.message.content)
        sens = self.virus_Total.harm_reduction(virus_total_result['malicious'], virus_total_result['harmless'])
        if sens >= self.load_config['guard']['sensitivity']:
            await event.message.delete()
            await event.message.channel.send(f"URL removed! Malicious content")
            console.log(f"URL deleted: {event.message.content}, sensitivity: {sens}")
            try:
                mdb = ModerationDatabase()
                mdb.add_warn(event.message.author.id, f'Malicious content {event.message.content}',
                             event.message.guild.name)
                embed = Embed(
                    title="Предупреждение",
                    description=f"Вы получили предупреждение за использование мошеннической ссылки",
                    color=0xff0000,
                )
                embed.set_author(
                    name='Legendary Web Enforcer',
                    url='https://github.com/Lorgar-Horusov/LWE_bot',
                    icon_url="https://cdn.discordapp.com/avatars/1269739594736341227/160567261d976bdb1d4bd31745520b77"
                )
                embed.add_field(
                    name="Ссылка",
                    value=event.message.content,
                    inline=True
                )
                embed.add_field(
                    name="Вероятность мошеннической ссылки:",
                    value=sens,
                    inline=True
                )
                embed.add_field(
                    name="Сервер",
                    value=event.message.guild.name,
                    inline=True
                )
                await event.message.author.send(embed=embed)
            except Exception:
                console.print_exception(show_locals=True)
        else:
            console.log(
                f"URL not deleted: {event.message.content}, sensitivity {sens} < {self.load_config['guard']['sensitivity']}")
            try:
                embed = Embed(
                    title="Оценка ссылки",
                    description=f"_Система автоматической фильтрации ссылок_",
                    color=0xff0000,
                )
                embed.set_author(
                    name='Legendary Web Enforcer',
                    url='https://github.com/Lorgar-Horusov/LWE_bot',
                    icon_url="https://cdn.discordapp.com/avatars/1269739594736341227/160567261d976bdb1d4bd31745520b77"
                )
                embed.add_field(
                    name="Ссылка",
                    value=event.message.content,
                    inline=True
                )
                embed.add_field(
                    name="Вероятность мошеннической ссылки:",
                    value=sens,
                    inline=True
                )
                embed.add_field(
                    name="Сервер",
                    value=event.message.guild.name,
                    inline=True
                )
                await event.message.channel.send(embed=embed)
            except Exception:
                console.print_exception(show_locals=True)
    def check_url(self, url):
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        for urls in self.load_config['guard']['whitelist']:
            if domain == urls:
                return True
            if 'www.' + domain == urls:
                return True
            if domain.lstrip('www.') == urls.lstrip('www.'):
                return True
        return False

    # @listen(MessageCreate)
    # async def anti_spam(self, event):
    #     message_limit = self.load_config['guard']['message_limit']
    #     time_limit = self.load_config['guard']['time_limit']
    #
    #     if not event.message.guild.id or event.message.author.bot:
    #         return
    #
    #     user_id = event.message.author.id
    #     now = datetime.datetime.now(datetime.UTC)
    #
    #     if user_id not in self.message_logs:
    #         self.message_logs[user_id]= deque()
    #
    #     log = self.message_logs[user_id]
    #     log.append(now)
    #
    #     while log and (now - log[0]).total_seconds() > time_limit:
    #         log.popleft()
    #
    #     if len(log) > message_limit:
    #         try:
    #             await event.message.author.timeout(1, reason="Spam detected")
    #             await event.message.channel.send(f"{event.message.author.mention}, spam detected!")
    #         except Exception:
    #             console.print_exception(show_locals=True)
    #         try:
    #             mdb = ModerationDatabase()
    #             mdb.add_warn(event.message.author.id, 'Spam', event.message.guild.name)
    #             self.message_logs[user_id].clear()
    #         except Exception:
    #             console.print_exception(show_locals=True)
