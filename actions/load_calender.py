import sqlite3
from sqlite3 import Error
import numpy as np 
import pandas as pd
from datetime import datetime, time


def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def fetch_slots(conn):
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM slots;')

    rows = cur.fetchall()

    slots = []
    for row in rows:
        slots.append(row)

    return slots

def create_calender(conn, calender):
    sql = ''' INSERT INTO calender(user_id,slot_id)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, calender)
    conn.commit()
    return cur.lastrowid

def main():
    
    # Enter Path where you want your database to be:
    database = r"database.db"


    # create a database connection => Db will be created if there does not exists one.
    conn = create_connection(database)

    with conn:

        slots = fetch_slots(conn)

        for slot in slots:

            calender = (3, slot[0])
            create_calender(conn, calender)
            calender = (4, slot[0])
            create_calender(conn, calender)
            calender = (5, slot[0])
            create_calender(conn, calender)


if __name__ == '__main__':
    main()
