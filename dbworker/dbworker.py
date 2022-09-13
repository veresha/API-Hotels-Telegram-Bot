import sqlite3 as sq


def create_table():
    with sq.connect('db_history.db') as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS history(
                       id INTEGER PRIMARY KEY autoincrement,
                       uid TEXT,
                       chat_id TEXT,
                       datetime TEXT,
                       city TEXT,
                       hotel_name TEXT,
                       checkin TEXT,
                       checkout TEXT,
                       quantity TEXT,
                       commands TEXT,
                       price_min TEXT,
                       price_max TEXT,
                       distance TEXT,
                       site TEXT,
                       price TEXT,
                       total_price TEXT);
                    """)


def set_history(history: dict) -> None:
    with sq.connect('db_history.db') as con:
        cur = con.cursor()
        cur.execute(f"INSERT INTO history(uid, chat_id, datetime, city, hotel_name, checkin, checkout, quantity, "
                    f"commands, price_min, price_max, distance, site, price, total_price) "
                    f"VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", history)


def get_history(user_id: str):
    with sq.connect('db_history.db') as con:
        cur = con.cursor()
        cur.execute(f"SELECT uid, datetime, commands, city, hotel_name, quantity, checkin, checkout, price_min, "
                    f"price_max, site, distance, total_price from history WHERE chat_id = '{user_id}'")
        return cur.fetchall()
