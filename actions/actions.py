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


class AskSlot(Action):

    def name(self) -> Text:
        return "ask_slot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello, will you be on 26th April at 12 PM?")

        return []


class SlotAccepted(Action):

    def name(self) -> Text:
        return "accept_slot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        dispatcher.utter_message(text="Thank you for accepting the slot.")

        return []


class SlotRejected(Action):

    def name(self) -> Text:
        return "reject_slot"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        d = tracker.latest_message['entities']
        t = d[0]
        v = t["value"]
        print(v)
        s = "The Slot has been rejected. New Slot is {}".format(v)
        dispatcher.utter_message(text=s)

        return []

class GetSlot(Action):

    def name(self) -> Text:
        return "get_slot"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        time = tracker.get_slot("time")
        print(time)
        time_object = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%f%z")
        print(time_object)
        dispatcher.utter_message("Please wait for a few moments till we get back to you.")

        return []