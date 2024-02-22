from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup


header1 = {'User-Agent': UserAgent().random}  # user agent для того чтобы узнать сколько страниц


def scraping(link, page):
    header = {'User-Agent': UserAgent().random}

    responce = requests.get(f'{link}{page}', headers=header).text
    soup = BeautifulSoup(responce, 'lxml')

    products = soup.find('section', class_='b-catalog__section i-catalog').find_all('div', class_='row')  # все продукты

    for i in products[:20]:
        name = i.find('div', class_='col-xs-5').find('a').text
        reference = i.find('div', class_='b-list__info').find_all('span', class_='text-black')[0].text
        try:  # если есть артикл то записываем, в ином случае пишем '!NOT!'
            article = i.find('div', class_='b-list__info').find_all('span', class_='text-black')[1].text
        except:
            article = '!NOT!'

        try:  # если есть цена то записываем, в ином случае пишем '!NOT!'
            price = i.find('div', class_='col-xs-2 no-gutter').find('span').text
        except:
            price = 'Цена по запросу'

        print(f'{name}  |  {price}  |  {reference}  |  {article}')


def all_page():
    '''функция для нахождения всех страниц'''
    link = 'https://www.texenergo.ru/catalog/list.html/90000005?set_filter=y&PAGEN_7='  # main link

    responce = requests.get(f'{link}1', headers=header1).text
    soup = BeautifulSoup(responce, 'lxml')

    last_page = int(soup.find('div', class_='b-pagination i-pagination').find_all('a')[-1].text.strip())

    for pg in range(1, last_page+1):
        print(f'парсится страница: {pg}')
        scraping(link, pg)


all_page()

