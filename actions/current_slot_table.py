import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    
    database = r"database.db"
    conn = create_connection(database)

    sql_create_status_table = """ CREATE TABLE IF NOT EXISTS status (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    interview_id integer not null,
                                    interviewer_1 integer not null,
                                    interviewer_2 integer not null,
                                    interviewer_3 integer not null,
                                    FOREIGN KEY (interview_id) REFERENCES interviews (id) ON DELETE CASCADE
                                ); """

    if conn is not None:

        create_table(conn, sql_create_status_table)

        print("Database Created")
    else:
        print("Error! cannot create the database connection.")
    

if __name__ == '__main__':
    main()
