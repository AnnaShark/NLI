
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

itsSuitableForPublic = True
phyisical = False

class DialogManager(StateMachine):
    #states
    welcome = State('Welcome',initial = True)
    basicData = State('BasicData')
    randomSolution = State('RandomSolution')
    randomSolutionSolving = State('RandomSolutionSolving')
    askingFor = State('AskingFor')
    askingForSecond = State('AskingForSecond')
    askingForSolving = State('AskingForolving')
    listenForSolution = State('ListenForSolution')
    listening = State('Listening')
    completed = State('Completed')
    end = State('End')
    #transitions
    transBasicData = welcome.to(basicData)
    
    transFromBasicDataToRandomSolution = basicData.to(randomSolution)
    transFromBasicDataToAskingFor = basicData.to(askingFor)
    transFromListenForSolution = basicData.to(listenForSolution)
    transFromBasicDataToBasicData = basicData.to(basicData)
    transFromBasicDataToEnd = basicData.to(end)

    transFromAskingForToAskingForSecond = askingFor.to(askingForSecond)
    transFromAskingForToAskingFor = askingFor.to(askingFor)
                            
    transFromAskingSecondToAskingForSecond = askingForSecond.to(askingForSecond)
    transFromAskingSecondToAskingForSolving = askingForSecond.to(askingForSolving)

    transFromAskingForSolvingToAskingForSolving = askingForSolving.to(askingForSolving)
    transFromAskingForSolvingToCompleted = askingForSolving.to(completed)
    
    transFromRandomSolutionToRandomSolution = randomSolution.to(randomSolution)
    transFromRandomSolutionToBasicData = randomSolution.to(basicData)
    transFromRandomSolutionToRandomSolutionSolving = randomSolution.to(randomSolutionSolving)

    transFromRandomSolutionSolvingToRandomSolutionSolving = randomSolutionSolving.to(randomSolutionSolving)
    transFromRandomSolutionSolvingToCompleted = randomSolutionSolving.to(completed)
    
    transFromListenSolutionToListenSolution = listenForSolution.to(listenForSolution)
    transFromLitenSolutionToBasicData = listenForSolution.to(basicData)
    transFromListenSolutionToListening = listenForSolution.to(listening)

    transFromListeningToListening = listening.to(listening)
    transFromListeningToCompleted = listening.to(completed)

    transFromCompletedToEnd = completed.to(end)
    transFromCompletedToCompleted = completed.to(completed)
    transFromCompletedToBasicData = completed.to(basicData)

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

    def on_enter_completed(self):
        speak(typeOfMessage = 'completed')

    def on_enter_askingFor(self):
        speak(typeOfMessage = 'askingFor')

    def on_enter_askingForSecond(self):
        speak(typeOfMessage = 'askingForSecond')

    def on_enter_askingForSolving(self):
        speak(typeOfMessage = 'askingForSolving')
        onto_searched = onto.search(techniqueName ="*")            
        for i in range(len(onto_searched)):
           
            if onto_searched[i].physicalActivityInvolved[0] == (phyisical) and onto_searched[i].suitableForPublicEnv[0] == (itsSuitableForPublic) :
                print(onto_searched[i].physicalActivityInvolved[0] == (phyisical), onto_searched[i].suitableForPublicEnv[0] == (itsSuitableForPublic))
                speakResult(onto_searched[i].techniqueName[0],onto_searched[i].techniqueName[0])
        speakResult("   Was it helpful?", "helpful")
            
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
            solution = 0
            
            while solution == 0:             
                basicDataDoc = recognizer.getAudio()
                print(basicDataDoc)
                for token in basicDataDoc:
                   # print(token.text, token.pos_, token.dep_)
                    if token.text == "random" and token.dep_ == "amod":
                        print("he wants to make a random solution")
                        solution =1
                                
                    elif token.text == "ask" or token.text == "asked":
                        print ( "he wants to be asked")
                        solution = 2
                                
                    elif token.text == "repeat":
                        print( "he wants to repeat the sentence")
                        solution = -1
                                
                    elif( token.text == "tell"):
                        print("tells a technique")
                        solution = 3
                    elif( token.text == "finish" or token.text == "done"):
                        print("exit")
                        solution = 4
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
            elif solution == 4:
                dm.transFromBasicDataToEnd()
                
        if dm.current_state == dm.randomSolution:
            random_agree = 0
            while random_agree == 0:
                listened = recognizer.getAudio()
                for token in listened:
                    #print(token.text, token.pos_, token.dep_)
                    if token.text == "yes":
                        print("AGREE, SAID A RANDOM SOLUTION")
                        random_agree =1
                           
                    elif token.text == "no":
                        print ( "DISAGREE, WASNT A RANDOM SOLUTION")
                        random_agree = 2
                                
                    elif token.text == "repeat":
                        print( "REPEAT, REPEAT THE SENTENCE")
                        random_agree = -1
                if random_agree == 0  :
                    print( "THE AGENT HASN'T UNDESTOOD")
                    speak(typeOfMessage='HasntUndestood')
                
            if   random_agree == 1:
                speak(typeOfMessage='HasUndestood')
                dm.transFromRandomSolutionToRandomSolutionSolving()              
            elif random_agree == 2:
                dm.transFromRandomSolutionToBasicData()
            elif random_agree == -1:
                dm.transFromRandomSolutionToRandomSolution()
                
        if dm.current_state == dm.randomSolutionSolving :             
                random_finished = 0
                while random_finished == 0:
                    listened = recognizer.getAudio()
                    for token in listened:
                        #print(token.text, token.pos_, token.dep_)
                        if token.text == "yes":
                            print("USER SAID IT WAS HELPFUL")
                            random_finished =1                
                                    
                        elif token.text == "no":
                            print ( "USER SAID IT WASNT HELPFUL")
                            random_finished = 2                  
                                    
                        elif token.text == "another":
                            print( "USER WANTS TO TRY ANOTHER RANDOM SOLUTION")
                            random_finished = -1
                            
                    if random_finished == 0  :
                        print( "DIDN'T UNDESTOOD")
                        speak(typeOfMessage='HasntUndestood')
                if random_finished == 1  :
                    dm.transFromRandomSolutionSolvingToCompleted()
                if random_finished == 2  :
                    dm.transFromRandomSolutionSolvingToCompleted()
                if random_finished == -1  :
                    dm.transFromRandomSolutionSolvingToRandomSolutionSolving()
                    
        if dm.current_state == dm.completed:
                can_leave = 0
                while can_leave == 0:
                    listened = recognizer.getAudio()
                    for token in listened:
                        #print(token.text, token.pos_, token.dep_)
                        if token.text == "yes":
                            print("USER SAID WE CAN DO OTHER THINGS")
                            can_leave =1                            
                                    
                        elif token.text == "no":
                            print ( "USER SAID WE CAN LEAVE")
                            can_leave = 2                           
                                    
                        elif token.text == "repeat":
                            print( "USER WANTS TO REPEAT THAT SENTENCE")
                            can_leave = -1
                            
                    if can_leave == 0  :
                        print( "DIDN'T UNDESTOOD")
                        speak(typeOfMessage='HasntUndestood')
                if can_leave == 1  :                    
                    dm.transFromCompletedToBasicData()
                if can_leave == 2  :
                    dm.transFromCompletedToEnd()
                if can_leave == -1 :
                    dm.transFromCompletedToCompleted()
                    
        if dm.current_state == dm.listenForSolution:
            listen_agree = 0
            while listen_agree == 0:
                listened = recognizer.getAudio()
                for token in listened:
                    #print(token.text, token.pos_, token.dep_)
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
                print(str(listened).lower())
                onto_searched = onto.search(techniqueName = str(listened).lower())
                print(onto_searched)
                for i in range(len(onto_searched)):
                    print(onto_searched[0].techniqueName[0].lower())
                    speakResult(onto_searched[0].techniqueName[0],onto_searched[0].techniqueName[0])
                    speakResult(onto_searched[0].techniqueScript[0],onto_searched[0].techniqueName[0]+"description")
                    proposal_told = 1
                    
                if len(listened) > 0:
                    print(listened)
                if proposal_told == 0  :
                    print( "LISTEN_DIDN'T UNDESTOOD")
                    speak(typeOfMessage='HasntUndestood')
                    
            if   proposal_told == 1:
                dm.transFromListeningToCompleted()
            elif proposal_told == 2:
                dm.transFromLitenSolutionToBasicData()
            elif proposal_told == -1:
                dm.transFromListenSolutionToListenSolution()
        if dm.current_state == dm.askingFor:           
            solution = 0
            while solution == 0:             
                listened = recognizer.getAudio()
                print(listened)
                for token in listened:
                   # print(token.text, token.pos_, token.dep_)
                    if token.text == "yes":
                        print("USER WANTS A PUBLIC SUITABLE SOLUTION")
                        solution =1
                                
                    elif token.text == "no":
                        print ( "USER WANTS A PRIVATE SOLUTION")
                        solution = -1
                                
                    elif token.text == "repeat":
                        print( "he wants to repeat the sentence")
                        solution = -2                                
                    
                if solution == 0  :
                    print( "didn't got anything")
                    speak(typeOfMessage='HasntUndestood')                         
                       
            if   solution == 1:
                dm.transFromAskingForToAskingForSecond()
                itsSuitableForPublic = True
            elif solution == -1:
                dm.transFromAskingForToAskingForSecond()
                itsSuitableForPublic = False
            elif solution == -2:
                dm.transFromAskingForToAskingFor()
        if dm.current_state == dm.askingForSecond:
            solution = 0
            while solution == 0:             
                listened = recognizer.getAudio()
                print(listened)
                for token in listened:
                   # print(token.text, token.pos_, token.dep_)
                    if token.text == "yes":
                        print("USER WANTS A PHYSICAL SOLUTION")
                        solution =1
                                
                    elif token.text == "no":
                        print ( "USER WANTS A STATIC SOLUTION")
                        solution = -1
                                
                    elif token.text == "repeat":
                        print( "he wants to repeat the sentence")
                        solution = -2                                
                    
                if solution == 0  :
                    print( "didn't got anything")
                    speak(typeOfMessage='HasntUndestood')                         
                       
            if   solution == 1:
                dm.transFromAskingSecondToAskingForSolving()
                phyisical = True
            elif solution == -1:
                dm.transFromAskingSecondToAskingForSolving()
                phyisical = False
            elif solution == -2:
                dm.transFromAskingForToAskingFor()

        if dm.current_state == dm.askingForSolving:
            solution = 0
            while solution == 0:             
                listened = recognizer.getAudio()
                print(listened)
                for token in listened:
                   # print(token.text, token.pos_, token.dep_)
                    if token.text == "yes":
                        print("WAS USEFUL")
                        solution =1
                                
                    elif token.text == "no":
                        print ( "WASNT USEFUL")
                        solution = -1
                                
                    elif token.text == "repeat":
                        print( "he wants to repeat the sentence")
                        solution = -2                                
                    
                if solution == 0  :
                    print( "didn't got anything")
                    speak(typeOfMessage='HasntUndestood')                         
                       
            if   solution == 1:
                dm.transFromAskingForSolvingToCompleted()
            elif solution == -1:
                dm.transFromAskingForSolvingToCompleted()
            elif solution == -2:
                dm.transFromAskingForSolvingToCompleted()
            
    speak(typeOfMessage = "GoodBye")
    
    
        
if __name__ == '__main__':
    import sys    
    main()
   
        
