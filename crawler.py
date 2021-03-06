from bs4 import BeautifulSoup
from requests import get
import sqlite3
from datetime import datetime


def parse_price(price):
    return float(price.replace(' ', '').replace('zł/miesiąc', ''))


def parse_info(info):
    return info.replace('pokoje', '').replace('pokój', '').replace('m2', '')


def parse_floor(floor):
    return floor.replace('Cena za m2', '').replace('Piętro', '').replace('zł', '').replace('Dostępne', '').replace(
        'Dodatkowa', '')


def make_rent_price_table():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE apartment_rent_price (location TEXT, price REAL, rooms INTEGER, area INTEGER, 
    floor INTEGER, year YEAR, month MONTH, day DAY) ''')
    connection.commit()
    connection.close()


def insert_new_data_to_rent_price_table():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    date = str(datetime.date(datetime.now()))
    date = date.split("-")
    for i in range(1, 120):
        URL = 'https://gethome.pl/mieszkania/do-wynajecia/krakow/?page={}'.format(i)

        # pobieranie zawartości strony
        page = get(URL)

        # przekazanie zawartości strony do konstruktora bs
        bs = BeautifulSoup(page.content, 'html.parser')

        # przejście po wszystkich ofertach
        for offer in bs.find_all('div', class_='css-1our9ed-offerBoxWrapper'):
            try:
                location = offer.find('p', class_='css-unl6d4-PropertyLocation-ellipsis e1es8y4n4').get_text().strip().split(',')[1]
                price = parse_price(offer.find('p', class_='css-pce4ym-Price eeuzmg10').get_text().strip())
                rooms = parse_info(offer.find('div', class_='css-jg9o52-Flex e8aa8cc0').get_text().strip()).split(' ')[0]
                area = parse_info(offer.find('div', class_='css-jg9o52-Flex e8aa8cc0').get_text().strip()).split(' ')[1]
                area = ''.join(i for i in area if i.isdigit() or i==',')

                link = offer.find('a')
                page2 = get('https://gethome.pl' + link['href'])
                bs2 = BeautifulSoup(page2.content, 'html.parser')
                floor = parse_floor(bs2.find('div', class_='css-1id7vsr-FeaturesList e1kihjfm0').get_text()).split(' ')[1]

                cursor.execute('INSERT INTO apartment_rent_price VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                               (location, price, rooms, area, floor, date[0], date[1], date[2]))
                connection.commit()
            except IndexError:
                pass
    connection.close()


if __name__ == "__main__":
    #make_rent_price_table
    insert_new_data_to_rent_price_table()

