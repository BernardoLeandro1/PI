import requests

class Phone:

    def __init__(self):
        self.f = open("actions/contacts.txt", "r")
        self.contacts = {}
        for line in self.f:
            contact = line.split("-")
            if len(contact)>1:
                self.contacts[contact[0]] = contact[1].removesuffix("\n")
        print(self.contacts)
        self.f.close()

    
    def make_call(self, contact):
        number = 0
        print(contact, str(contact).capitalize())
        if str(contact).capitalize() in self.contacts:
            number = self.contacts[contact]
        if number == 0:
            return "Contacto não encontrado"
        try:
            call = requests.get("http://192.168.1.200:3001/call/" + number)
            return "A ligar a " + contact
        except Exception as e:
            print(e)
            return "De momento, não consigo realizar essa chamada. Tente mais tarde!"
    

    def add_contact(self, name, number):
        file = open("actions/contacts.txt", "a")
        contact = "\n" + str(name) + "-+351" + str(number)
        print(name)
        print(number)
        if (name != None and number != None):
            file.write(contact)
            message = "Contacto adicionado!"
        else:
            message = "Não foi possível adicionar o contacto, tente mais tarde!"
        file.close()
        return message

