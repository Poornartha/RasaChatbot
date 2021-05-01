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



def delete_slot(conn, id):

    sql = 'DELETE FROM slots WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()


def main():

    # Enter Path where you want your database to be:
    database = r"database.db"

    # create a database connection => Db will be created if there does not exists one.
    conn = create_connection(database)

    with conn:
        delete_slot(conn, 1);




if __name__ == '__main__':
    main()