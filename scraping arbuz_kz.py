import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

# чтобы сайт не заметил парсера
header = {'User-Agent': UserAgent().random}

for page in range(1, 4):
    '''цикл который перебирает страницы сайта'''
    # ссылки для проверок
    # link = f'https://arbuz.kz/ru/collections/249612-dlya_detei?available=1&limit=48&page={page}#/'
    # link = f'https://arbuz.kz/ru/collections/249613-this_is_halloween#/'
    link = f'https://arbuz.kz/ru/collections/249326-gotovye_obedy?available=1&limit=48&page={page}#/'
    empty_link = 'https://arbuz.kz'

    responce = requests.get(link, headers=header).text
    block = BeautifulSoup(responce, 'lxml')

    # все карточки продуктов
    all_product = block.find('div', class_="product-card-list")
    product_cards = all_product.find_all('article', class_="product-item product-card")

    # счетчик продуктов, на одной странице могут находиться 48 продуктов
    count_product = 0

    for i in product_cards:
        '''цикл в котором проверяется если страница завершена то открываем новую, в случае что страницы закончились останавливаем цикл'''
        if count_product % 48 == 0:
            page += 1
        elif count_product == 144:
            break

        # информация о продукте
        product = f'Name: {i.find("main", class_="product-card__body").find("a", class_="product-card__title").text.strip()}' \
                   f'\nPrice: {i.find("main", class_="product-card__body").find("p", class_="product-card__price").text.strip().split("₸")[0] + "₸"}\n' \
                   f'URL: {empty_link + i.find("main", class_="product-card__body").find("a", class_="product-card__title").get("href")}' \
                   f'\n{"-" * 30}\n'

        count_product += 1  # прибавляем к счетчику один продукт

        #  запись в консоль
        print(product)
        time.sleep(1)

        # запись в файл
        # with open('arbuz_kz_catalog.txt', 'a', encoding='utf-8') as file:
        #     file.write(product)


print('PROGRAMM END')
