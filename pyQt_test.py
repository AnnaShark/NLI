
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from speech2Text import SpeechToText
from text2speech import Text2Speach as t2s
import _thread
import json
import random

class VisualSelector( QDialog):    
    def __init__(self, parent=None):
        super(VisualSelector, self).__init__(parent)
        self.speechStarted = 0
        self.drawSpeechButton()
        
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.speechManager)
         
        self.setLayout(mainLayout)
        self.setWindowTitle("SPEECH ")
    def activate_speech(self):        
        self.speechStarted = 1
        print(self.speechStarted)
    def deActivate_speech(self):        
        self.speechStarted = 0
        print(self.speechStarted)
             
    def drawSpeechButton(self):
        self.speechManager = QGroupBox();
        activateButton = QPushButton('START')
        activateButton.clicked.connect(self.activate_speech)
        deActivateButton = QPushButton('END')
        deActivateButton.clicked.connect(self.deActivate_speech)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("initiate or end the speech recognition"))
        layout.addWidget(activateButton)
        layout.addWidget(deActivateButton)
        self.speechManager.setLayout(layout)

    

def speech_thread (recognizer,view):
    
    while recognizer.iterate == 1:
        if view.speechStarted == 1:
            print("is iterating: ", recognizer.iterate)
            recognizer.getAudio()
            print("++++++++++++++++++++++")
        else:
            print("stopped")
            
def dataInitialization():
        with open('server_questions.json') as f:
            return json.load(f)

def getAudioTosay(data,typeOfMessage):
    return data[typeOfMessage][random.randint(0,len(data[typeOfMessage])-1)]
                               
def main():
    data = dataInitialization()
    dataInitialization()
    QApplication.setStyle(QStyleFactory.create("Fusion"))
    app = QApplication(sys.argv)
    view = VisualSelector()
    recognizer = SpeechToText()
    recognizer.iterate = 1
    currentState = "noInitialized"
    
    view.show()    
    t2s.speak(getAudioTosay(data,typeOfMessage='welcome'))
    print("started")
    _thread.start_new_thread(speech_thread,( recognizer, view,))
    sys.exit(app.exec_())
    
    
        
if __name__ == '__main__':
    import sys    
    main()
   
        
