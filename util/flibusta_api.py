import requests
import pprint
from bs4 import BeautifulSoup


def search_books(query, limit=None):
    # URL с запросом
    url = f"https://flibusta.site/booksearch?ask={query}&chb=on"

    # Выполняем запрос
    response = requests.get(url)

    # Парсим HTML с BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Извлекаем только книги, игнорируя другие элементы
    books = []
    for li in soup.find_all('li'):
        a_tag = li.find('a')
        if a_tag and '/b/' in a_tag['href']:  # Проверяем, что это ссылка на книгу
            book_title = a_tag.text
            book_url = "https://flibusta.site" + a_tag['href']  # Формируем полную ссылку на книгу
            author = li.find_all('a')[-1].text
            books.append({
                "title": book_title,
                "author": author,
                "book_url": f'{book_url}',
                "download_url_fb2": f'{book_url}/fb2',
                "download_url_epub": f'{book_url}/epub',
                "download_url_mobi": f'{book_url}/mobi'
            })
            if limit and len(books) >= limit:
                break

    return books

if __name__ == '__main__':
    response = requests.get('http://flibusta.site/b/133900/fb2')
    print(response.status_code)
    # result = search_books("Хоббит")
    # pprint.pprint(result, sort_dicts=False)
