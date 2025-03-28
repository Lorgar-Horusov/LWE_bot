import keyring
from rich.console import Console
import asyncio
import aiohttp

console = Console()


class VirusTotal:
    def __init__(self):
        self.api_key = keyring.get_password("virustotal", "api_key")
        if self.api_key is None:
            self.api_key = input('Write Token: ')
            keyring.set_password("virustotal", "api_key", self.api_key)

        self.api_key = keyring.get_password("virustotal", "api_key")
        self.base_url = 'https://www.virustotal.com/api/v3/'
        self.headers = {'x-apikey': self.api_key}

    async def url_scan(self, url):
        base_url = f'{self.base_url}urls'
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(base_url, headers=self.headers, data={'url': url}) as response:
                    if response.status == 200:
                        response_json = await response.json()
                        analysis_url = response_json.get('data', {}).get('links', {}).get('self')
                        if not analysis_url:
                            console.log("Ошибка: Не удалось получить ссылку на анализ")
                            return None
                        result = await self._get_analysis_result(session, analysis_url)
                        return result['data']['attributes']['stats']
                    else:
                        console.log(f'Ошибка при отправке URL: {response.status}')
            except Exception as e:
                console.log(f'Ошибка запроса: {e}')
                return None

    async def _get_analysis_result(self, session, analysis_url, retries=5, delay=5):
        for _ in range(retries):
            async with session.get(analysis_url, headers=self.headers) as response:
                if response.status == 200:
                    result = await response.json()
                    status = result.get('data', {}).get('attributes', {}).get('status')
                    if status == 'completed':
                        return result
                    console.log("Анализ ещё не завершён, ждём...")
                    await asyncio.sleep(delay)
        console.log("Не удалось получить результат анализа.")
        return None

    @staticmethod
    def harm_reduction(harm, harmless):
        try:
            if harmless == 0:
                return 100.0 if harm > 0 else 0.0  # Если нет "безопасных" проверок, но есть вредоносные, то 100%
            return round((harm / (harm + harmless)) * 100, 2)
        except ZeroDivisionError:
            return 0.0
if __name__ == '__main__':
    vt = VirusTotal()
    result = asyncio.run(vt.url_scan('https://www.perplexity.ai/'))
    console.log(result)