import sqlite3
from datetime import datetime
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def rent_price_model():
    date = str(datetime.date(datetime.now()))
    date = date.split("-")
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute(
        'SELECT  price, location, rooms, area FROM apartment_rent_price WHERE year=? AND month=?',
        (date[0], date[1]))

    possible_locations = [' Stare Miasto', ' Krowodrza', ' Grzegórzki', ' Dębniki', ' Podgórze', ' Prądnik Biały',
                          ' Prądnik Czerwony', ' Bronowice', ' Zwierzyniec', ' Czyżyny', ' Podgórze Duchackie',
                          ' Łagiewniki-Borek Fałęcki', ' Bieżanów-Prokocim', ' Nowa Huta', ' Mistrzejowice',
                          ' Bieńczyce', ' Swoszowice']
    data = []
    for row in cursor.fetchall():
        if row[1] in possible_locations:
            row = list(row)
            row[3] = float(str(row[3]).replace(",", "."))
            if type(row[2]) == str:
                row[2] = 2
            data.append(row)

    df = pd.DataFrame(data, columns=['price', 'location', 'rooms', 'area'])
    df = pd.get_dummies(df, columns=['location'])
    data = np.array(df)
    x = data[:, 1:]
    y = data[:, 0]
    model = LinearRegression().fit(x, y)
    df_loc_order = df.columns[3:]

    return model, possible_locations, df_loc_order


def hot_one_encoding(location, locations):
    result = []
    for loc in locations:
        if loc == location:
            result.append(1)
        else:
            result.append(0)
    return result
