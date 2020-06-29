import sqlite3
from datetime import date, datetime
from MailHandler import MailHandler

import requests

def create_conn():
    conn = None
    try :
        conn = sqlite3.connect('db.sqlite3')
    except sqlite3.Error as e:
        print(e)
    return conn

def update_values(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM app_item")
    rows = cur.fetchall()
    list_of_games = []
    list_of_discounts = []
    for row in rows:
        list_of_games.append(row)
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
        cur = conn.cursor()
        sql_last_update = '''SELECT * from app_item WHERE item_id = ?'''
        cur.execute(sql_last_update,(val[0],))
        last_update = cur.fetchall()
        for last in last_update:
            if last[2] > val[2]:
                list_of_discounts.append(val[0])
        sql_update = '''UPDATE app_item SET price = ? where item_id = ? '''
        cur = conn.cursor()
        cur.execute(sql_update, (price, val[0]))
    conn.commit()
    print(cur.fetchall())
    cur.close()
    return list_of_discounts

def sendDiscountEmails(conn, list_of_discounts):
    mh = MailHandler(587, 'smtp.gmail.com', 'noreply.PSN.Checker@gmail.com', 'Psn12345')
    cur = conn.cursor()
    cur.execute("SELECT * FROM app_basket")
    for row in cur.fetchall():
        game_names = []
        game_prices = []
        game_url = []
        cur = conn.cursor()
        cur.execute("SELECT * FROM app_basketitem where basket_id = ?",(row[0],))
        for item in cur.fetchall():
            if item[2] in list_of_discounts:
                cur = conn.cursor()
                cur.execute("SELECT * FROM app_item WHERE id = ?",(item[2],))
                item_details = cur.fetchall()
                game_names.append(item_details[1])
                game_prices.append(item_details[2])
                game_url.append(item_details[5])
        cur = con.cursor()
        cur.execute('SELECT * from auth_user WHERE id = ?', (row[3],))
        user = cur.fetchall()
        if len(game_names) > 0:
            mh.sendDiscount(user[4], user[6], game_names, game_prices, game_url)



con = create_conn()
list_of_discounts = update_values(con)
sendDiscountEmails(con, list_of_discounts)