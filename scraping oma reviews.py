import requests
from bs4 import BeautifulSoup

header = {'user-agent': 'random_people'}

link = 'https://www.oma.by/reviews/'

responce = requests.get(link, headers=header).text
block = BeautifulSoup(responce, 'lxml')

reviews = block.find_all('div', class_="reviews-block_item review")

count_review = 0
for review in reviews:
    count_review += 1

    reviews_about = review.find('div', class_='review_content-param')
    reviews_grade_like = review.find('div', class_='review_likes likes').find('span', class_='likes_btn likes_btn__like active')
    reviews_grade_dislike = review.find('div', class_='review_likes likes').find('span', class_='likes_btn likes_btn__dislike active')

    review_date = review.find('div', class_="review_info-param")

    print(f'{reviews_about.text.strip()}\nLIKES: {reviews_grade_like.text.strip()}\tDISLIKES: {reviews_grade_dislike.text.strip()}\nDATE: {review_date.text.strip()}\n------------\n')

print('end')
