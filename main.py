import requests
from bs4 import BeautifulSoup
import json

URL = 'https://www.rbc.ru/'


def get_soup(url):
    r = requests.get(url).text
    return BeautifulSoup(r, 'lxml')


def save_json(data):
    with open('rbk_data.json', "w") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def main():
    news_data = {}

    soup = get_soup(URL)

    # Получаем все ссылки на новости
    news_links = soup.find('div', class_='main').find_all('a', {'class': ['main__big__link', 'main__feed__link']})

    # Для каждой ссылки получаем информацию и записываем в news_data
    for i in range(15):

        name = 'New_{0}'.format(i + 1)
        news_data[name] = {}
        link = news_links[i].get('href').split('?')[0]
        soup = get_soup(link)

        # Переходим на страницу для дальнейшенго парсинга
        article = soup.find('div', class_='article')
        category = article.find('a', class_='article__header__category')
        date = article.find('span', class_='article__header__date').get('content').replace('T', ' ').split('+')[0]
        title = article.find('span', class_='js-slide-title').text
        overview = article.find('div', class_='article__text__overview').find('span').text.replace('\xa0', '')
        image = article.find('div', class_='article__main-image')
        article_paragraphs = article.find_all('p')
        article_text = ''
        for paragraph in article_paragraphs:
            article_text += paragraph.text

        # Заполняем полученными данными news_data
        news_data[name]['link'] = link
        news_data[name]['date'] = date
        news_data[name]['title'] = title
        news_data[name]['text'] = article_text.replace('\xa0', '').replace('\n', '')
        news_data[name]['overview'] = overview
        try:
            news_data[name]['category'] = category.text
        except AttributeError:
            news_data[name]['category'] = 'Без категории'
        try:
            news_data[name]['image'] = image.find('img').get('src')
        except AttributeError:
            news_data[name]['image'] = 'Без обложки'

    save_json(news_data)


if __name__ == "__main__":
    main()
