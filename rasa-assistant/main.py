from datetime import datetime
import textwrap
import requests
import sys
from VoiceModule import VoskInputVoiceModule, OutputVoiceModule, GoogleInputVoiceModule, GoogleOutputVoiceModule
import tkinter as tk
import threading
from flask import Flask;
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
            "adeus",
            "Adeus",
        ]
        
        self.listener = GoogleInputVoiceModule()   
        self.speaker = GoogleOutputVoiceModule()
        # GUI
        window = tk.Tk()
        window.title("CasaViva+")
        window.geometry('500x550+50+50')
        window.resizable(width=False, height=False)
        self.text = tk.Label(text ="CasaViva+",justify="center", font=("Lato", 70), fg='#000')
        self.text.pack()
        self.now = datetime.now()
        self.current_time = self.now.strftime("%D - %H:%M \n")
        self.ChatLog = tk.Text(window, bd=0, height="8", width="90", font="Lato", wrap="word")
        self.ChatLog.tag_config("right", justify="right")
        self.ChatLog.tag_config("left", justify="left")
        self.ChatLog.tag_config("small", font=("Lato", 10)) # CONFIG HORAS
        self.ChatLog.tag_config("colour", foreground="#333333") #CONFIG MENSAGENS BOT 
        self.ChatLog.tag_config("colourUser", foreground="#000000") #CONFIG MENSAGENS USER
        self.ChatLog.tag_config("colourBot", foreground="#11ee00") #CONFIG MENSAGENS USER
        self.ChatLog.tag_config("medium", font=("Lato", 16)) 
        scrollbar = tk.Scrollbar(window, command=self.ChatLog.yview, cursor="double_arrow")
        self.ChatLog['yscrollcommand'] = scrollbar.set
        scrollbar.place(x=460, y=85, height=450)
        self.ChatLog.place(x=40, y=80, height=460, width=420)

        threading.Thread(target=self.run).start()
        window.mainloop()
    def run(self):
        print( "Assistente a funcionar... \n")
        while True:
            bot_response = ""
            user_input = ""

            while user_input not in self.WAKE_UP:
                user_input = self.listener.listen()
            self.text["fg"] = "#11ee00"
            self.text["text"] = "CasaViva+  🎙️"
            self.ChatLog.config(state=tk.NORMAL)
            self.ChatLog.insert(tk.END, self.current_time, ("small","right","colour"))
            self.ChatLog.insert(tk.END, user_input + '\n\n',("right","colourUser","medium"))
            self.ChatLog.config(foreground="#000", font=("Lato", 16))
            print("D. Maria: " + user_input) 
            
            bot_response = self.interact(user_input)
            
            # GUI
            print("Assistente: " + bot_response)
            self.ChatLog.config(state=tk.NORMAL)
            self.ChatLog.insert(tk.END, self.current_time, ("small","colour"))
            self.ChatLog.insert(tk.END,textwrap.fill(bot_response, 30))
            self.ChatLog.insert(tk.END,'\n')
            self.ChatLog.config(foreground="#11ee00", font=("Lato", 16))
            self.ChatLog.config(state=tk.DISABLED)
            
            #speak
            self.speaker.say(bot_response)

            while user_input not in self.SLEEP:
                
                user_input = self.listener.listen()
                if user_input is None:
                    continue
               
                # GUI
                self.ChatLog.config(state=tk.NORMAL)
                self.ChatLog.config(foreground="#000", font=("Lato", 16))
                self.ChatLog.insert(tk.END, self.current_time, ("small","right","colour"))
                self.ChatLog.insert(tk.END, user_input.capitalize() + '\n\n',("right","colourUser","medium"))
                print("D. Maria: " + user_input) 

                bot_response = self.interact(user_input)
                
                #GUI
                self.ChatLog.config(state=tk.NORMAL)
                self.ChatLog.insert(tk.END, self.current_time, ("small","colour"))
                self.ChatLog.insert(tk.END,textwrap.fill(bot_response, 30))
                self.ChatLog.insert(tk.END,'\n')
                self.ChatLog.config(foreground="#11ee00", font=("Lato", 16))
                self.ChatLog.config(state=tk.DISABLED)
                print("Assistente: " + bot_response)

                self.speaker.say(bot_response)
                
                if bot_response in self.GOODBYE:
                    self.text["fg"] = "#000"
                    self.text["text"] = "CasaViva+"
                    break
    
    def interact(self, message):
        try:
            r = requests.post('http://localhost:5002/webhooks/rest/webhook', json={"message": message})
            for i in  r.json() :
                response = i['text']
            return response
        except:
            error = "Não entendi o que queria dizer. Pode repetir?"
            return error


Assistant()
