import sqlite3
import pandas as pd
import numpy as np


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


generate_historical_data_table()

