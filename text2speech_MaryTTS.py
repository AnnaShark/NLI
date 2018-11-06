import wave
from io import StringIO
from marytts import MaryTTS


class Text2SpeechMaryTTS():
    
    
    def __init__(self, parent=None):
        self.marytts  = MaryTTS()
        self.wavs =self.marytts.synth_wav('Hello World!')
        self.wav = wave.open(StringIO.StringIO(wavs))
        print (wav.getnchannels(), wav.getframerate(), wav.getnframes())

    
tts =    Text2SpeechMaryTTS()

    

        
