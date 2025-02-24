import pyttsx3
import wikipedia
import smtplib
import os
import pyautogui
import psutil
import pyjokes
import time
import requests
import json
import wolframalpha

import webbrowser as wb
import speech_recognition as sr

from urllib.request import urlopen
from datetime import datetime, timedelta

wolframalpha_api = "R8X6Y4-9HY74X9AYL"

engine = pyttsx3.init()
engine.setProperty('rate', 210)
engine.setProperty('volume', 1)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def time_():
    Time = datetime.now().strftime("%I:%M:%S") # 12 Hour clock
    speak("La hora actual es")
    speak(Time)

def date_():
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
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

    hour = datetime.now().hour
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

def rest():
    speak("Descansando... Dime 'despierta' para volver a activarme.")
    
    while True:
        # Escuchar continuamente hasta que se reciba el comando de despertar
        command = TakeCommand().lower()
        
        if 'despierta' in command:
            speak("Me desperté")
            break  # Salir del bucle para continuar con el resto del código
        else:
            speak("Estoy en modo de descanso. Dime 'despierta' para volver.")
            time.sleep(1)  # Esperar un segundo antes de volver a escuchar

def get_weather(city_name):
    api_key = "13dc7b5fa5931e769c3cba13b5aee73d"  # Reemplaza con tu clave API
    base_url = "http://api.openweathermap.org/data/2.5/weather?q="
    
    # Construir la URL completa
    complete_url = f"{base_url}{city_name}&appid={api_key}&units=metric&lang=es"  # Usar 'metric' para obtener la temperatura en Celsius 'lang=es' para español

    # Hacer la solicitud a la API
    response = requests.get(complete_url)
    x = response.json()

    # Verificar si la ciudad fue encontrada
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        current_pressure = y["pressure"]
        current_humidity = y["humidity"]
        z = x["weather"]
        weather_description = z[0]["description"]

        # Imprimir y hablar los resultados
        weather_info = (
            f"Temperatura: {current_temperature}°C\n"
            f"Presión atmosférica: {current_pressure} hPa\n"
            f"Humedad: {current_humidity}%\n"
            f"Descripción: {weather_description.capitalize()}"
        )
        print(weather_info)
        speak(weather_info)  # Asegúrate de que la función speak esté definida
    else:
        speak("Ciudad no encontrada.")

def get_news():
    api_key = "8e3d9abfde7946e9b98ac95a75ef2768"  # Reemplaza con tu clave API
    # Obtener la fecha de ayer ya que no muestra las noticias del dia actual
    yesterday = datetime.now() - timedelta(days=1)
    today = yesterday.strftime('%D-%M-%Y')  # Formato de fecha YYYY-MM-DD
    url = f"https://newsapi.org/v2/everything?q=world&from={today}&to={today}&sortBy=publishedAt&language=es&apiKey={api_key}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(data)  # Imprimir la respuesta completa para depuración
            if data['status'] == 'ok' and data['totalResults'] > 0:
                speak("Aquí están las noticias del día:")
                print("Aquí están las noticias del día:")
                for article in data['articles']:
                    speak(article['title'])
                    print(article['title'])
            else:
                speak("No se pudieron obtener noticias.")
                print("No se pudieron obtener noticias.")
        else:
            speak(f"Error en la API: {response.status_code} - {response.text}")
            print(f"Error en la API: {response.status_code} - {response.text}")

    except Exception as e:
        speak("Ocurrió un error.")
        print("Ocurrió un error:", str(e))

def handle_location_query(query):
    if "dónde es" in query:
        query = query.replace("dónde es", "").strip()  # Eliminar la frase y espacios
        location = query
        speak("Localización solicitada")
        speak(location)
        wb.open("https://www.google.com/maps/place/" + location)




if __name__ == "__main__":

    clear = lambda: os.system('cls')

    clear()

    try:
        nombre_usuario = os.getlogin()
    except Exception:
        nombre_usuario = os.environ.get('USERNAME') or os.environ.get('USER')

    # wishme()

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

        elif 'adiós' in query or 'desconéctate' in query:
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

        elif 'descansa' in query or 've a descansar' in query:
            rest()

        elif "clima" in query:
            speak("Nombre de la ciudad:")
            print("Nombre de la ciudad:")
            city_name = TakeCommand()  # Asegúrate de que esta función esté definida
            get_weather(city_name)

        elif 'noticias' in query:
            get_news()

        elif "dónde es" in query:
            handle_location_query(query)

        elif 'calcula' in query:            
            client = wolframalpha.Client(wolframalpha_api)
            indx = query.lower().split().index('calcula')
            query = query.split()[indx + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            print("La respuesta es " + answer)
            speak("La respuesta es " + answer)

        # Se manejan en ingles las consultas y los resultados se devuelven en español 
        elif "what is" in query or "who is" in query: 
            client = wolframalpha.Client(wolframalpha_api)
            # Agregar el parámetro de idioma a la consulta
            query = f"{query} in Spanish"
            res = client.query(query)
            
            try:
                print (next(res.results).text)
                speak (next(res.results).text)
            except StopIteration:
                print ("No results") 
