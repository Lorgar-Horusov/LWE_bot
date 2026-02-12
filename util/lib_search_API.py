from pprint import pprint
import httpx
import asyncio


async def search_manga(manga_name, count: int):
    url = f"https://api2.mangalib.me/api/manga?fields[]=rate_avg&fields[]=rate&fields[]=releaseDate&q={manga_name}&site_id[]=1"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            json_data = response.json()
            answer = []

            # Проверяем структуру JSON
            if isinstance(json_data, dict) and "data" in json_data:
                manga_list = json_data["data"]
            elif isinstance(json_data, list):
                manga_list = json_data
            else:
                print("Неподдерживаемая структура данных.")
                return []

            # Обрабатываем первые `count` элементов
            for item in manga_list[:count]:
                manga_data = {
                    "name": item.get("name"),
                    "rus_name": item.get("rus_name"),
                    "coverImage": item['cover']['defaultuv '],
                    "href": f"https://mangalib.me/ru/manga/{item.get('slug_url')}"
                }
                answer.append(manga_data)

            return answer
        else:
            print(f"Ошибка при запросе: {response.status_code}")
            return []

if __name__ == '__main__':
    async def main():
        manga_name = "one piece"
        result = await search_manga(manga_name, count=1)
        pprint(result)

    asyncio.run(main())