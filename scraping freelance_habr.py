from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests

page = 1
flag = True

about_task = []
count_len_task = []

while flag:
    try:
        link = f'https://freelance.habr.com/tasks?page={page}&q=python'

        header = {'User-Agent': UserAgent().random}

        responce = requests.get(link, headers=header).text
        block = BeautifulSoup(responce, 'lxml')

        all_tasks = block.find('ul', class_='content-list content-list_tasks')

        tasks_without_marked = all_tasks.find_all('li', class_='content-list__item')

        for task in tasks_without_marked:
            name = f"Description: {task.find('div', class_='task__title').find('a').text}\n"
            url_task = f"\nURL: {task.find('div', class_='task__title').find('a').get('href')}\n\n"
            information = task.find('div', class_='task__params params')

            responses = f"Responses: {information.find('i', class_='params__count').text}\n"
            views = f"Views: {information.find('span', class_='params__views icon_task_views').find('i').text}\n"
            date = f"Date: {information.find('span', class_='params__published-at icon_task_publish_at').find('span').text}\n"

            try:
                price = f"Price: {task.find('aside', class_='task__column_price').find('span', class_='count').text.strip()}\n"
            except:
                price = 'Price: NONE\n'

            tags = task.find("div", class_="task__tags").find("ul", class_="tags tags_short").find_all("a")
            list_of_tags = []

            for tag in tags:
                list_of_tags.append(tag.text.strip())

            about_task.append(name + price + responses + views + date + 'Tags: ' + str(list_of_tags) + url_task)

        count_len_task.append(len(about_task))
        page += 1

        if len(count_len_task) > 1 and count_len_task[-1] == count_len_task[-2]:
            flag = False
            break
    except:
        print('PROGRAMM END')
        flag = False
        break


for whole_task in about_task:
    print(whole_task)
