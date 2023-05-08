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

import os.path
import re

from word2numberi18n import w2n
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from httplib2 import Http
from oauth2client import file, client, tools
from typing import Dict, Text, Any, List, Union
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from datetime import date, datetime, timedelta
from actions import agenda, weather
import GLOBAL
from rasa_sdk.events import SessionStarted, ActionExecuted
from rasa_sdk.types import DomainDict

class ValidateCheckEventDataForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_check_event_data_form"
    
    def validate_event(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `event` value."""
        print(tracker.get_slot("event"))
        if slot_value == None:
            dispatcher.utter_message(text=f"Não percebi a atividade que queria que marcasse, pode repetir?.")
            return {"event": None}
        else:
            return {"event": slot_value}

    def validate_hour(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `hour` value."""
        print(tracker.get_slot("hour"))
        # regex = "^([01]?[0-9]|2[0-3]):[0-5][0-9]$"
        # p = re.compile(regex)
        # m = re.search(p, slot_value)
        if slot_value == None:
            dispatcher.utter_message(text=f"Não percebi a que horas queria realizar a atividade, pode repetir?.")
            return {"hour": None}
        elif tracker.get_slot("event") == None:
            dispatcher.utter_message(text=f"Não percebi a atividade que queria que marcasse, pode repetir?.")
            return {"event": None} 
        else:
            dispatcher.utter_message("Quer que marque {}, às {}?".format(tracker.get_slot("event"), tracker.get_slot("hour")))
            return {"event": tracker.get_slot("event"), "hour": slot_value}

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
        
     
        #print(domain)       

        calendar = agenda.GoogleCalendar("actions/credentials.json")
        d = str(tracker.get_slot("day")).split()
        if(len(d)>1):
            d = d[1]
        else:
            d =d[0]
        occur = None
        if (str(tracker.get_slot("occurrence")).lower().__contains__("dias") or str(tracker.get_slot("occurrence")).lower().__contains__("diariamente")):
            occur = "DAILY"
        elif(str(tracker.get_slot("occurrence")).lower().__contains__("meses") or str(tracker.get_slot("occurrence")).lower().__contains__("mensalmente")):
            occur = "MONTHLY"
        elif(str(tracker.get_slot("occurrence")).lower().__contains__("anualmente")):
            occur= "ANNUALY"
        else:
            occur = "WEEKLY"
            if str(tracker.get_slot("occurrence")).lower().__contains__("segunda"):
                SlotSet("day_of_week", "segunda")
            if str(tracker.get_slot("occurrence")).lower().__contains__("terça"):
                SlotSet("day_of_week", "terça")
            if str(tracker.get_slot("occurrence")).lower().__contains__("quarta"):
                SlotSet("day_of_week", "quarta")
            if str(tracker.get_slot("occurrence")).lower().__contains__("quinta"):
                SlotSet("day_of_week", "quinta")
            if str(tracker.get_slot("occurrence")).lower().__contains__("sexta"):
                SlotSet("day_of_week", "sexta")
            if str(tracker.get_slot("occurrence")).lower().__contains__("sabado"):
                SlotSet("day_of_week", "sabado")
            if str(tracker.get_slot("occurrence")).lower().__contains__("domingo"):
                SlotSet("day_of_week", "domingo")
        instance = w2n.W2N(lang_param="pt")
        horas= 0
        minutos = 0
        a=str(tracker.get_slot("hour"))
        # Uncoment if voice recognition can't process numbers and gives them extended
        if a.__contains__("tarde") or a.__contains__("noite"):
            b = a.split(" ")
            print(a)
            horario = b[0].split(":")
            print(horario)
            horario[0] = int(horario[0]) + 12
            a = str(horario[0]) + ":" + str(horario[1])
        """
        
        if a.__contains__("hora"):
            b = a.split("hora")
            horas = b[0]
            print(horas)
            if horas.__contains__("uma"):
                horas = "um"
            elif horas.__contains__("duas"):
                horas = "dois"
            elif horas.__contains__("vinte e uma"):
                horas = "vinte e um"
                print(horas)
            elif horas.__contains__("vinte e duas"):
                horas = "vinte e dois"
            if b[1].__contains__("minutos"):
                b[1].removesuffix("minutos")
                minutos = b[1][b[1].find("e")+1 : len(b[1])]
            else:
                if len(b[1]) > 2:
                    minutos = b[1][b[1].find("e")+1 : len(b[1])]

        else:
            b = a.split(" ")
            if len(b)==3:
                horas = b[0]
                if horas.__contains__("uma"):
                    horas = "um"
                elif horas.__contains__("duas"):
                    horas = "dois"
                minutos = b[2]
            if len(b) == 5:
                horas = b[0] + " " + b[1] + " "  + b[2]
                if horas.__contains__("vinte e uma"):
                    horas = "vinte e um"
                elif horas.__contains__("vinte e duas"):
                    horas = "vinte e dois"
                minutos = b[4]
                if instance.word_to_num(horas) > 24:
                    horas = b[0]
                    if horas.__contains__("uma"):
                        horas = "um"
                    elif horas.__contains__("duas"):
                        horas = "dois"
            
                    minutos = b[2] + " " + b[3] + " "  + b[4]
            if len(b) == 7:
                horas = b[0] + " " + b[1] + " "  + b[2] 
                if horas.__contains__("uma"):
                    horas = "um"
                elif horas.__contains__("duas"):
                    horas = "dois"
                elif horas.__contains__("vinte e uma"):
                    horas = "vinte e um"
                    print(horas)
                elif horas.__contains__("vinte e duas"):
                    horas = "vinte e dois"
                minutos = b[4] + " " + b[5] + " "  + b[6] 
        
        if horas == "dezassete":
            horario =  "17:" + str(instance.word_to_num(minutos))
        elif minutos == "dezassete":
            horario =  str(instance.word_to_num(horas)) + ":17"
        else:
            horario = str(instance.word_to_num(horas)) + ":" + str(instance.word_to_num(minutos))
        
        print(horario)
        event_start_time = datetime.strptime(horario, "%H:%M").time()
        """
        event_start_time = datetime.strptime(a, "%H:%M").time()
        hn = str(datetime.today().hour)
        mn = str(datetime.today().minute)
        now = hn+":"+mn
        if(tracker.get_slot("hour") != None):
            if (tracker.get_slot("day") == None):
                if (tracker.get_slot("day_of_week")!= None):
                    if (str(tracker.get_slot("day_of_week")).lower == "amanhã"):
                        event_date = str(datetime.today().date() + timedelta(days=1))
                    else:
                        assistday = str(tracker.get_slot("day_of_week")).lower()
                        match assistday:
                            case "segunda": 
                                weekday = 0
                            case "terça":
                                weekday = 1
                            case "quarta":
                                weekday = 2
                            case "quinta":
                                weekday = 3
                            case "sexta":
                                weekday = 4
                            case "sabado":
                                weekday = 5
                            case "domingo":
                                weekday = 6
                        d = datetime.today().date()
                        print("AAAAAAAAAAAAAAAAaa")
                        print(tracker.get_slot("day_of_week"))
                        print(d)
                        days_ahead = weekday - d.weekday()
                        if days_ahead <= 0: # Target day already happened this week
                            days_ahead += 7
                        event_date = str(d + timedelta(days=days_ahead))
                else:
                    print(event_start_time)
                    if datetime.strptime(str(a), "%H:%M").time() > datetime.strptime(now, "%H:%M").time() :
                        event_date = str(date.today())
                    else:
                        day = str(datetime.today().day+1)
                        month = str(datetime.now().month)
                        year = str(datetime.now().year)
                        event_date = year + "-" + month + "-" + day
            elif (tracker.get_slot("month") == None and tracker.get_slot("day") != None):
                if (int(d) > datetime.now().day):
                    month = str(datetime.now().month)
                    day = str(d)
                    year = str(datetime.now().year)
                    event_date = year + "-" + month + "-" + day
                else:
                    month = str(datetime.now().month+1)
                    day = str(d)
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
                day = str(d)
                print(d)
                year = str(datetime.now().year)
                event_date = year + "-" + month + "-" + day
            

            

            
            until = None
            event_start_datetime = datetime.combine(datetime.strptime(event_date, '%Y-%m-%d'), event_start_time).isoformat()
            new_hour = str(datetime.strptime(event_start_datetime, '%Y-%m-%dT%H:%M:%S') + timedelta(minutes=30))
            new_hour = new_hour.replace(" ", "T")
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
                elif x[1].__contains__("dia"):
                    f = instance.word_to_num(x[0])

                    until = str(datetime.strptime(new_hour, '%Y-%m-%dT%H:%M:%S') + timedelta(days=f))
                    until = until.replace(" ", "T")
                    until = until.replace(":", "")
                    until = until.replace("-", "")
                    until = until.__add__("Z")
                    event_end_datetime = str(datetime.strptime(event_start_datetime, '%Y-%m-%dT%H:%M:%S') + timedelta(minutes=15))
                    event_end_datetime = event_end_datetime.replace(" ", "T")
                elif x[1].__contains__("semana"):
                    if (x[0].__contains__("uma")):
                        x[0] = "um"
                    elif (x[0].__contains__("duas")):
                        x[0] = "dois"
                    f = instance.word_to_num(x[0])
                    until = str(datetime.strptime(new_hour, '%Y-%m-%dT%H:%M:%S') + timedelta(weeks=f))
                    until = until.replace(" ", "T")
                    until = until.replace(":", "")
                    until = until.replace("-", "")
                    until = until.__add__("Z")
                    event_end_datetime = str(datetime.strptime(event_start_datetime, '%Y-%m-%dT%H:%M:%S') + timedelta(minutes=15))
                    event_end_datetime = event_end_datetime.replace(" ", "T")
                elif x[1].__contains__("mes") or x[1].__contains__("mês"):
                    f = instance.word_to_num(x[0])
                    until = str(datetime.strptime(new_hour, '%Y-%m-%dT%H:%M:%S') + timedelta(month=f))
                    until = until.replace(" ", "T")
                    until = until.replace(":", "")
                    until = until.replace("-", "")
                    until = until.__add__("Z")
                    event_end_datetime = str(datetime.strptime(event_start_datetime, '%Y-%m-%dT%H:%M:%S') + timedelta(minutes=15))
                    event_end_datetime = event_end_datetime.replace(" ", "T")
                    
            print(tracker.get_slot("duration"))
            print(occur)
            print(until)
            try:
                event = calendar.add_event(event_start_datetime, event_end_datetime, tracker.get_slot("event"), tracker.get_slot("location"), tracker.get_slot("person"), occur, until)
                # transforming data and day into variables
                aux = str(event["start"]).split(":")[1]
                aux2 = aux.split("T")
                aux3 = aux2[0].split("'")[1]
                data = aux3.split("-")
                dia = data[2] + "-" + data[1] + "-" + data[0]
                hora = aux2[1] + ":" + str(event["start"]).split(":")[2] + ":" + str(event["start"]).split(":")[3].split("+")[0]
                dispatcher.utter_message("Evento criado: {} às {} do dia {}".format(event["summary"], hora, dia))
            except HttpError as error:
                dispatcher.utter_message("Erro ao criar o evento: {}".format(str(error)))

            return [SlotSet("event", None), SlotSet("duration", None), SlotSet("hour", None),
                    SlotSet("occurrence", None), SlotSet("person", None), SlotSet("month", None), SlotSet("day_of_week", None), SlotSet("day", None), SlotSet("location", None), SlotSet("person", None)]

class QueryWeatherAction(Action):

    def name(self) -> Text:
        return "action_get_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

            weatherProvider = weather.WeatherProvider()
            todayDate = datetime.today().date()

            location = str(tracker.get_slot("location"))
            
            if location == "None": 
                location = GLOBAL.CURRENT_LOCATION
            
            if (tracker.get_slot("duration")!= None and tracker.get_slot("duration") == "fim de semana"):
                days_ahead = 6 - todayDate.weekday()
                if days_ahead > 5:
                     # TODO Melhorar esta frase 
                    dispatcher.utter_message("Desculpe mas não consegui encontrar informação para uma data tão à frente. Só tenho informação relativa aos próximos cinco dias.")
                    return [SlotSet("day_of_week", None), SlotSet("day", None), SlotSet("location", None), SlotSet("duration", None)]
                
                # TODO chamar função de fim de semana

            if (tracker.get_slot("day_of_week")!= None):
                    
                    if (str(tracker.get_slot("day_of_week")).lower() == "hoje"):
                        event_date = str(datetime.today().date())
                    elif (str(tracker.get_slot("day_of_week")).lower() == "amanhã"):
                        event_date = str(datetime.today().date() + timedelta(days=1))
                    else:
                        assistday = str(tracker.get_slot("day_of_week")).lower()
                        match assistday:
                            case "segunda": 
                                weekday = 0
                            case "terça":
                                weekday = 1
                            case "quarta":
                                weekday = 2
                            case "quinta":
                                weekday = 3
                            case "sexta":
                                weekday = 4
                            case "sabado":
                                weekday = 5
                            case "domingo":
                                weekday = 6
                        
                        #print("AAAAAAAAAAAAAAAAaa")
                        #print(tracker.get_slot("day_of_week"))
                        #print(d)
                        days_ahead = weekday - todayDate.weekday()
                        if days_ahead <= 0: # Target day already happened this week
                            days_ahead += 7
                        
                        if days_ahead > 5:
                            # TODO Melhorar esta frase 
                            dispatcher.utter_message("Desculpe mas não consegui encontrar informação para uma data tão à frente. Só tenho informação relativa aos próximos cinco dias.")
                            return [SlotSet("day_of_week", None), SlotSet("day", None), SlotSet("location", None), SlotSet("duration", None)]

                        event_date = str(todayDate + timedelta(days=days_ahead))
                    # TODO chamar função

                    dispatcher.utter_message(weatherProvider.get_forecast_for_day(event_date,location))
            else:
                if (tracker.get_slot("day")!= None):
                    day = str(tracker.get_slot("day")).split()
                    if(len(day)>1):
                        day = day[1]
                    else:
                        day =day[0]
                days_ahead = day - todayDate.day
                if days_ahead <= 0:
                    # TODO Melhorar esta frase 
                    dispatcher.utter_message("Desculpe mas não consegui encontrar informação para uma data tão à frente. Só tenho informação relativa aos próximos cinco dias.")
                    return [SlotSet("day_of_week", None), SlotSet("day", None), SlotSet("location", None), SlotSet("duration", None)]
                event_date = str(todayDate + timedelta(days=days_ahead))
                # TODO chamar função
                dispatcher.utter_message(weatherProvider.get_forecast_for_day(event_date,location))


class ConfirmWeatherAction(Action):

    def name(self) -> Text:
        return "action_confirm_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        weatherProvider = weather.WeatherProvider()
        todayDate = datetime.today().date()
        
        weather =  str(tracker.get_slot("location"))
        if not weather:
            # TODO Melhorar esta frase + Ver se estamos a tratar corretamente este erro
            dispatcher.utter_message("Desculpe mas não consegui entender o que pretendia. Pode repetir?")
            return [SlotSet("day_of_week", None), SlotSet("day", None), SlotSet("location", None)]
        
        location = str(tracker.get_slot("location"))
        if not location: 
            location = GLOBAL.CURRENT_LOCATION
        
                
        if (tracker.get_slot("day_of_week")!= None):
                if (str(tracker.get_slot("day_of_week")).lower == "hoje"):
                    event_date = str(datetime.today().date())
                elif (str(tracker.get_slot("day_of_week")).lower == "amanhã"):
                    event_date = str(datetime.today().date() + timedelta(days=1))
                else:
                    assistday = str(tracker.get_slot("day_of_week")).lower()
                    match assistday:
                        case "segunda": 
                            weekday = 0
                        case "terça":
                            weekday = 1
                        case "quarta":
                            weekday = 2
                        case "quinta":
                            weekday = 3
                        case "sexta":
                            weekday = 4
                        case "sabado":
                            weekday = 5
                        case "domingo":
                            weekday = 6
                    
                    #print("AAAAAAAAAAAAAAAAaa")
        

class CheckEventAction(Action):
    def name(self) -> Text:
        return "action_check_event"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        

        calendar = agenda.GoogleCalendar("actions/credentials.json")
        print(tracker.get_slot("day_of_week"))
        event_end_date = None
        if(tracker.get_slot("day_of_week"))!= None:
            if str(tracker.get_slot("day_of_week")).lower().__contains__("amanhã"):
                event_date = str(datetime.today().date() + timedelta(days=1))
                print(event_date)
            else:
                assistday = str(tracker.get_slot("day_of_week")).lower()
                match assistday:
                    case "segunda": 
                        weekday = 0
                    case "terça":
                        weekday = 1
                    case "quarta":
                        weekday = 2
                    case "quinta":
                        weekday = 3
                    case "sexta":
                        weekday = 4
                    case "sabado":
                        weekday = 5
                    case "domingo":
                        weekday = 6
                d = datetime.today().date()
                days_ahead = weekday - d.weekday()
                if days_ahead <= 0: # Target day already happened this week
                    days_ahead += 7
                event_date = str(d + timedelta(days=days_ahead))
        else:
            event_date = str(datetime.today().date())
        
        if(tracker.get_slot("day")!=None):
            day = str(tracker.get_slot("day"))
            print(day)
            aa = day.split(" ")
            print(aa)
            dia = aa[0]
            mes = aa[2]
            print(mes)
            match mes:
                case "janeiro": 
                    mes = "1"
                case "fevereiro":
                    mes = "2"
                case "março":
                    mes = "3"
                case "abril":
                    mes = "4"
                case "maio":
                    mes = "5"
                case "junho":
                    mes = "6"
                case "julho":
                    mes = "7"
                case "agosto":
                    mes = "8"
                case "setembro":
                    mes = "9"
                case "outubro":
                    mes = "10"
                case "novembro":
                    mes = "11"
                case "dezembro":
                    mes = "12"
            ano = str(datetime.now().year)
            event_date = ano + "-" + mes + "-" + dia
            event_date = str(datetime.strptime(event_date, '%Y-%m-%d')).split(" ")[0]

        if(tracker.get_slot("duration")!=None):
            a = str(tracker.get_slot("duration"))
            if a.__contains__("próxima"):
                d = datetime.today().date()
                days_ahead = 6 - d.weekday()
                if days_ahead <= 0: # Target day already happened this week
                    days_ahead += 7
                event_date = str(d + timedelta(days=days_ahead))
                event_end_date = str(d + timedelta(days=days_ahead+7))
            elif a.__contains__("esta"):
                event_date = str(datetime.today().date())
                d = datetime.today().date()
                days_ahead = 5 - d.weekday()
                if days_ahead <= 0: # Target day already happened this week
                    days_ahead += 7
                event_end_date = str(d + timedelta(days=days_ahead))

        startTime = "00:00:00"
        endTime = "23:59:59"
        print(tracker.get_slot("hour"))
        if (tracker.get_slot("hour"))!=None:
            a = str(tracker.get_slot("hour"))
            if a.__contains__("depois"):
                startTime = a.split(" ")[2] + ":00"
            elif(a.__contains__("antes")):
                endTime = a.split(" ")[2] + ":00"
            elif(a.__contains__("entre")):
                startTime = a.split(" ")[2] + ":00"
                endTime = a.split(" ")[5] + ":00"
        print(startTime)
        try:
            events = calendar.find_event(start_date = event_date, start_time = startTime, end_date = event_end_date, end_time = endTime)
            if len(events)<1:
                dispatcher.utter_message("Não tem nada marcado")
                return [SlotSet("day_of_week", None), SlotSet("day", None), SlotSet("hour", None)]
            print()
            for event in events:
                horas = str(event['start']['dateTime']).split("T")
                dia = horas[0]
                horas = horas[1].split("+")
                
                match datetime.strptime(dia, '%Y-%m-%d').date().strftime('%A'):
                    case "Monday": 
                        weekday = "segunda"
                    case "Tuesday":
                        weekday = "terça"
                    case "Wednesday":
                        weekday = "quarta"
                    case "Thursday":
                        weekday = "quinta"
                    case "Friday":
                        weekday = "sexta"
                    case "Saturday":
                        weekday = "sabado"
                    case "Sunday":
                        weekday = "domingo"
                if(tracker.get_slot("day")!= None):
                    dispatcher.utter_message("Tem {} às {} de {}".format(event['summary'], horas[0], tracker.get_slot("day")))
                else:
                    dispatcher.utter_message("Tem {} às {} de {}".format(event['summary'], horas[0], weekday))
            return [SlotSet("day_of_week", None), SlotSet("day", None), SlotSet("hour", None)]

        except HttpError as error:
            dispatcher.utter_message("Erro ao procurar eventos!")
    
