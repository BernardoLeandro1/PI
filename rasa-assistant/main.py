import requests
import sys
from VoiceModule import VoskInputVoiceModule, OutputVoiceModule, GoogleInputVoiceModule
import tkinter as tk
import threading

class Assistant:

    def __init__(self) -> None:
        ASSISTANT_NAME = "assistente"
        self.WAKE_UP = [
            "oi " + ASSISTANT_NAME, 
            "bom dia "+ ASSISTANT_NAME, 
            "boa tarde "+ ASSISTANT_NAME,
            "boa noite "+ ASSISTANT_NAME,
            "olá "+ ASSISTANT_NAME,
            "olá",
                        ]
        self.SLEEP = [ 
            "xau "+ ASSISTANT_NAME,
            "adeus "+ ASSISTANT_NAME,
            "até logo "+ ASSISTANT_NAME,
            "boa noite "+ ASSISTANT_NAME,
            "até amanhã "+ ASSISTANT_NAME,
            "adeus",
            ]
        self.GOODBYE = [
            "Adeus!",
        ]
        
        #self.listener = VoskInputVoiceModule()
        self.listener = GoogleInputVoiceModule()
        self.speaker = OutputVoiceModule()     
        
        # GUI
        window = tk.Tk()
        window.title("CasaViva+")
        window.geometry('200x150+50+50')
        text = tk.Label(text ="🤖",justify="center", font=("Arial", 125))
        text.pack()
        
        threading.Thread(target=self.run).start()
        window.mainloop()
    
    def run(self):
        print( "Assistente a funcionar... \n")
        while True:
            bot_response = ""
            user_input = ""

            while user_input not in self.WAKE_UP:
                user_input = self.listener.listen()
                
            # debug    
            print("D. Maria: " + user_input) 
            bot_response = self.interact(user_input)
            #debug
            print("Assistente: " + bot_response)
            self.speaker.say(bot_response)

            while user_input not in self.SLEEP:
                user_input = self.listener.listen()
                if user_input is None:
                    continue
                # debug    
                print("D. Maria: " + user_input) 
                bot_response = self.interact(user_input)
                #debug
                print("Assistente: " + bot_response)
                self.speaker.say(bot_response)
                
                if bot_response in self.GOODBYE:
                    break
    
    def interact(self, message):
        try:
            r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": message})
            for i in  r.json() :
                response = i['text']
            return response
        except:
            error = "Ocorreu um erro com o seu assistente. Por favor volte a tentar."
            return error

Assistant()
