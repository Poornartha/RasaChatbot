import sqlite3
from sqlite3 import Error

def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def fetch_user(conn, username):
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM users where name = "{username}"')

    rows = cur.fetchall()

    for row in rows:
        print(row)

def fetch_slots(conn, user_id):
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM calender where user_id = "{user_id}"')

    rows = cur.fetchall()

    for row in rows:
        print(row)


def main():
    
    # Enter Path where you want your database to be:
    database = r"database.db"


    # create a database connection => Db will be created if there does not exists one.
    conn = create_connection(database)

    with conn:
        print("Get User: ")
        fetch_user(conn, "Poornartha Sawant")
        fetch_slots(conn, 1)

if __name__ == '__main__':
    main()