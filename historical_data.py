import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime


def generate_historical_data_table():
    df = pd.read_csv("HistoricalData.csv", ";")
    data = df.to_numpy()
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(
        '''CREATE TABLE historical_price (year YEAR, month MONTH, average_price_0_to_38 INTEGER, average_price_38_to_60 
        INTEGER, average_price_60_to_90 INTEGER, PRIMARY KEY(year, month) ) ''')
    for row in data:
        cursor.execute('INSERT INTO historical_price VALUES (?, ?, ?, ?, ?)', (int(row[0]), int(row[1]), int(row[2]), int(row[3]), int(row[4])))
        connection.commit()
    connection.close()


def add_row_to_historical_data(month, year):
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute('SELECT price, area FROM apartment_rent_price WHERE year=? AND month=?', (year, month))

    price_sum = [0, 0, 0]
    count_apartment = [0, 0, 0]
    for row in cursor.fetchall():
        price = row[0]
        area = float(str(row[1]).replace(",", "."))

        if area <= 38:
            price_sum[0] += price
            count_apartment[0] += 1
        elif 38 < area <= 60:
            price_sum[1] += price
            count_apartment[1] += 1
        elif 60 < area <= 90:
            price_sum[2] += price
            count_apartment[2] += 1

    mean_price = []
    for i in range(3):
        mean_price.append(round(price_sum[i]/count_apartment[i], 3))

    date = str(datetime.date(datetime.now()))
    date = date.split("-")
    cursor.execute('INSERT INTO historical_price VALUES (?, ?, ?, ?, ?)',
                   (date[0], date[1], mean_price[0], mean_price[1], mean_price[2]))
    connection.commit()
    connection.close()


if __name__ == "__main__":
    #generate_historical_data_table()
    add_row_to_historical_data(4, 2021)
