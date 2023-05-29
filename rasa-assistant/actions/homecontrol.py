#Cenas para home control
import requests
from actions.lightsimulator import lightssss

class SwitchLights:
    def __init__(self, lightsimulator):
        self.mockLights = {"quarto": "0", "quarto de banho" : "1", "casa de banho" : "1", "sala" : "2", "cozinha": "3", "dispensa": "4", "entrada" : "5", "espelho": "6"}
        self.realLights = {"quarto": "19", "sala" : "18"}
        self.wn = lightsimulator

    def switchlight(self, switch, place):
        id = None
        onoff = None
        for a in self.realLights:
            if place == a:
                id = self.realLights[a]
        if id == None:
            for a in self.mockLights:
                if place == a:
                    id = self.mockLights[a]
        if str(switch).lower().__contains__("desliga") or str(switch).lower().__contains__("apaga"):
            onoff = 0
        elif str(switch).lower().__contains__("liga") or str(switch).lower().__contains__("acende"):
            onoff = 1
        try:
            #alldevices = requests.get("http://localhost:3010/getDevices")
            alldevices = requests.get("http://192.168.1.200:3010/getDevices")
            print(f"all devices:  {alldevices.text}")
            for dev in alldevices.json():
                if dev["id"] == int(id):
                    if dev["switchedOn"] == True and onoff == 0:
                        response = requests.get("http://192.168.1.200:3010/setOnOff/" + id + "/" + str(onoff))
                        message = "A luz que pediu foi apagada"
                    elif dev["switchedOn"] == True and onoff == 1:
                        message = "A luz já está acesa!"
                    elif dev["switchedOn"] == False and onoff == 0:
                        message = "A luz já está apagada!"
                    elif dev["switchedOn"] == False and onoff == 1:
                        response = requests.get("http://192.168.1.200:3010/setOnOff/" + id + "/" + str(onoff))
                        message = "A luz que pediu foi acesa"
        except:
            print("Faking it")
            """
            if onoff == 1:
                response = self.wn.turn_on(place)
            else:
                response = self.wn.turn_off(place)
            print(response)
            print(onoff)
            if response == "OK" and onoff == 1:
                message = "A luz que pediu foi acesa!"
            elif response == "OK" and onoff == 0:
                message = "A luz que pediu foi apagada!"
            elif response == "Done" and onoff == 1:
                return "A luz que pediu já está acesa!"
            elif response == "Done" and onoff == 0:
                message = "A luz que pediu já está apagada!"
            else: 
                message = "De momento, não consigo realizar o que pediu. Tente mais tarde!"
            """
        return message
    
    def light_cost(self, place):
        ids = []
        value = 0
        for a in self.realLights:
            if place == a:
                id = self.realLights[a]
        try:
            if str(place).__contains__("casa"):
                alldevices = requests.get("http://192.168.1.200:3010/getDevices")
                for dev in alldevices.json():
                    ids.append(dev["id"])
                for id in ids:
                    value += requests.get("http://192.168.1.200:3010/getConsumption/" + id).json()["consumedMW"]
                message = "O consumo total da casa é" + str(value)
            else:
                value = requests.get("http://192.168.1.200:3010/getConsumption/" + id).json()["consumedMW"]
                message = "O consumo pedido é" + str(value)
        except:
            message = "De momento, não tenho valores de consumo para essa luz! Tente mais tarde!"
        return message