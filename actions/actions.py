# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from datetime import datetime
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.events import ReminderScheduler
import sqlite3
from sqlite3 import Error

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []


class InsertInformation(Action):

    def create_connection(self):

        conn = None
        try:
            conn = sqlite3.connect("/home/poornartha/Desktop/Git/RasaChatbot/actions/database.db")
            return conn
        except Error as e:
            pass

        return conn

    def create_user(self, conn, user):

        sql = ''' INSERT INTO users(name,sender_id,emp_id)
                VALUES(?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, user)
        conn.commit()
        return cur.lastrowid


    def fetch_slots(self, conn):
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM slots;')

        rows = cur.fetchall()

        slots = []
        for row in rows:
            slots.append(row)

        return slots

    def create_calender(self, conn, calender):
        sql = ''' INSERT INTO calender(user_id,slot_id)
                VALUES(?,?) '''
        cur = conn.cursor()
        cur.execute(sql, calender)
        conn.commit()
        return cur.lastrowid

    def name(self) -> Text:
        return "insert_information"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        username = tracker.get_slot("username")
        empid = tracker.get_slot("empid")
        senderid = tracker.sender_id

        print('Username:', username)
        print('Empid:', empid)
        print('Sender ID:', senderid)
        
        conn = self.create_connection()
        try:
            with conn:
                user = (username, senderid, empid)
                user_id = self.create_user(conn, user)
                slots = self.fetch_slots(conn)

                for slot in slots:
                    calender = (user_id, slot[0])
                    self.create_calender(conn, calender)

        except Exception:
            pass
        dispatcher.utter_message(text="Thankyou for your information")

        return []

class AskSlot(Action):


    def create_connection(self):

        conn = None
        try:
            conn = sqlite3.connect("/home/poornartha/Desktop/Git/RasaChatbot/actions/database.db")
            return conn
        except Error as e:
            pass

        return conn

    def fetch_user(self, conn, sender_id):
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM users where sender_id = "{sender_id}"')

        row = cur.fetchone()

        return row


    def fetch_calender(self, conn, user_id):
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM calender where user_id = {user_id}')

            row = cur.fetchone()

            return row

    def fetch_slot(self, conn, slot_id):
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM slots where id = "{slot_id}"')

            row = cur.fetchone()

            return row

    def create_status(self, conn, status):

        sql = ''' INSERT INTO status(interview_id,slot_id,interviewer_1,interviewer_2,interviewer_3)
                    VALUES(?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, status)
        conn.commit()
        return cur.lastrowid

    def create_user_status(self, conn, user_status):

        sql = ''' INSERT INTO user_status(user_id,status_id,active)
                    VALUES(?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, user_status)
        conn.commit()
        return cur.lastrowid


    def fetch_status(self, conn, slot_id, interview_id):
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM status where slot_id = "{slot_id}" and interview_id = {interview_id}')
        row = cur.fetchone()
        return row

    def name(self) -> Text:
        return "ask_slot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = self.create_connection()
        sender_id = tracker.sender_id
        try:
            with conn:
                # dispatcher.utter_message(text=f'Would you be available on {sender_id}')
                user = self.fetch_user(conn, sender_id)
                print(user)
                calender = self.fetch_calender(conn, user[0])
                # dispatcher.utter_message(text=f'Would you be available on {calender}')
                slot_id = calender[2]
                slot = self.fetch_slot(conn, slot_id)
                dispatcher.utter_message(text=f'Would you be available on {slot[1]}')
                status_id = self.fetch_status(conn, slot[0], 4)
                if status_id == None:
                    status_data = (4, slot[0], 0, 0, 0)
                    status_id = self.create_status(conn, status_data)
                user_status_data = (user[0], status_id[0], 1)
                user_status = self.create_user_status(conn, user_status_data)
                dispatcher.utter_message(text=f'Your Interview ID is: {status_id[0]}')
        except Exception as e:
            dispatcher.utter_message(text=f'Error Occured! {e}')

        return []

class SlotAccepted(Action):

    def create_connection(self):

        conn = None
        try:
            conn = sqlite3.connect("/home/poornartha/Desktop/Git/RasaChatbot/actions/database.db")
            return conn
        except Error as e:
            pass

        return conn

    def fetch_user_status(self, conn, user_id):
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM user_status where user_id = "{user_id}"')
        row = cur.fetchone()
        return row

    def fetch_user_status_status(self, conn, status_id):
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM user_status where status_id = {status_id}')
        users = []
        for row in cur.fetchall():
            users.append(self.fetch_user_id(conn, row[1])[1])
        return users

    def fetch_status(self, conn, status_id):
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM status where id = {status_id}')
        row = cur.fetchone()
        return row

    def fetch_user(self, conn, sender_id):
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM users where sender_id = "{sender_id}"')

        row = cur.fetchone()

        return row   

    def fetch_user_id(self, conn, id):
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM users where id = "{id}"')

        row = cur.fetchone()

        return row     

    def update_status(self, conn, status):
        sql = '''UPDATE status set interviewer_1 = ?, interviewer_2 = ?, interviewer_3 = ? where id = ?'''
        cur = conn.cursor()
        cur.execute(sql, status)
        conn.commit()

    def name(self) -> Text:
        return "accept_slot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

    
        sender_id = tracker.sender_id
        conn = self.create_connection()

        try:
            with conn:
                user = self.fetch_user(conn, sender_id)
                user_status = self.fetch_user_status(conn, user[0])
                status_id = user_status[2]
                status = self.fetch_status(conn, status_id)
                (s_id, i_id, slot_id, interviewer_1, interviewer_2, interviewer_3) = status
                if interviewer_1 and interviewer_2:
                    interviewer_3 = 1
                    dispatcher.utter_message(text=f'Slot has been confirmed.')
                    users_confirmed = self.fetch_user_status_status(conn, status_id)
                    for user_selected in users_confirmed:
                        dispatcher.utter_message(text=f'Interviewers: {user_selected}')
                elif interviewer_1:
                    interviewer_2 = 1
                else:
                    interviewer_1 = 1
                status_data = (interviewer_1, interviewer_2, interviewer_3, s_id)

                self.update_status(conn, status_data)

                dispatcher.utter_message(text=f'Thank you for accepting the slot for Interview ID: {status_data[3]}')
        except Exception as e:
            dispatcher.utter_message(text=f'Thank you for accepting the slot: {e}')
        
        #   Just insert the accepted slot in database
        # Fetch User
        # Fetch Status
        # Fetch Slot 
        # Check if other interviewers have said True
        # add True
        dispatcher.utter_message(text="Thank You")

        return []


class SlotRejected(Action):

    def name(self) -> Text:
        return "reject_slot"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #   Check for given slot whether it is in free slots in database
        #   if not in free slots then ask the same user about the slot
        #   again repeat the procedure 
        #   Confirm with other interviews about the slot
        #   Revert back to the users for the slot

        d = tracker.latest_message['entities']
        t = d[0]
        v = t["value"]
        print(v)
        s = "The Slot has been rejected. New Slot is {}".format(v)
        dispatcher.utter_message(text=s)

        return []

class GetSlot(Action):

    # def __init__(self):
    #     self.sender_dict = dict()

    def name(self) -> Text:
        return "get_slot"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conversation_id = tracker.sender_id

        # time = tracker.get_slot("time")
        # print(time)
        # time_object = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f%z")
        # print(time_object)
        # self.sender_dict[tracker.sender_id] = [{'time_value' : time_object , 'boolean_value' : True}]
        # print('This is the sender id',tracker.sender_id)

        # # print('This is the dictionary',self.sender_dict)
        # # print('This is the slots',tracker.slots)
        # # print('This is the events',tracker.events)
        # # print('This is the latest message',tracker.latest_message)

        dispatcher.utter_message("Please wait for a few moments till we get back to you. {} ".format(conversation_id))

        return []

class GiveSchedule(Action):

    def name(self) -> Text:
        return "give_schedule"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        sender_id = tracker.sender_id

        #   With the sender id we can fetch interviews of the respective user along with time 

        text = "Following are the interviews:- " #  interviews with timw with respect to user
        dispatcher.utter_message(text=text)

        return []

class ActionReminderInterview(Action):

    def name(self) -> Text:
        return "action_reminder_interview"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #   reminder should be set here
        dispatcher.utter_message(text="")

        return []