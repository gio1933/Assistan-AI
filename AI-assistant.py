import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia

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

# wishme()

def TakeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Procesando...")
        query = r.recognize_google(audio, language='es-ES')
        print(query)

    except Exception as e:
        print(e)
        speak("Lo siento, no pude entender lo que dijiste. Por favor, repite lo que querias decirme")
        return "None"
    return query

# TakeCommand()

if __name__ == "__main__":

    wishme()

    while True:
        query = TakeCommand().lower()

        if 'time' in query:
            time_()
        
        elif 'date' in query:
            date_()

        elif 'wikipedia' in query:
            speak("Buscando en Wikipedia...")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query,sentences=3)
            speak("Según Wikipedia, " + result)