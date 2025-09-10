import requests
from bs4 import *
import os
import time
import json
import csv

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36 Edg/140.0.0.0'}
glb_inf_book = []
print('Осталось 50 итераций')
for i in range(1, 51):
    response = requests.get('https://books.toscrape.com/catalogue/category/books_1/page-1.html', headers=headers)
    os.makedirs(f'data/page{i}')
    with open(f'data/page{i}/pagehtml{i}.html', 'w', encoding='utf-8') as file:
        file.write(response.text)
    with open(f'data/page{i}/pagehtml{i}.html', encoding='utf-8') as file:
        src = file.read()
    with open(f'data/page{i}/{i}_table.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Название',
                'Фото',
                'Цена',
                'Наличие',
                'Рейтинг'
            )
        )

    soup = BeautifulSoup(src, 'lxml')
    books_inf = soup.find_all('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
    link_books = []
    for item in books_inf:
        title_link_book = 'https://books.toscrape.com/catalogue' + item.find('h3').find_next().get('href')[5:]
        link_books.append(title_link_book)

    for item in link_books:
        response = requests.get(item, headers=headers)
        with open(f'data/page{i}/book.html', 'w', encoding='utf-8') as file:
            file.write(response.text)
        with open(f'data/page{i}/book.html', encoding='utf-8') as file:
            src = file.read()
        soup = BeautifulSoup(src, 'lxml')
        image_book = 'https://books.toscrape.com/catalogue' + soup.find('div', class_='item active').find_next().get('src')[5:]
        title_book = soup.find('div', class_='col-sm-6 product_main').find('h1').text
        price_book = soup.find('div', class_='col-sm-6 product_main').find('p', class_='price_color').text
        availability_book = soup.find('div', class_='col-sm-6 product_main').find('p', class_='instock availability').text
        rating_book = soup.find('div', class_='col-sm-6 product_main').find('p', class_='instock availability').find_next().find_next()
        if 'One' in str(rating_book):
            rating_book = 'One'
        elif 'Two' in str(rating_book):
            rating_book = 'Two'
        elif 'Three' in str(rating_book):
            rating_book = 'Three'
        elif 'Four' in str(rating_book):
            rating_book = 'Four'
        elif 'Five' in str(rating_book):
            rating_book = 'Five'
        information_book = {
            'Title': title_book,
            'Image': image_book,
            'Price': price_book,
            'Availability': availability_book.strip(),
            'Rating': rating_book
        }
        glb_inf_book.append(information_book)
        with open(f'data/page{i}/{i}_table.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
               (
                    title_book.replace(' ', '_'),
                    image_book.replace(' ', '_'),
                    price_book.replace(' ', '_'),
                    availability_book.strip().replace(' ', '_'),
                    rating_book.replace(' ', '_')
               )
            )
    print(f'Осталось {50-i} итераций')
    print('Загрузка...')
    time.sleep(2)

with open('data/inf_book.JSON', 'a', encoding='utf-8') as file:
    json.dump(glb_inf_book, file, indent=4, ensure_ascii=False)



print('hello')