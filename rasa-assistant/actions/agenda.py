from datetime import date, datetime, timedelta
import os
import pytz
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from httplib2 import Http
from oauth2client import file, client, tools


class GoogleCalendar:
    def __init__(self, credentials_path):        
        SCOPES = 'https://www.googleapis.com/auth/calendar'
        creds= None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        self.service = build('calendar', 'v3', credentials=creds)
    

    def add_event(self, start_time , end_time, summary, location, person, occur, until):
        if (occur != None and until != None):
            recur = 'RRULE:FREQ=' + occur + ';UNTIL=' + until
            event = {
                'summary': summary,
                'location': location,
                'start': {
                    'dateTime': start_time,
                    'timeZone': 'Portugal',
                },
                'end': {
                    'dateTime': end_time,
                    'timeZone': 'Portugal',
                },
                'attendees': person,
                'recurrence': [ recur, ]

            }
            print('RRULE:FREQ=' + occur + ';UNTIL=' + until)
        else: 
            event = {
                'summary': summary,
                'location': location,
                'start': {
                    'dateTime': start_time,
                    'timeZone': 'Portugal',
                },
                'end': {
                    'dateTime': end_time,
                    'timeZone': 'Portugal',
                },
                'attendees': person,
            }
        # attendees tem de conter email, depois iremos buscar esse email aos contactos quando houver contactos
        # [
        #         {'email': 'diogomfsilva98@gmail.com'},
        #         {'email': 'luisccmartins88@gmail.com'},
        #         {'email': 'pedrocoelho485@gmail.com'},
        #         {'email': 'manu.guerra.diaz@gmail.com'},
                
        #     ],

        try:
            event = self.service.events().insert(calendarId='primary', body=event).execute()
            print(f'Event created: {event["summary"]}')
        except HttpError as error:
            print(f'An error occurred: {error}')
            event = None
        return event

    def remove_event(self, event_id):
        try:
            self.service.events().delete(calendarId=self.primary, eventId=event_id).execute()
            print(f'Event deleted: {event_id}')
            return True
        except HttpError as error:
            print(f'An error occurred: {error}')
            return False

    def edit_event(self, event_id, summary=None, start_time=None, end_time=None):
        event = self.service.events().get(calendarId=self.primary, eventId=event_id).execute()

        if summary is not None:
            event['summary'] = summary
        if start_time is not None:
            event['start']['dateTime'] = start_time.isoformat()
            event['start']['timeZone'] = start_time.tzinfo.zone
        if end_time is not None:
            event['end']['dateTime'] = end_time.isoformat()
            event['end']['timeZone'] = end_time.tzinfo.zone

        try:
            updated_event = self.service.events().update(calendarId=self.calendar_id, eventId=event_id, body=event).execute()
            print(f'Event updated: {updated_event["htmlLink"]}')
            return updated_event
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None

    def find_event(self, summary=None, start_date=None, start_time=None, end_date = None, end_time = None):
        pagetoken = None
        print(start_date)
        while True:
            events_result = self.service.events().list(calendarId='primary', orderBy= 'startTime', singleEvents=True).execute()
            items = events_result['items']
            b = []
            if end_date != None:
                for event in items:
                    a = str(event['start']['dateTime']).split("T")
                    if(a[0]>start_date and a[0]< end_date) or a[0]==start_date or a[0]==end_date:
                        print(event['summary'])
                        b.append(event)
            else: 
                for event in items:
                    a = str(event['start']['dateTime']).split("T")
                    h = a[1].split("+")[0]
                    if(a[0]==start_date and datetime.strptime(h, '%H:%M:%S') > datetime.strptime(start_time, '%H:%M:%S') and datetime.strptime(h, '%H:%M:%S') < datetime.strptime(end_time, '%H:%M:%S')):
                        print(a[1])
                        print(event['summary'])
                        b.append(event)
                
            # pagetoken = events_result.get('nextPageToken')
            # if not pagetoken:
            #     break
            return b

            #     if (not summary or summary in event['summary']) and (not start_time or start_time == event['start'].get('dateTime', None)):
            #         return event['id']
            # return None