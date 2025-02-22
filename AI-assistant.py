import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import smtplib
import webbrowser as wb
import os
import pyautogui
import psutil
import pyjokes


engine = pyttsx3.init()
engine.setProperty('rate', 210)
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

def write_note_with_date(notes):
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    with open('notes.txt', 'a') as file:  # Usar 'a' para agregar al final del archivo
        file.write(f"{strTime} :- {notes}\n")

def write_note_without_date(notes):
    with open('notes.txt', 'a') as file:  # Usar 'a' para agregar al final del archivo
        file.write(f"{notes}\n")

def read_notes():
    with open('notes.txt', 'r') as file:
        return file.read()

def handle_write_note():
    speak("¿Qué debo escribir?")
    notes = TakeCommand()
    speak(f"{nombre_usuario}, ¿Quieres que incluya la fecha?")
    ans = TakeCommand()

    if 'sí' in ans or 'claro' in ans or 'por supuesto' in ans or 'incluye la fecha' in ans:
        write_note_with_date(notes)
    elif 'no' in ans or 'no incluyas la fecha' in ans:
        write_note_without_date(notes)

    speak('Termine de anotar lo solicitado.')
    speak("¿Quieres que abra la nota?")
    ans = TakeCommand()
    if 'sí' in ans or 'claro' in ans or 'por supuesto' in ans:
        notes_content = read_notes()
        print(notes_content)
        speak(notes_content)
    elif 'guarda la nota' in ans:
        speak('La nota ha sido guardada')

def handle_show_note():
    speak("¿Quieres que te la lea o la muestre en pantalla?")
    ans = TakeCommand()
    notes_content = read_notes()

    if 'leerme la nota' in ans or 'lee la nota' in ans or 'leeme la nota' in ans:
        speak(notes_content)
    elif 'mostrarme la nota' in ans or 'muéstrame la nota' in ans:
        print(notes_content)
    else:
        print(notes_content)

def screenshot():
    try:
        img = pyautogui.screenshot()
        img.save('C:/Users/Giovanni/Pictures/screenshot.png')  # Asegúrate de que esta ruta sea válida
        speak("Captura de pantalla guardada.")
    except Exception as e:
        speak("Ocurrió un error al tomar la captura.")
        print(e)

if __name__ == "__main__":

    clear = lambda: os.system('cls')

    clear()

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

        elif 'abrir word' in query:
            speak("Abriendo Microsoft Word...")
            os.startfile("C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD")

        elif 'escribe una nota' in query:
            handle_write_note()

        elif 'muéstrame la nota' in query:
            handle_show_note()

        elif 'tomar captura' in query:
            speak("Tomando captura...")
            screenshot()

        elif 'recordar' in query:
            speak("¿Qué debo recordar?")
            memory = TakeCommand()
            speak("Me pediste que recordara" + memory)
            remember = open('memory.txt','w')
            remember.write(memory)
            remember.close()

        elif 'recuerdas algo' in query:
            remember =open('memory.txt', 'r')
            speak("Me pediste que recordara" + remember.read())

        elif 'cerrar sesión' in query:
            speak("Cerrando sesión...")
            os.system("shutdown -l")

        elif 'reiniciar' in query:
            speak("Reiniciando...")
            os.system("shutdown /r /t 1")

        elif 'apaga' in query or 'apagar' in query:
            speak("Apagando...")
            os.system("shutdown /s /t 1")