# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from __future__ import print_function

#import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from httplib2 import Http
from oauth2client import file, client, tools
from typing import Dict, Text, Any, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from datetime import date, datetime, timedelta

class ActionGreetUser(Action):
    def name(self) -> Text:
        return "action_greet_user"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("name")

        if name:
            message = f"Hello {name}, how can I assist you today (python)?"
        else:
            message = "Hello, how can I assist you today? (python)?"

        dispatcher.utter_message(text=message)

        return []
    
class CreateEventAction(Action):
    def name(self) -> Text:
        return "action_create_event"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # try: 
        #      import argparse
        #      flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        # except ImportError:
        #      flags=None
        SCOPES = 'https://www.googleapis.com/auth/calendar'
        store= file.Storage('/home/bernardo/Desktop/PI/rasa-assistant/actions/storage.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow=client.flow_from_clientsecrets('/home/bernardo/Desktop/PI/rasa-assistant/actions/credentials.json', SCOPES)
            creds=tools.run_flow(flow, store, flags) \
                if flags else tools.run(flow, store)
        # Get the user's Google credentials
        #creds = Credentials.from_authorized_user_info(tracker.get_slot("google_auth"))

        # Authenticate and build the Google Calendar service
        service = build('calendar', 'v3', credentials=creds)

        # Get the event details from the user
        event_title = tracker.get_slot("event")
        #event_location = tracker.get_slot("event_location")
        #event_description = tracker.get_slot("event_description")
        #event_date = datetime.strptime(tracker.get_slot("event_date"), "%Y-%m-%d").date()
        d = str(tracker.get_slot("day")).split()
        print(tracker.get_slot("month"))
        if (tracker.get_slot("day") == None):
            event_date = date.today()
            print(event_date)
        elif (tracker.get_slot("month") == None and tracker.get_slot("day") != None):
            print(tracker.get_slot("day"))
            print(d)
            if (int(d[1]) > datetime.now().day):
                month = str(datetime.now().month)
                day = str(d[1])
                year = str(datetime.now().year)
                event_date = year + "-" + month + "-" + day
            else:
                month = str(datetime.now().month+1)
                day = str(d[1])
                year = str(datetime.now().year)
                event_date = year + "-" + month + "-" + day            
        elif (tracker.get_slot("month") != None and tracker.get_slot("day") != None):
            assistmonth = str(tracker.get_slot("month")).lower()
            match assistmonth:
                case "janeiro": 
                    month = "1"
                case "fevereiro":
                    month = "2"
                case "março":
                    month = "3"
                case "abril":
                    month = "4"
                case "maio":
                    month = "5"
                case "junho":
                    month = "6"
                case "julho":
                    month = "7"
                case "agosto":
                    month = "8"
                case "setembro":
                    month = "9"
                case "outubro":
                    month = "10"
                case "novembro":
                    month = "11"
                case "dezembro":
                    month = "12"
            day = str(d[1])
            year = str(datetime.now().year)
            event_date = year + "-" + month + "-" + day
        
        event_start_time = datetime.strptime(tracker.get_slot("hour"), "%H:%M").time()
        event_start_datetime = datetime.combine(datetime.strptime(event_date, '%Y-%m-%d'), event_start_time).isoformat()
        if (tracker.get_slot("duration") == None):
            event_end_datetime = str(datetime.strptime(event_start_datetime, '%Y-%m-%dT%H:%M:%S') + timedelta(minutes=15))
            event_end_datetime = event_end_datetime.replace(" ", "T")
        else:
            x = str(tracker.get_slot("duration")).split()
            if x[1].__contains__("hora"):
                a = int(x[0])
                event_end_datetime = str(datetime.strptime(event_start_datetime, '%Y-%m-%dT%H:%M:%S') + timedelta(hours=a))
                event_end_datetime = event_end_datetime.replace(" ", "T")
            elif x[1].__contains__("minutos"):
                a = int(x[0])
                event_end_datetime = str(datetime.strptime(event_start_datetime, '%Y-%m-%dT%H:%M:%S') + timedelta(minutes=a))
                event_end_datetime = event_end_datetime.replace(" ", "T")
    
        

        # Create the start and end datetime objects for the event
        
        #event_end_datetime = datetime.combine(event_date, event_end_time).isoformat()

        # Create the event object
        # event = {
        #   'summary': event_title,
        #   'location': event_location,
        #   'description': event_description,
        #   'start': {
        #     'dateTime': event_start_datetime,
        #     'timeZone': tracker.get_slot("timezone"),
        #   },
        #   'end': {
        #     'dateTime': event_end_datetime,
        #     'timeZone': tracker.get_slot("timezone"),
        #   },
        #   'reminders': {
        #     'useDefault': True,
        #   },
        # }
        print(event_start_datetime)
        print(event_end_datetime)
        event = {
            'summary': event_title,
            'start': {
             'dateTime': event_start_datetime,
             'timeZone': 'Portugal',
           },
           'end': {
             'dateTime': event_end_datetime,
             'timeZone': 'Portugal',
           }
        }

        try:
            # Insert the event into the user's calendar
            event = service.events().insert(calendarId='primary', body=event).execute()
            dispatcher.utter_message("Evento criado: {} às {}".format(tracker.get_slot("event"), tracker.get_slot("hour")))
        except HttpError as error:
            dispatcher.utter_message("Erro ao criar o evento: {}".format(str(error)))

        return [SlotSet("event", None), SlotSet("duration", None), SlotSet("hour", None),
                SlotSet("occurrence", None), SlotSet("person", None), SlotSet("month", None), SlotSet("day_of_week", None), SlotSet("day", None)]