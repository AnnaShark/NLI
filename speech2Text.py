
import speech_recognition as sr 
import spacy
from gtts import gTTS
from pygame import mixer
class SpeechToText():
    
    
    def __init__(self, parent=None):
        self.iterate = 0
        self.canProcess = 0
        self.r = sr.Recognizer()
        self.r.pause_threshold = 0.8
        self.nlp = spacy.load('en_core_web_sm')

    
    def speech2Txt(self):
    
        try:
            print("Google Speech Recognition thinks you said " + self.r.recognize_google(self.audio))
            canProcess = 1
            doc = self.nlp(self.r.recognize_google(self.audio))
            return doc
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return {}
        except sr.RequestError as e:
            return {}
            
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

   
    def getAudio(self):
        with sr.Microphone() as source:
            print("Say something!")
            self.audio = self.r.listen(source)
            print("listening...")
        return self.speech2Txt()


    

        
