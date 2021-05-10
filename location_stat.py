import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def get_number(location):
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
    plt.title("Wykres pudełkowy ceny wynajmu")
    plt.savefig('static/images/loc.png')



#print(price_boxplot("Bronowice"))