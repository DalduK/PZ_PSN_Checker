import sqlite3
from datetime import date, datetime

import requests

def create_conn():
    conn = None
    try :
        conn = sqlite3.connect('/home/dldk/PycharmProjects/PZ_PSN_Checker/db.sqlite3')
    except sqlite3.Error as e:
        print(e)
    return conn

def update_values(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM app_item")
    rows = cur.fetchall()
    list_of_games = []
    for row in rows:
        list_of_games.append(row)
    print(list_of_games)
    for val in list_of_games:
        resp = requests.get("https://store.playstation.com/store/api/chihiro/00_09_000/container/PL/pl/999/" + val[4])
        ret = resp.json()
        price = ret["default_sku"]["price"] / 100
        sql_insert = '''INSERT INTO app_itemprice(item_id_id,historical_price,date_fetched) values(?,?,?)'''
        cur = conn.cursor()
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y %H:%M:%S.%f")
        print(dt_string)
        cur.execute(sql_insert,(val[0],val[2],dt_string))
        sql_update = '''UPDATE app_item SET price = ? where item_id = ? '''
        cur = conn.cursor()
        cur.execute(sql_update, (price, val[0]))
    conn.commit()
    print(cur.fetchall())
    cur.close()
    conn.close()

con = create_conn()
update_values(con)