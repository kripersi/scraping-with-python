import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

header = {'User-Agent': UserAgent().random}

link_empty = 'http://himsnab-spb.ru/article/ps/'

try:
    message = str(input('Если вы хотите узнать информацию то напишите люой хим элемент например Cl, H, Au:  '))
    link = link_empty + message.lower()

    responce = requests.get(link, headers=header).text
    block = BeautifulSoup(responce, 'lxml')

    all_info = block.find('tbody').find_all('tr')

    name_element = f'\nНазвание: {all_info[0].text.strip()} ({message.strip()})\n\n'
    atom_num_element = f'Атомный номер: {all_info[1].find_all("td")[-1].text.strip()}\n'
    massa_element = f'Атомная масса: {all_info[4].find_all("td")[-1].text.strip()}\n'
    electons_element = f'Электронная конфигурация: {all_info[7].find_all("td")[-1].text.strip()}\n'
    oxidation_element = f'Степени окисления: {all_info[13].find_all("td")[-1].text.strip()}\n'
    appearance_element_no_f = all_info[2].find_all("td")[-1].text.strip().replace("\t", " ")
    appearance_element = f'Внешний вид вещества: {appearance_element_no_f}'

    if appearance_element[-1] in [' ', '', '\t']:
        appearance_element = 'Внешний вид вещества: не найден'

    print(name_element + atom_num_element + massa_element + electons_element + oxidation_element + appearance_element)
except:
    print('Элемент не найден. Вы ввели неверный запрос!\nПример ввода: Cl, Au, Br, Ba')
