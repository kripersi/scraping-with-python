from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import re

# чтобы сайт не заметил парсера
header = {'User-Agent': UserAgent().random}
page = 1
link = f'https://pravda-sotrudnikov.ru/catalog/uslugi-naseleniju/it-kompanii-razrabotka-hosting?page=2'

responce = requests.get(link, headers=header).text

block = BeautifulSoup(responce, 'lxml')
all_company = block.find('div', class_="col-xs-12 mdc-reviews").find_all('div', class_="col-md-4 mdc-reviews-item")[1:]

while True:
    try:
        link = f'https://pravda-sotrudnikov.ru/catalog/uslugi-naseleniju/it-kompanii-razrabotka-hosting?page={page}'

        responce = requests.get(link, headers=header).text
        block = BeautifulSoup(responce, 'lxml')

        all_company = block.find('div', class_="col-xs-12 mdc-reviews").find_all('div', class_="col-md-4 mdc-reviews-item")[1:]

        for i in all_company:
            try:
                name_site = i.find('div', class_='mdc-companies-item-title').find('a').text # name
                site_grade = i.find('span', class_="mdc-companies-item-rating-stars rating-autostars").get('data-rating') # grade
                info_site = i.find('div', class_='mdc-companies-item-text') #  block info

                site_company = info_site.find_all('div')[-1].find('a').text.strip()
                email_site_block = info_site.find_all('div')

                for emails in email_site_block:
                    if '@' in str(emails.find('a')):
                        email_site = re.findall(r'<a\b[^>]*>(.*?)</a>', str(emails.find('a')))[0]
                        break

                site_telephone = ''
                all_site_info = ''

                for info in info_site:
                    telephone = re.findall(r'\+?\d+ \(\d+\) \d+-\d+\d+-\d+', str(info))
                    if len(telephone) != 0:
                        site_telephone = telephone

                if email_site.strip().replace('//', '') == site_company.strip() and '@' not in email_site.strip():
                    all_site_info += f'Name: {name_site}\n' \
                                     f'Site grade: {site_grade}\n' \
                                     f'Number telephone: {" | ".join(site_telephone)}\n' \
                                     f'Site: {site_company}\n' \
                                     f'{"-" * 15}\n'.replace(' ', '').replace('\n', '').replace('\t', '')
                else:

                    all_site_info_beta = f'Name: {name_site}\n' \
                                     f'Site grade: {site_grade}\n' \
                                     f'Number telephone: {" | ".join(site_telephone)}\n' \
                                     f'Site: {site_company}\n' \
                                     f'Email: {email_site}\n' \
                                     f'{"-" * 15}\n'
                    if str(all_site_info_beta[all_site_info_beta.index('telephone') + 11]) not in ['8', '+', '0', '7', '3']:
                        all_site_info += f'Name: {name_site}\n' \
                                              f'Site grade: {site_grade}\n' \
                                              f'Site: {site_company}\n' \
                                              f'Email: {email_site}\n' \
                                              f'{"-" * 15}\n'
                    else:
                        all_site_info = all_site_info_beta


                print(all_site_info)
            except:
                continue
        page += 1
    except:
        print('error')
        page += 1
        continue
