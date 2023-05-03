import pyaudio
from vosk import Model, KaldiRecognizer
import pyttsx3 as tts
from os import system
import platform
import json
import GLOBAL
from google.cloud import speech
from six.moves import queue
import sys
import re


class VoskInputVoiceModule:
    def __init__(self) -> None:
        # VOSK
        self.model = Model("vosk-model-small-pt-0.3")
        #self.model = Model("vosk-model-complete")   # este modelo é muito grande para colocar no git
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.recognizer.SetMaxAlternatives(1)
        self.mic = pyaudio.PyAudio()
        self.stream = self.mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        self.stream.start_stream()

    def listen(self):
        data = self.stream.read(4096, exception_on_overflow = False)
        if self.recognizer.AcceptWaveform(data):
            input = self.recognizer.FinalResult()
            input_json = json.loads(input)
            text = input_json['alternatives'][0]['text']
            text = text.lower()
            confidence = input_json['alternatives'][0]['confidence']
            if text != "<unk>" and len(text) > 1 :
                #debug
                if GLOBAL.DEBUG:
                    print("Listen: " + text + " --- " + str(confidence))
                return text
        return None
    
class GoogleInputVoiceModule():
    def __init__(self) -> None:
        language_code = "pt-PT"
        self.client = speech.SpeechClient()#.from_service_account_json("speechToTextKey.json")
        config = speech.RecognitionConfig( encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, sample_rate_hertz=16000, language_code=language_code)
        self.streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)

    def listen(self):
        with MicrophoneStream() as stream:
            audio_generator = stream.generator()
            requests = (speech.StreamingRecognizeRequest(audio_content=content) for content in audio_generator)
            responses = self.client.streaming_recognize(self.streaming_config, requests)
            
            input, confidence = stream.result(responses)
            #print("Listen: " + input)
            if confidence > 0.8:
                #print( input + " --- " + str(confidence))
                return input
            else: 
                #print("NÃO OUVI MUITO BEM: "+ input + " ---" + str(confidence))
                return None

class MicrophoneStream(object):
    def __init__(self):
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self.mic = pyaudio.PyAudio()
        self.stream = self.mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1600, stream_callback=self._fill_buffer,)
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self.stream.stop_stream()
        self.stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self.mic.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)

    def result(self, responses):
        num_chars_printed = 0
        for response in responses:
            if not response.results:
                continue
            result = response.results[0]
            if not result.alternatives:
                continue
            transcript = result.alternatives[0].transcript
            confidence = result.alternatives[0].confidence
            overwrite_chars = " " * (num_chars_printed - len(transcript))

            if not result.is_final:
                num_chars_printed = len(transcript)

            else:
                num_chars_printed = 0
                return str(transcript + overwrite_chars), confidence

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

