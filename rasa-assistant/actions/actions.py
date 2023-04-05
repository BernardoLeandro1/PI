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

import datetime
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
from datetime import datetime, timedelta

class CreateEventAction(Action):
    def name(self) -> Text:
        return "action_create_event"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try: 
            import argparse
            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            flags=None
        SCOPES = 'https://www.googleapis.com/auth/calendar'
        store= file.Storage('storage.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow=client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds=tools.run_flow(flow, store, flags) \
                if flags else tools.run(flow, store)
        # Get the user's Google credentials
        #creds = Credentials.from_authorized_user_info(tracker.get_slot("google_auth"))

        # Authenticate and build the Google Calendar service
        service = build('calendar', 'v3', credentials=creds)

        # Get the event details from the user
        event_title = tracker.get_slot("event_title")
        event_location = tracker.get_slot("event_location")
        event_description = tracker.get_slot("event_description")
        event_date = datetime.strptime(tracker.get_slot("event_date"), "%Y-%m-%d").date()
        event_start_time = datetime.strptime(tracker.get_slot("event_start_time"), "%H:%M").time()
        event_end_time = datetime.strptime(tracker.get_slot("event_end_time"), "%H:%M").time()

        # Create the start and end datetime objects for the event
        event_start_datetime = datetime.combine(event_date, event_start_time).isoformat()
        event_end_datetime = datetime.combine(event_date, event_end_time).isoformat()

        # Create the event object
        event = {
          'summary': event_title,
          'location': event_location,
          'description': event_description,
          'start': {
            'dateTime': event_start_datetime,
            'timeZone': tracker.get_slot("timezone"),
          },
          'end': {
            'dateTime': event_end_datetime,
            'timeZone': tracker.get_slot("timezone"),
          },
          'reminders': {
            'useDefault': True,
          },
        }

        try:
            # Insert the event into the user's calendar
            event = service.events().insert(calendarId='primary', body=event).execute()
            dispatcher.utter_message("Event created: {}".format(event.get('htmlLink')))
        except HttpError as error:
            dispatcher.utter_message("Error creating event: {}".format(str(error)))

        return [SlotSet("event_title", None), SlotSet("event_location", None), SlotSet("event_description", None),
                SlotSet("event_date", None), SlotSet("event_start_time", None), SlotSet("event_end_time", None)]
