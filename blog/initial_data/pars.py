import requests
from bs4 import BeautifulSoup
import time
from random import randrange
import json

from blog.blog.settings import BASE_DIR

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36 OPR/85.0.4341.60'
}

# получение ссылок на посты
def get_articles_urls(url):
    s = requests.Session()
    response = s.get(url=url, headers=headers)

    soup = BeautifulSoup(response.text, 'lxml')
    pagination_count = int(soup.find('ul', class_='tn-pagination').find_all('li')[-2].text)

    article_urls_list = []
    # указывается количество страниц (пагинации) для получения ссылок на посты
    for page in range(2, 30):
        response = s.get(url=f'https://tengrinews.kz/tech/page/{page}/', headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        article_urls = soup.find_all('a', class_='tn-link')

        for au in article_urls:
            art_url = au.get('href')
            article_urls_list.append(f'https://tengrinews.kz{art_url}')

        # остановка работы программы с рандомным временем, чтобы не получить бан
        time.sleep(randrange(1, 3))
        print(f'Обработал {page}/{pagination_count}')

    # запись ссылок в файл
    with open('article_urls.txt', 'w') as file:
        for url in article_urls_list:
            file.write(f'{url}\n')

    return 'Работа по сбору ссылок выполнена!'

# получение информации из постов по ссылкам, собранным ранее
def get_data(file_path):
    global article_category
    with open(file_path, encoding='utf-8') as file:
        urls_list = [line.strip() for line in file.readlines()]

    urls_count = len(urls_list)

    s = requests.Session()
    result_data = []
    r = 0

    for url in enumerate(urls_list):
        response = s.get(url=url[1], headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        article_title = soup.find('div', class_='tn-content').find('h1', class_='tn-content-title').text.strip()
        date = soup.find('div', class_='tn-side-bar').find('time', class_='tn-visible@t').text.strip()
        date1 = date.split()
        m = {'января': '01',
             'февраля': '02',
             'марта': '03',
             'апреля': '04',
             'мая': '05',
             'июня': '06',
             'июля': '07',
             'августа': '08',
             'сентября': '09',
             'октября': '10',
             'ноября': '11',
             'декабря': '12'}
        article_date = f'{date1[2][:4]}-{m.get(date1[1])}-{date1[0]} {date1[3]}Z'
        try:
            exile_img = f"https://tengrinews.k" \
                    f"z{soup.find('div', class_='tn-news-content').find('picture').find('img').get('src')}"
        except AttributeError:
            exile_img = "https://klike.net/uploads/posts/2018-07/1531820435_2.jpg"
        image_bytes = requests.get(exile_img).content
        s1 = exile_img.split('/')

        with open(BASE_DIR / f'media/main/{s1[-1]}', 'wb') as file:
            file.write(image_bytes)
        article_img = 'main/' + s1[-1]
        article_text = soup.find('div', class_='tn-news-content').find('article',
                                                                       class_='tn-news-text').text.strip().replace('\n',
                                                                                                                   '')

        ac = {
            1: 'Интернет',
            2: 'Медицина',
            3: 'Наука',
            4: 'Технологии',
            5: 'Прогресс',
            6: 'Автомобили',
            7: 'Гаджеты',
        }
        for keys in ac:
            if ac[keys] == soup.find('ol').find_all('li')[-1].find('a').text.strip():
                article_category = keys

        result_data.append(
            {
                'model': "main.Post",
                'pk': r,
                'fields':
                    {
                        'title': article_title.split('\n')[0],
                        'slug': r,
                        'text': article_text,
                        'category': article_category,
                        'image': article_img,
                        'publish_date': article_date,
                    }

            }
        )

        time.sleep(randrange(2, 4))
        r += 1
        print(f'Обработал {url[0] + 1}/{urls_count}')

    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(result_data, file, indent=4, ensure_ascii=False)


def main():
    get_articles_urls(url='http://tengrinews.kz/tech')
    get_data(file_path='D:/Django/blog/initial_data/article_urls.txt')



if __name__ == '__main__':
    main()
