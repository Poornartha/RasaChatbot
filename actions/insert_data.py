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


def create_user(conn, user):

    sql = ''' INSERT INTO users(name,sender_id,emp_id)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid


def create_slot(conn, slot):

    sql = ''' INSERT INTO slots(start,end)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, slot)
    conn.commit()
    return cur.lastrowid



def create_calender(conn, calender):
    sql = ''' INSERT INTO calender(user_id,slot_id)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, calender)
    conn.commit()
    return cur.lastrowid


def create_interview(conn, interview):
    sql = ''' INSERT INTO interviews(location,mode)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, interview)
    conn.commit()
    return cur.lastrowid

def create_schedule(conn, schedule):
    sql = ''' INSERT INTO schedule(user_id,interview_id)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, schedule)
    conn.commit()
    return cur.lastrowid   


def actions_user_create(username, sender_id, emp_id):
    database = r"database.db"
    conn = create_connection(database)

    with conn:
        user = (username, sender_id, emp_id)
        user_id = create_user(conn, user)
        print("User Created with ID: ", user_id)


def main():
    
    # Enter Path where you want your database to be:
    database = r"database.db"


    # create a database connection => Db will be created if there does not exists one.
    conn = create_connection(database)

    # Insert Values in Tables
    with conn:

        # user = ('Poornartha Sawant', '12775630', '100')
        # user_id = create_user(conn, user)


        # slot = ('2015-01-01', '2015-01-02')
        # slot_id = create_slot(conn, slot)


        # calender = (user_id, slot_id)
        # calender_id = create_calender(conn, calender)

        interview = ('Canada', 'Online')
        interview_id = create_interview(conn, interview)

        # schedule = (user_id, interview_id)
        # schedule_id = create_schedule(conn, schedule)

        print("Data Added")


if __name__ == '__main__':
    main()