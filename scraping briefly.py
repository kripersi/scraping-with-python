import requests
from bs4 import BeautifulSoup

header = {'user-agent': 'random_people'}

# link for checks / ссылки для проверок

# link = 'https://briefly.ru/fonvizin/nedorosl/'
# link = 'https://briefly.ru/gorkii/na_dne/'
# link = 'https://briefly.ru/mandzoni/obruchennye/'
# link = 'https://briefly.ru/popular/'


def story_and_name(link):
    '''Функция для нахождения: Персонажей, краткого содержания, сюжета, года, автора'''
    responce = requests.get(link, headers=header).text
    block = BeautifulSoup(responce, 'lxml')

    # Конечная строка с кратким содержанием
    end_briefly_str = ''
    all_person = '\t\t\t\t\tCharacter/Персонажи\t\t\n'

    # блок со всем содержанием
    brief = block.find('div', id='text')

    # дата написания текста
    date = block.find('div', class_='titulus').find('span', class_='date').text
    # элемент до которого будет идти краткое содержание
    element = block.find(id='h2-2')

    # персонажи и автор
    characters = brief.find_all('div', class_='character')
    author = block.find('div', class_='breadcrumb__name').text
    # строка в которой будет вся информация
    all_s = 'Дата: ' + date + '\n\nАвтор: ' + author + '\n\n'

    try:
        '''пытаемся найти сюжет и добавить его в главную строку'''
        plot = block.find("article", class_='summary_box').find('p', class_="microsummary__content").text
        all_s += 'Сюжет:' + plot + '\n\n'
    except:
        None

    for character in characters:
        # находим всех персонажей и их характеристику - у характеристики убираем лишние тире
        char_name = character.find('dt', class_="character__name").text
        char_des = character.find('dd', class_="character__description").text.replace('­', '')
        # добавляем персонажа в строку где все персонажи
        all_person += f'{char_name}{char_des}\n'

    all_s += all_person + '\n\n'


    for i in brief:
        # пробегаемся по содержанию и если видим что оно закончилось то прерываем цикл
        if '<h2 id="h2-2">' in str(i):
            break
        # добавляем в строку с кратким содержанием все теги p
        elif str(i)[:2] == '<p':
            end_briefly_str += str(i.text.strip()) + '\n'

    # добавляем краткое содержание в конечную строку
    all_s += 'Краткое содержание: ' + end_briefly_str
    quest = str(input('Что бы вы хотели узнать? Дату[1], Краткое содержание[2], Сюжет[3], Персонажи[4], Автор[5], Всё[6]: '))

    choice = {'1': f'DATE/ДАТА: {date}\n',
            '2': end_briefly_str,
            '3': plot,
            '4': all_person,
            '5': author,
            '6': all_s}

    print(choice[quest])


def popular_story():
    '''популярные рассказы'''
    link = 'https://briefly.ru/popular/'

    responce = requests.get(link, headers=header).text
    block = BeautifulSoup(responce, 'lxml')

    # получаем блок где находиться все популярные рассказы
    popular_cards_story = block.find('ul', class_="work-cards-grid")
    story_card = popular_cards_story.find_all('li', class_="work-cards-grid__item")

    # информация о расказах
    about_card_story = ''
    # какое место занимает рассказ в топе лучших
    c = 1

    for i in story_card:
        # пробегаемся по всем популярным рассказам и находим: название рассказа, ссылку, автора, сюжет
        name_story = i.find('a').text.replace('­', '')
        url_story = str(i.find('a').get('href'))
        author_story = i.find('small', class_="work__meta").text.split('·')
        mini_plot = i.find('p', class_="work__microsummary").text.replace('­', '')
        # добавляем все в карточку и прибавляем в счетчик +1
        about_card_story += f'{str(c)}. {name_story}\nAuthor / автор: {author_story[0]}\nGenre / жанр: {author_story[1]}\nPlot / сюжет: {mini_plot}\nURL:  https://briefly.ru{url_story}\n{"-"*15}\n'
        c += 1

    print(about_card_story)

# спрашиваем что пользователь хочет узнать популярные рассказы или краткое содержание какого либо рассказа
a = str(input('ENTER 1 OR 2\nPopular story - 1\nbrief story - 2\n'))

if a == '1':
    popular_story()
elif a == '2':
    url = input('enter a link to the text | введите ссылку на краткое содержание: ')
    try:
        story_and_name(url)
    except:
        print('NOT FOUND')

