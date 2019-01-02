from gtts import gTTS
from pygame import mixer

class Text2Speach():
    def speak(sentence):
        tts = gTTS(text=sentence, lang='en')
        tts.save("test.mp3")

        mixer.init()
        mixer.music.load("test.mp3")
        mixer.music.play()
        while mixer.music.get_busy() == True:
            continue
        
    def __init__(self, parent=None):
        print("Text 2 Speach initialied.")
        

    

    
