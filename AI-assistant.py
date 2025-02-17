import pyttsx3
import datetime

engine = pyttsx3.init()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time_():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak("La hora Actual es")
    speak(Time)

def date_():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    speak("La fecha actual es")
    speak(day)  
    speak(month)
    speak(year)

time_()
date_()