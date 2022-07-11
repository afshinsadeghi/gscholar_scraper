#pip install pyttsx3 , if not have the text to speach lib
import pyttsx3


#engine = pyttsx3.init()
engine = pyttsx3.init('nsss')
voices = engine.getProperty('voices')

engine.setProperty('voice', 'com.apple.speech.synthesis.voice.samantha')#samantha
#engine.setProperty('voices', voices[1].id)
rate = engine.getProperty('rate')
engine.setProperty('rate', 170)


def speak(audio):
    print(audio)
    engine.say(audio)
    engine.runAndWait()


speak("Next meeting is in 10 minutes, lets prepare")
