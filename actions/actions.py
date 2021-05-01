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

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []


class InsertInformation(Action):

    def name(self) -> Text:
        return "insert_information"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        print('This is the entity',tracker.latest_message["entities"])
        print('This is the slot',tracker.slots)
        print('Username:',tracker.get_slot("username"))
        print('Empid:',tracker.get_slot("empid"))
        print('Sender Id is:', tracker.sender_id)
        dispatcher.utter_message(text="Hello, will you be on 26th April at 12 PM?")
        return []

class AskSlot(Action):

    def name(self) -> Text:
        return "ask_slot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Would you be available on 2nd May 12pm!!")

        return []

class SlotAccepted(Action):

    def name(self) -> Text:
        return "accept_slot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #   Just insert the accepted slot in database
        dispatcher.utter_message(text="Thank you for accepting the slot.")

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