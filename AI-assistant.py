import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser as wb
import psutil
import pyjokes
import os

engine = pyttsx3.init()

engine.setProperty('rate', 190)
engine.setProperty('volume', 1)

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
    try:
        nombre_usuario = os.getlogin()
    except Exception:
        nombre_usuario = os.environ.get('USERNAME') or os.environ.get('USER')
    
    speak(f"Bienvenido {nombre_usuario}")

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

def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()

    server.login('user@gmail.com','password')
    server.sendmail('user@gmail.com', to, content)
    server.close()

def cpu():
    usage = str(psutil.cpu_percent())
    speak('La CPU está en'+usage)

def battery():
    battery = psutil.sensors_battery()
    percentage = battery.percent
    speak('La batería está en'+str(percentage)+'%')

def joke():
    speak(pyjokes.get_joke(language='es'))



if __name__ == "__main__":

    try:
        nombre_usuario = os.getlogin()
    except Exception:
        nombre_usuario = os.environ.get('USERNAME') or os.environ.get('USER')

    wishme()

    while True:
        query = TakeCommand().lower()

        if 'hora es' in query:
            time_()
        
        elif 'la fecha' in query:
            date_()

        elif 'buscar en wikipedia' in query:
            speak("Buscando en Wikipedia...")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query,sentences=3)
            speak("Según Wikipedia, " + result)
        
        elif 'enviar correo' in query:
            try:
                speak("¿Que debo escribir?")
                content = TakeCommand()

                # reciever = 'reciever_is_me@gmail.com'
                speak("¿Quién es el destinatario?")
                reciever = input("Ingresa el correo destinatario: ")
                to = reciever
                sendEmail(to,content)
                speak(content)
                speak("Correo enviado")

            except Exception as e:
                print(e)
                speak("Correo no enviado")

        elif 'buscar en youtube' in query:
            speak("¿Qué debo buscar?")
            search_Term = TakeCommand().lower()
            speak("Buscando en YouTube...")
            wb.open('https://www.youtube.com/results?search_query='+search_Term)

        elif 'buscar en google' in query:
            speak("¿Qué debo buscar?")
            search_Term = TakeCommand().lower()
            speak("Buscando en Google...")
            wb.open('https://www.google.com/search?q='+search_Term)

        elif 'la cpu' in query:
            cpu()
        
        elif 'la batería' in query:
            battery()

        elif 'cuéntame un chiste' in query:
            joke()

        elif 'adiós' in query:
            speak(f"hasta pronto {nombre_usuario}")
            quit()