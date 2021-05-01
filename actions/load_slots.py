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

def create_slot(conn, slot):

    sql = ''' INSERT INTO slots(start,end)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, slot)
    conn.commit()
    return cur.lastrowid

def main():

    # Enter Path where you want your database to be:
    database = r"database.db"


    # create a database connection => Db will be created if there does not exists one.
    conn = create_connection(database)

    read_data = pd.read_excel('output.xlsx', engine='openpyxl')
    data = pd.DataFrame()
    data['Start'] = read_data['Start']
    data['End'] = read_data['End']
    
    free_slots = [(data['Start'][i], data['End'][i]) for i in data.index]

    for i in free_slots:
        # print(i[0].isoformat(), i[1].isoformat())
        slot = (i[0].isoformat(), i[1].isoformat())
        slot_id = create_slot(conn, slot)

    print("Slots Loaded")


if __name__ == '__main__':
    main()