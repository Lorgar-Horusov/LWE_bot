from pprint import pprint
from playwright.async_api import async_playwright

async def search_manga(manga_name):
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)  # Безголовый режим
        page = await browser.new_page()
        answer = []

        # Перехватываем все запросы
        async def handle_response(response):
            if "application/json" in response.headers.get("content-type", ""):
                try:
                    json_data = await response.json()  # Преобразуем в JSON
                    for item in json_data:  # Проходим по всем элементам списка
                        # Извлекаем только нужные поля
                        manga_data = {
                            "name": item.get("name"),
                            "rus_name": item.get("rus_name"),
                            "summary": item.get("summary"),
                            "coverImage": item.get("coverImage"),
                            "href": item.get("href")
                        }
                        answer.append(manga_data)
                except Exception as e:
                    print(f"Ошибка: {e}")

        page.on("response", handle_response)

        # Формируем URL для поиска манги
        url = f"https://mangalib.me/search?type=manga&q={manga_name}"
        await page.goto(url)

        # Ждем загрузки страницы и выполнения всех скриптов
        await page.wait_for_timeout(5000)

        # Закрываем браузер
        await browser.close()
        return answer


if __name__ == '__main__':
    manga_name = "one piece"
    result = search_manga(manga_name)
    result = result
    pprint(result)