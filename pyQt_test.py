
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from speech2Text import SpeechToText
import _thread



class VisualSelector( QDialog):    
    def __init__(self, parent=None):
        super(VisualSelector, self).__init__(parent)
        self.speechStarted = 0
        
        self.draw_radio_buttons_selectParser()
        self.drawRadioButtons()
        self.drawSpeechButton()
        
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.speech_2_text_selector)
        mainLayout.addWidget(self.text2SpeechSelector)
        mainLayout.addWidget(self.speechManager)
         
        self.setLayout(mainLayout)
        self.setWindowTitle("SPEECH ")
    def activate_speech(self):
        if self.speechStarted == 1:
            self.speechStarted = 0
            print(self.speechStarted)
            
        else:
            self.speechStarted = 1
            print(self.speechStarted)
             
    def drawSpeechButton(self):
        self.speechManager = QGroupBox();
        activateButton = QPushButton('START')
        activateButton.clicked.connect(self.activate_speech)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("initiate or end the speech recognition"))
        layout.addWidget(activateButton)
        layout.addWidget(QPushButton('END'))
        self.speechManager.setLayout(layout)

    def draw_radio_buttons_selectParser(self):
        self.speech_2_text_selector = QGroupBox("Select speech Synthetizer")
        radioButton_mary = QRadioButton("MaryTTS")
        radioButton_google = QRadioButton("Google API")
        radioButton_Festival = QRadioButton("Festival")
        radioButton_google.setChecked(True)
        layout = QVBoxLayout()
        layout.addWidget(radioButton_mary)        
        layout.addWidget(radioButton_google)
        layout.addWidget(radioButton_Festival)
        layout.addStretch(1)
        self.speech_2_text_selector.setLayout(layout)
        
    def drawRadioButtons(self):
        self.text2SpeechSelector = QGroupBox("Select speech Synthetizer")
        pic = QLabel(self)
        pic.setPixmap(QPixmap("icon.jpg"))
        radioButton1 = QRadioButton("Speech Synth. 1")
        radioButton2 = QRadioButton("Speech Synth. 2")
        radioButton3 = QRadioButton("Speech Synth. 3")
        radioButton1.setChecked(True)        

        layout = QVBoxLayout()
        layout.addWidget(pic)
        layout.addWidget(radioButton1)
        layout.addWidget(radioButton2)
        layout.addWidget(radioButton3)
        layout.addStretch(1)
        self.text2SpeechSelector.setLayout(layout)

def speech_thread (recognizer,view):
    while recognizer.iterate == 1:
        if view.speechStarted == 1:
            print("is iterating: ", recognizer.iterate)
            recognizer.getAudio()
            print("++++++++++++++++++++++")
def main():
    QApplication.setStyle(QStyleFactory.create("Fusion"))
    app = QApplication(sys.argv)
    view = VisualSelector()
    recognizer = SpeechToText()
    recognizer.iterate = 1
    print("started")
    view.show()
    _thread.start_new_thread(speech_thread,( recognizer, view,))
    sys.exit(app.exec_())
    
    
        
if __name__ == '__main__':
    import sys
    main()
   
        
