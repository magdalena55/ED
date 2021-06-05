import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


def plot_avg_price_fo_each_loc():
    date = str(datetime.date(datetime.now()))
    date = date.split("-")
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(
        'SELECT  AVG(price/area), location FROM apartment_rent_price WHERE year=? AND month=? GROUP BY location ORDER '
        'BY AVG(price/area) DESC',
        (date[0], date[1]))
    possible_locations = [' Stare Miasto', ' Krowodrza', ' Grzegórzki', ' Dębniki', ' Podgórze', ' Prądnik Biały',
                          ' Prądnik Czerwony', ' Bronowice', ' Zwierzyniec', ' Czyżyny', ' Podgórze Duchackie',
                          ' Łagiewniki-Borek Fałęcki', ' Bieżanów-Prokocim', ' Nowa Huta', ' Mistrzejowice',
                          ' Bieńczyce', ' Swoszowice']
    locations, avg_price = [], []
    for row in cursor.fetchall():
        if row[1] in possible_locations:
            avg_price.append(row[0])
            locations.append(row[1])

    y_pos = np.arange(len(locations))
    performance = avg_price
    error = np.random.rand(len(locations))
    fig, ax = plt.subplots()
    hbars = ax.barh(y_pos, performance, xerr=error, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(locations)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Avg price for m^2')
    #ax.set_title('Avg price for m^2 for each location')
    # Label with specially formatted floats
    ax.bar_label(hbars, fmt='%.2f')
    ax.set_xlim(right=max(avg_price) + 2)  # adjust xlim to fit labels
    plt.tight_layout()
    plt.savefig('static/images/plot_avg_price.png')


## 2

def plot_number_of_offers():
    date = str(datetime.date(datetime.now()))
    date = date.split("-")
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(
        'SELECT  COUNT(*), location FROM apartment_rent_price WHERE year=? AND month=? GROUP BY location ORDER BY COUNT(*) DESC',
        (date[0], date[1]))
    possible_locations = [' Stare Miasto', ' Krowodrza', ' Grzegórzki', ' Dębniki', ' Podgórze', ' Prądnik Biały',
                          ' Prądnik Czerwony', ' Bronowice', ' Zwierzyniec', ' Czyżyny', ' Podgórze Duchackie',
                          ' Łagiewniki-Borek Fałęcki', ' Bieżanów-Prokocim', ' Nowa Huta', ' Mistrzejowice',
                          ' Bieńczyce', ' Swoszowice']
    locations = []
    count_locations = []
    for row in cursor.fetchall():
        if row[1] in possible_locations:
            count_locations.append(row[0])
            locations.append(row[1])

    y_pos = np.arange(len(locations))
    performance = count_locations
    error = np.random.rand(len(locations))
    fig, ax = plt.subplots()
    hbars = ax.barh(y_pos, performance, xerr=error, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(locations)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Number of offers')
    #ax.set_title('Number of offers for each location')

    ax.bar_label(hbars)
    ax.set_xlim(right=max(count_locations) + 2)  # adjust xlim to fit labels
    plt.tight_layout()
    plt.savefig('static/images/plot_number_of_offers.png', dpi=300)

#
# plot_number_of_offers()
# plot_avg_price_fo_each_loc()


def historical_plot():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(
        'SELECT  * FROM historical_price ORDER BY year, month')
    possible_locations = [' Stare Miasto', ' Krowodrza', ' Grzegórzki', ' Dębniki', ' Podgórze', ' Prądnik Biały',
                          ' Prądnik Czerwony', ' Bronowice', ' Zwierzyniec', ' Czyżyny', ' Podgórze Duchackie',
                          ' Łagiewniki-Borek Fałęcki', ' Bieżanów-Prokocim', ' Nowa Huta', ' Mistrzejowice',
                          ' Bieńczyce', ' Swoszowice']
    date = []
    values1, values2, values3 = [], [], []
    for row in cursor.fetchall():
        date.append(str(row[0]) + "/" + str(row[1]))
        values1.append(row[2]), values2.append(row[3]), values3.append(row[4])
    fig, ax = plt.subplots()
    ax.plot(date, values1)
    ax.plot(date, values2)
    ax.plot(date, values3)
    plt.xticks(np.arange(0, len(date) + 1, 7))
    plt.tight_layout()
    plt.savefig('static/images/plot_historical.png', bbox_inches='tight')


def get_data():
    date = str(datetime.date(datetime.now()))
    date = date.split("-")
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(
        'SELECT  price, area FROM apartment_rent_price WHERE year=? AND month=?',
        (date[0], date[1]))
    possible_locations = [' Stare Miasto', ' Krowodrza', ' Grzegórzki', ' Dębniki', ' Podgórze', ' Prądnik Biały',
                          ' Prądnik Czerwony', ' Bronowice', ' Zwierzyniec', ' Czyżyny', ' Podgórze Duchackie',
                          ' Łagiewniki-Borek Fałęcki', ' Bieżanów-Prokocim', ' Nowa Huta', ' Mistrzejowice',
                          ' Bieńczyce', ' Swoszowice']

    price, area = [], []
    for row in cursor.fetchall():
        price.append(row[0])
        area.append(float(str(row[1]).replace(",",".")))
    price = np.asarray(price)
    area = np.asarray(area)
    ratio = price/area

    # zwraca liczbe ofert, srednia cene
    return area.shape[0], np.mean(ratio) , round(np.median(ratio),2), round(np.quantile(ratio, 0.25),2), round(np.quantile(ratio, 0.75),2)


def plot_current_price(location):
    location = " " + location
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(
        'SELECT AVG(price/area), year, month FROM apartment_rent_price WHERE location=? GROUP BY year, month ',
        (location,))

    price, date = [], []
    for row in cursor.fetchall():
        price.append(row[0])
        date.append(str(row[1]) + '/' +str(row[2]))

    fig, ax = plt.subplots()
    ax.plot(date, price)
    plt.title("Średnia cena za m^2 na przestrzeni czasu")
    ax.set_xlabel("Data")
    ax.set_ylabel("Średnia Cena za m^2 (PLN) ")
    plt.tight_layout()
    location = location.replace(' ', '_')
    plt.savefig('static/images/loc_price_{}.png'.format(location))


def make_all_plot_price():
    possible_locations = ['Stare Miasto', 'Krowodrza', 'Grzegórzki', 'Dębniki', 'Podgórze', 'Prądnik Biały',
                          'Prądnik Czerwony', 'Bronowice', 'Zwierzyniec', 'Czyżyny', 'Podgórze Duchackie',
                          'Łagiewniki-Borek Fałęcki', 'Bieżanów-Prokocim', 'Nowa Huta', 'Mistrzejowice',
                          'Bieńczyce', 'Swoszowice']
    for loc in possible_locations:
        plot_current_price(loc)
        plt.clf()


def plot_room_info_all():
    date = str(datetime.date(datetime.now()))
    date = date.split("-")
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute('SELECT  rooms FROM apartment_rent_price WHERE year=? AND month=? ', (date[0], date[1]))
    rooms = []
    for row in cursor.fetchall():
        if type(row[0]) == str:
            rooms.append(int(row[0][-1]))
        else:
            rooms.append(row[0])
    frequency = {}
    options = [1, 2, 3, 4, 5, "6+"]
    for i in options:
        frequency[i] = 0
    for item in rooms:
        if item < 6:
            frequency[item] += 1
        else:
            frequency["6+"] += 1
    y_pos = np.arange(len(frequency.keys()))
    performance = frequency.values()
    error = np.random.rand(len(frequency.values()))
    fig, ax = plt.subplots()
    hbars = ax.barh(y_pos, performance, xerr=error, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(frequency.keys())
    ax.invert_yaxis()
    ax.set_xlabel('Liczba danych mieszkań')
    ax.bar_label(hbars, fmt='%.2f')
    ax.set_xlim(right=max(frequency.values()) + 2)
    plt.ylabel("Liczba pokojów")
    plt.tight_layout()
    plt.savefig('static/images/rooms_info.png')

plot_room_info_all()
make_all_plot_price()
plot_avg_price_fo_each_loc()
plot_number_of_offers()
historical_plot()