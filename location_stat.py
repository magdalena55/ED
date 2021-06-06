import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def get_number_of_offers(location):
    date = str(datetime.date(datetime.now()))
    date = date.split("-")
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    location = " " + location
    cursor.execute(
        'SELECT  COUNT(*) FROM apartment_rent_price WHERE year=? AND month=? AND location=?',
        (date[0], date[1], location))
    number = cursor.fetchall()[0][0]

    return number


def get_avg_price(location):
    date = str(datetime.date(datetime.now()))
    date = date.split("-")
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    location = " " + location
    cursor.execute(
        'SELECT  AVG(price) FROM apartment_rent_price WHERE year=? AND month=? AND location=?',
        (date[0], date[1], location))
    avg_price = cursor.fetchone()[0]

    return round(avg_price, 2)


def get_location_stats(location):
    date = str(datetime.date(datetime.now()))
    date = date.split("-")
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    location = " " + location
    cursor.execute(
        'SELECT  price, area FROM apartment_rent_price WHERE year=? AND month=? AND location=?',
        (date[0], date[1], location))
    price, area = [], []
    for row in cursor.fetchall():
        price.append(row[0])
        area.append(float(str(row[1]).replace(",", ".")))
    price = np.asarray(price)
    area = np.asarray(area)
    ratio = price / area

    return round(np.mean(ratio),2), round(np.median(ratio), 2), round(np.quantile(ratio, 0.25), 2), round(np.quantile(ratio, 0.75))


def get_room_info(location):
    date = str(datetime.date(datetime.now()))
    date = date.split("-")
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    location = " " + location
    cursor.execute('SELECT  rooms FROM apartment_rent_price WHERE year=? AND month=? AND location=?',
        (date[0], date[1], location))

    rooms = []
    for row in cursor.fetchall():
        if type(row[0]) == str:
            rooms.append(int(row[0][-1]))
        else:
            rooms.append(row[0])
    frequency = {}
    #options = [1, 2, 3, 4, "5+"]
    options = ["5+", 4, 3, 2, 1]
    for i in options:
        frequency[i] = 0
    for item in rooms:
        if item < 5:
            frequency[item] += 1
        else:
            frequency["5+"] += 1
    return frequency


def plot_room_info(location):
    date = str(datetime.date(datetime.now()))
    date = date.split("-")
    frequency = get_room_info(location)
    y_pos = np.arange(len(frequency.keys()))
    performance = frequency.values()
    error = np.random.rand(len(frequency.values()))
    fig, ax = plt.subplots()
    hbars = ax.barh(y_pos, performance, xerr=error, align='center', color='orange')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(frequency.keys())
    ax.invert_yaxis()
    ax.set_xlabel('Liczba ofert')
    ax.bar_label(hbars, fmt='%.0f')
    ax.set_xlim(right=max(frequency.values()) + 30)
    ax.set_title('Liczba ofert wynajmu mieszkania w zależności od \n liczby pokoi w miesiącu {}/{}'.format(date[1],date[0]))
    plt.ylabel("Liczba pokoi")
    plt.tight_layout()
    location = location.replace(' ', '_')
    plt.savefig('static/images/loc_rooms_{}.png'.format(location))


def price_boxplot(location):
    date = str(datetime.date(datetime.now()))
    date = date.split("-")
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    location = " " + location
    cursor.execute(
        'SELECT  price FROM apartment_rent_price WHERE year=? AND month=? AND location=?',
        (date[0], date[1], location))

    prices = []
    for price in cursor.fetchall():
        prices.append(price[0])

    fig, ax = plt.subplots()
    df = pd.DataFrame(prices)
    df.boxplot(ax=ax)
    ax.set_xticks([])
    plt.title('Wykres pudełkowy ceny wynajmu mieszkania dla dzielnicy {}'.format(location))
    plt.ylabel('Cena (PLN)')
    plt.xlabel(location)
    location = location[1:]
    location = location.replace(' ', '_')
    plt.savefig('static/images/loc_{}.png'.format(location))


def make_all_plots():
    possible_locations = ['Stare Miasto', 'Krowodrza', 'Grzegórzki', 'Dębniki', 'Podgórze', 'Prądnik Biały',
                          'Prądnik Czerwony', 'Bronowice', 'Zwierzyniec', 'Czyżyny', 'Podgórze Duchackie',
                          'Łagiewniki-Borek Fałęcki', 'Bieżanów-Prokocim', 'Nowa Huta', 'Mistrzejowice',
                          'Bieńczyce', 'Swoszowice']
    for loc in possible_locations:
        price_boxplot(loc)
        plot_room_info(loc)
        plt.clf()


make_all_plots()