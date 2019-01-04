
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from speech2Text import SpeechToText
from text2speech import Text2Speach as t2s
from statemachine import StateMachine, State
import time
import _thread
import json
import random

class DialogManager(StateMachine):
    #states
    welcome = State('Welcome',initial = True)
    basicData = State('basicData')
    location = State('Location')
    solve = State('Solve')
    goodBye = State('Goodbye')
    #transitions
    transBasicData = welcome.to(basicData)
    transLocation = basicData.to(location)
    transSolve = location.to(solve)
    transGoodBye = solve.to(goodBye)
    
    

    #callbacks
    def on_enter_basicData(self):
        print(dm.current_state)
        speak(typeOfMessage='askHowAreYou')
        recognizer.getAudio()

    def on_enter_location(self):
        print(dm.current_state)
        speak(typeOfMessage='HasUndestood')
        
    def on_enter_solve(self):
        print(dm.current_state)
        speak(typeOfMessage='HasntUndestood')
        
    def on_enter_goodBye(self):
        print(dm.current_state)
        speak(typeOfMessage='GoodBye')

    

        
def dataInitialization():
        with open('server_questions.json') as f:
            return json.load(f)
        
dm = DialogManager()
data = dataInitialization()
recognizer = SpeechToText()
    

def speech_thread (recognizer):
    
    while recognizer.iterate == 1:        
        recognizer.getAudio()
        print("++++++++++++++++++++++")
            


def getAudioTosay(typeOfMessage):
    return data[typeOfMessage][random.randint(0,len(data[typeOfMessage])-1)]

def speak(typeOfMessage):
    t2s.speak(sentence=getAudioTosay(typeOfMessage=typeOfMessage),fileName=str(time.time())+typeOfMessage)
def main():
    
    
  
    
    recognizer.iterate = 0
    currentState = "noInitialized"
    speak(typeOfMessage='welcome')
    print("started")
    dm.transBasicData()
    ##_thread.start_new_thread(speech_thread,( recognizer,))
    
    
    
        
if __name__ == '__main__':
    import sys    
    main()
   
        
