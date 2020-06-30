import sqlite3
from datetime import date, datetime
from MailNotification.MailHandler import MailHandler
from apscheduler.schedulers.blocking import BlockingScheduler
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
    list_of_discounts = []
    for row in rows:
        list_of_games.append(row)
    for val in list_of_games:
        resp = requests.get("https://store.playstation.com/store/api/chihiro/00_09_000/container/PL/pl/999/" + val[3])
        ret = resp.json()
        if len(ret["default_sku"]["rewards"]) == 0:
            price = ret["default_sku"]["price"] / 100
        else:
            price = ret["default_sku"]["rewards"][0]["price"] / 100
        # price = 1000.00
        sql_insert = '''INSERT INTO app_itemprice(item_id_id,historical_price,date_fetched) values(?,?,?)'''
        cur = conn.cursor()
        now = datetime.utcnow()
        cur.execute(sql_insert,(val[0],price,now))
        conn.commit()
        cur = conn.cursor()
        sql_last_update = '''SELECT * from app_item WHERE item_id = ?'''
        cur.execute(sql_last_update,(val[0],))
        last_update = cur.fetchall()
        for last in last_update:
            print(last[1])
            print(price)
            if last[1] > price:
                list_of_discounts.append(val[0])
        sql_update = '''UPDATE app_item SET price = ? where item_id = ? '''
        cur = conn.cursor()
        cur.execute(sql_update, (price, val[0]))
    conn.commit()
    cur.close()
    return list_of_discounts

def sendDiscountEmails(conn, list_of_discounts):
    # cur = conn.cursor()
    # cur.execute("SELECT * FROM app_item")
    # print([description[0] for description in cur.description])
    # cur = con.cursor()
    # cur.execute("SELECT * FROM app_basketitem")
    # print([description[0] for description in cur.description])
    # cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # print(cur.fetchall())
    mh = MailHandler(587, 'smtp.gmail.com', 'noreply.PSN.Checker@gmail.com', 'Psn12345')
    cur = conn.cursor()
    cur.execute("SELECT * FROM auth_user")
    # print([description[0] for description in cur.description])
    for user in cur.fetchall():
        game_names = []
        game_prices = []
        game_url = []
        cur = conn.cursor()
        cur.execute("SELECT * FROM app_basketitem where user_id_id = ?",(user[0],))
        # print([description[0] for description in cur.description])
        for item in cur.fetchall():
            if item[1] in list_of_discounts:
                cur = conn.cursor()
                cur.execute("SELECT * FROM app_item WHERE item_id = ?",(item[1],))
                # print([description[0] for description in cur.description])
                item_details = cur.fetchall()[0]
                game_names.append(item_details[10])
                game_prices.append(item_details[1])
                game_url.append(item_details[4])
        if len(game_names) > 0:
            mh.sendDiscount(user[4], user[6], game_names, game_prices, game_url)
    conn.close()


def app():
    con = create_conn()
    list_of_discounts = update_values(con)
    print(list_of_discounts)
    sendDiscountEmails(con, list_of_discounts)

scheduler = BlockingScheduler()
scheduler.add_job(app, 'interval', hours=1)
scheduler.start()
