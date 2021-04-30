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

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY AUTOINCREMENT,
                                        name text NOT NULL,
                                        sender_id text NOT NULL UNIQUE,
                                        emp_id integer NOT NULL UNIQUE
                                    ); """

    sql_create_slots_table = """CREATE TABLE IF NOT EXISTS slots (
                                    id integer PRIMARY KEY AUTOINCREMENT, 
                                    start timestamp,
                                    end timestamp
                                );"""

    sql_create_interview_table = """CREATE TABLE IF NOT EXISTS interviews (
                                    id integer PRIMARY KEY AUTOINCREMENT, 
                                    location text,
                                    mode text
                                );"""

    sql_create_calender_table = """CREATE TABLE IF NOT EXISTS calender (
                                    id integer PRIMARY KEY AUTOINCREMENT, 
                                    user_id integer not null,
                                    slot_id integer not null,
                                    FOREIGN KEY (user_id) REFERENCES users (id) on delete cascade,
                                    FOREIGN KEY (slot_id) REFERENCES slots (id) on delete cascade
                                );"""

    sql_create_schedule_table = """CREATE TABLE IF NOT EXISTS schedule (
                                    id integer PRIMARY KEY AUTOINCREMENT,   
                                    user_id integer not null,
                                    interview_id integer not null,
                                    FOREIGN KEY (user_id) REFERENCES users (id) on delete cascade,
                                    FOREIGN KEY (interview_id) REFERENCES interviews (id) on delete cascade
                                );"""

    if conn is not None:
        # create projects table
        create_table(conn, sql_create_users_table)

        # create tasks table
        create_table(conn, sql_create_slots_table)

        # create projects table
        create_table(conn, sql_create_interview_table)

        # create tasks table
        create_table(conn, sql_create_calender_table)

        # create projects table
        create_table(conn, sql_create_schedule_table)

        print("Database Created")
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()

