import pyaudio
from vosk import Model, KaldiRecognizer
import pyttsx3 as tts
from os import system
import platform

class InputVoiceModule:
    def __init__(self) -> None:
        self.model = Model("vosk-model-small-pt-0.3")
        #self.model = Model("vosk-model-complete")   # este modelo é muito grande para colocar no git
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.mic = pyaudio.PyAudio()
        self.stream = self.mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        self.stream.start_stream()

    def listen(self):
        data = self.stream.read(4096, exception_on_overflow = False)
        if self.recognizer.AcceptWaveform(data):
            text = self.recognizer.Result()
            text = text[14:-3]
            text = text.lower()
            if text != "<unk>":
                #debug
                #print(text)
                return text
        return None
    
 
class OutputVoiceModule:   
    def __init__(self) -> None:
       
        if platform.system() == 'Windows':  # windows
            self.speaker = tts.init()
            self.speaker.setProperty('rate', 150)
            #TODO definir a voz para windows
            # self.speaker.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_ptPT_Helia")
        
        else: #MAC
            self.speaker = None

    def say(self, message):
        if self.speaker != None:
            self.speaker.say("Olá Dona Maria")
            self.speaker.runAndWait()
        else:
            system("say " + str(message))

