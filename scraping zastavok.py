import requests
from bs4 import BeautifulSoup

image_number = 0  # для названия изображения
storage_num = 1
link = f'https://zastavok.net'

for storage_num in range(2450):
    responce = requests.get(f'{link}/{storage_num}/').text
    soup = BeautifulSoup(responce, 'lxml')
    block = soup.find('div', class_="block-photo")
    all_image = block.find_all('div', class_='short_full')

    for image in all_image:
        image = image.find('a').get('href')
        
        donwnload_storage = requests.get(f'{link}{image}').text
        download_soup = BeautifulSoup(donwnload_storage, 'lxml')
        download_block = download_soup.find('div', class_='image_data').find('div', class_='block_down')
        result_link = download_block.find('a').get('href')

        image_bytes = requests.get(f'{link}{result_link}').content

        with open(fr'C:\Users\Какаша\PycharmProjects\pythonProject4\venv\imagee\{image_number}.jpg', 'wb') as file:
            file.write(image_bytes)

        image_number += 1
        print(f'pictures {image_number}.jpg download')
    storage_num += 1



