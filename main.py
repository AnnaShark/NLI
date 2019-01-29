
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from SPARQLWrapper import SPARQLWrapper,JSON
import rdflib
from owlready2 import *

from speech2Text import SpeechToText
from text2speech import Text2Speach as t2s
from statemachine import StateMachine, State
from random import *
import time
import _thread
import json
import random



class DialogManager(StateMachine):
    #states
    welcome = State('Welcome',initial = True)
    basicData = State('BasicData')
    randomSolution = State('RandomSolution')
    randomSolutionSolving = State('RandomSolutionSolving')
    askingFor = State('AskingFor')
    listenForSolution = State('ListenForSolution')
    listening = State('Listening')
    end = State('End')
    #transitions
    transBasicData = welcome.to(basicData)
    
    transFromBasicDataToRandomSolution = basicData.to(randomSolution)
    transFromBasicDataToAskingFor = basicData.to(askingFor)
    transFromListenForSolution = basicData.to(listenForSolution)
    transFromBasicDataToBasicData = basicData.to(basicData)
    
    transFromRandomSolutionToRandomSolution = randomSolution.to(randomSolution)
    transFromRandomSolutionToBasicData = randomSolution.to(basicData)
    transFromRandomSolutionToRandomSolutionSolving = randomSolution.to(randomSolutionSolving)

    transFromRandomSolutionSolvingToRandomSolutionSolving = randomSolutionSolving.to(randomSolutionSolving)
    transFromRandomSolutionSolvingToEnd = randomSolutionSolving.to(end)
    
    transFromListenSolutionToListenSolution = listenForSolution.to(listenForSolution)
    transFromLitenSolutionToBasicData = listenForSolution.to(basicData)
    transFromListenSolutionToListening = listenForSolution.to(listening)

    transFromListeningToListening = listening.to(listening)
    transFromListeningToEnd = listening.to(end)

    def on_enter_basicData(self):
        speak(typeOfMessage='askHowAreYou') 
    def on_enter_randomSolution(self):        
        speak(typeOfMessage='randomSolutionCheck')

    def on_enter_randomSolutionSolving(self):
        onto_searched = onto.search(techniqueName = "*")
        randomSolution = randint(0,len(onto_searched))
        print(randomSolution)
        randomSolutionFound =onto_searched[randomSolution] 
        print(randomSolutionFound.techniqueName)
                
        speakResult(randomSolutionFound.techniqueName[0],randomSolutionFound.techniqueName[0])
        speakResult(randomSolutionFound.techniqueScript[0],randomSolutionFound.techniqueName[0]+"description")

        speakResult("Was it helpful?", "helpful")
        
    def on_enter_listenForSolution(self):
        speak(typeOfMessage ='listenForProposalCheck')

    def on_enter_listening(self):
        speak(typeOfMessage = 'listening')
            
def dataInitialization():
        with open('server_questions.json') as f:
            return json.load(f)
        
dm = DialogManager()
data = dataInitialization()
recognizer = SpeechToText()
onto = get_ontology("resources/root-ontology.owl").load()

def speech_thread (recognizer):    
    while recognizer.iterate == 1:        
        recognizer.getAudio()
        print("++++++++++++++++++++++")        


def getAudioTosay(typeOfMessage):
    return data[typeOfMessage][random.randint(0,len(data[typeOfMessage])-1)]

def speak(typeOfMessage):
    t2s.speak(sentence=getAudioTosay(typeOfMessage=typeOfMessage),fileName=str(time.time())+typeOfMessage)

def speakResult(msg,name):
    t2s.speak(msg,name)

    
def main():     
    recognizer.iterate = 0
    currentState = "noInitialized"
    speak(typeOfMessage='welcome')
    dm.transBasicData()
    print(dm.current_state)
    ##_thread.start_new_thread(speech_thread,( recognizer,))
    while dm.current_state != dm.end:
        if dm.current_state == dm.basicData :
            print(dm.current_state)
            print(dm.is_basicData)
            print(dm.is_welcome)
            solution = 0
            
            while solution == 0:             
                basicDataDoc = recognizer.getAudio()
                print(basicDataDoc)
                for token in basicDataDoc:
                    print(token.text, token.pos_, token.dep_)
                    if token.text == "random" and token.dep_ == "amod":
                        print("he wants to make a random solution")
                        solution =1
                                
                    elif token.text == "ask":
                        print ( "he wants to be asked")
                        solution = 2
                                
                    elif token.text == "repeat":
                        print( "he wants to repeat the sentence")
                        solution = -1
                                
                    elif( token.text == "tell"):
                        print("tells a technique")
                        solution = 3
                if solution == 0  :
                    print( "didn't got anything")
                    speak(typeOfMessage='HasntUndestood')                         
                       
            if   solution == 1:
                dm.transFromBasicDataToRandomSolution()
            elif solution == 2:
                dm.transFromBasicDataToAskingFor()
            elif solution == 3:
                dm.transFromListenForSolution()
            elif solution == -1:
                dm.transFromBasicDataToBasicData()
                
        if dm.current_state == dm.randomSolution:
            random_agree = 0
            while random_agree == 0:
                listened = recognizer.getAudio()
                for token in listened:
                    print(token.text, token.pos_, token.dep_)
                    if token.text == "yes":
                        print("AGREE")
                        random_agree =1
                                
                    elif token.text == "no":
                        print ( "DISAGREE")
                        random_agree = 2
                                
                    elif token.text == "repeat":
                        print( "REPEAT")
                        random_agree = -1
                if random_agree == 0  :
                    print( "DIDN'T UNDESTOOD")
                    speak(typeOfMessage='HasntUndestood')
            if   random_agree == 1:
                speak(typeOfMessage='HasUndestood')
                
                dm.transFromRandomSolutionToRandomSolutionSolving()
                random_finished = 0
                while random_finished == 0:
                    listened = recognizer.getAudio()
                    for token in listened:
                        print(token.text, token.pos_, token.dep_)
                        if token.text == "yes":
                            print("AGREE")
                            random_finished =1
                            dm.transFromRandomSolutionSolvingToEnd()
                                    
                        elif token.text == "no":
                            print ( "DISAGREE")
                            random_finished = 2
                                    
                        elif token.text == "another":
                            print( "TRY ANOTHER")
                            random_finished = -1
                            dm.transFromRandomSolutionSolvingToRandomSolutionSolving()
                            
                    if random_finished == 0  :
                        print( "DIDN'T UNDESTOOD")
                        speak(typeOfMessage='HasntUndestood')
                            
            if random_agree == 0  :
                print( "DIDN'T UNDESTOOD")
                speak(typeOfMessage='HasntUndestood')
            elif random_agree == 2:
                dm.transFromRandomSolutionToBasicData()
            elif random_agree == -1:
                dm.transFromRandomSolutionToRandomSolution()
                
        if dm.current_state == dm.listenForSolution:
            listen_agree = 0
            while listen_agree == 0:
                listened = recognizer.getAudio()
                for token in listened:
                    print(token.text, token.pos_, token.dep_)
                    if token.text == "yes":
                        print("LISTEN_AGREE")
                        listen_agree =1
                                
                    elif token.text == "no":
                        print ( "LISTEN_DISAGREE")
                        listen_agree = 2
                                
                    elif token.text == "repeat":
                        print( "LISTEN_REPEAT")
                        listen_agree = -1
                if listen_agree == 0  :
                    print( "LISTEN_DIDN'T UNDESTOOD")
                    speak(typeOfMessage='HasntUndestood')
            if   listen_agree == 1:
                dm.transFromListenSolutionToListening()
            elif listen_agree == 2:
                dm.transFromLitenSolutionToBasicData()
            elif listen_agree == -1:
                dm.transFromListenSolutionToListenSolution()
        if dm.current_state == dm.listening:
            proposal_told = 0
            while proposal_told == 0:
                listened = recognizer.getAudio()
                print(listened)
                onto_searched = onto.search(techniqueName = "*")
                print(onto_searched)
                for i in range(len(onto_searched)):
                    print(onto_searched[i].techniqueName[0].lower())
                    if onto_searched[i].techniqueName[0].lower() == listened:                  
                        speakResult(onto_searched[i].techniqueName[0],onto_searched[i].techniqueName[0])
                        speakResult(onto_searched[i].techniqueScript[0],onto_searched[i].techniqueName[0]+"description")
                        proposal_told = 1
                        break;
                    
                if len(listened) > 0:
                    print(listened)
                if listen_agree == 0  :
                    print( "LISTEN_DIDN'T UNDESTOOD")
                    speak(typeOfMessage='HasntUndestood')
                    
            if   proposal_told == 1:
                dm.transFromListeningToEnd()
            elif proposal_told == 2:
                dm.transFromLitenSolutionToBasicData()
            elif proposal_told == -1:
                dm.transFromListenSolutionToListenSolution()
            
    speak(typeOfMessage = "GoodBye")
    
    
        
if __name__ == '__main__':
    import sys    
    main()
   
        
