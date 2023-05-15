import requests

class Phone:

    def __init__(self):
        self.contacts = {"Bernardo" : "+351913614013"}

    
    def make_call(self, contact):
        number = 0
        if contact in self.contacts:
            number = self.contacts[contact]
        if number == 0:
            return "Contacto não encontrado"
        try:
            call = requests.get("http://192.168.1.200:3001/call/" + number)
            return "A ligar a " + contact
        except Exception as e:
            print(e)
            return "De momento, não consigo realizar essa chamada. Tente mais tarde!"