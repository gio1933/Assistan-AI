import pyttsx3
import datetime

engine = pyttsx3.init()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time_():
    Time = datetime.datetime.now().strftime("%I:%M:%S") # 12 Hour clock
    speak("La hora actual es")
    speak(Time)

def date_():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    speak("La fecha actual es")
    speak(str(day))   # Convertir a cadena
    speak(str(month)) # Convertir a cadena
    speak(str(year))  # Convertir a cadena

def wishme():
    speak("Bienvenido")

    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        speak("Buenos días")
    elif hour >= 12 and hour < 18:
        speak("Buenas tardes")
    elif hour >= 18 and hour < 24:
        speak("Buenas noches")
    else:
        speak("Buenas noches")

    time_()
    date_()

    speak("Estoy aquí para ayudarte con cualquier cosa que necesites. ¿En qué puedo ayudarte?")

wishme()