from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import time
import csv

with open('new_table.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(
        ['name', 'URL']
    )


header = {'User-Agent': UserAgent().random}

link = 'https://poli-vsp.ru/'

responce = requests.get(link, headers=header).text
block = BeautifulSoup(responce, 'lxml')

max_page = str(block.find('nav', class_='navigation pagination').find_all('a', class_='page-numbers')[-2].get('href')).split('/')[-2]

for i in range(1, int(max_page)+1):
    link = f'https://poli-vsp.ru/page/{i}/'

    responce = requests.get(link, headers=header).text
    block = BeautifulSoup(responce, 'lxml')

    all_info = block.find('div', class_='post-cards').find_all('div', class_='post-card__title')

    for i in all_info:
        with open('new_table.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(
                [str(i.find('a').text), str(i.find('a').get('href'))]
            )
            print(f"{i.find('a').text}: {i.find('a').get('href')}")

    time.sleep(1)
