import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import google.generativeai as genai
import sys
import keys
import datetime

recognizer = sr.Recognizer()
engine = pyttsx3.init()

"""VOICE"""
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def say(text):
    engine.say(text)
    engine.runAndWait()


def aiProcess(command):

    genai.configure(api_key=keys.api_key_gemini)

    model = genai.GenerativeModel('gemini-1.5-flash')

    response = model.generate_content(command)
    return (response.text)


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://www.google.com/")
    elif "open instagram" in c.lower():
        webbrowser.open("https://www.instagram.com/")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://www.linkedin.com/in/siddhantghosh/")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com/")
    elif "open whatsapp" in c.lower():
        webbrowser.open("https://web.whatsapp.com")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={keys.newsapi}")

        if r.status_code == 200:

            data = r.json()

            articles = data.get('articles', [])


            for article in articles:
                say(article['title'])
    elif "weather" in c.lower():
        api_key = keys.weatherapi
        base_url = "https://api.openweathermap.org/data/2.5/weather?"
        city_name = "bangalore"  # Replace with the desired city
        complete_url = base_url + "appid=" + api_key + "&q=" + city_name
        response = requests.get(complete_url)
        data = response.json()
        try:
            y = data["main"]
            current_temperature = y["temp"]
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = data["weather"]
            weather_description = z[0]["description"]
            say(f"The weather in {city_name} is {weather_description}. The temperature is {round(current_temperature - 273.15)} degrees Celsius, with a pressure of {current_pressure} hPa and humidity of {current_humidity}%.")
        except KeyError:
            say("Sorry, I couldn't find weather information for that city.")
    elif "time" in c.lower():
        current_time = datetime.datetime.now()
        hour = current_time.hour
        minute = current_time.minute
        meridian = "AM" if hour < 12 else "PM"
        say(f"It is {hour}:{minute:02d} {meridian}")
    elif "date" in c.lower():
        today = datetime.datetime.now()
        day = today.day
        month = today.strftime("%B")
        year = today.year
        ordinal_suffix = "th"
        if day in [1, 21, 31]:
            ordinal_suffix = "st"
        elif day in [2, 22]:
            ordinal_suffix = "nd"
        elif day in [3, 23]:
            ordinal_suffix = "rd"
        say(f"Today is the {day}{ordinal_suffix} of {month}, {year}")
    elif "stop" in c.lower():
        a = sys.exit()

    else:

        output = aiProcess(c)
        say(output)


if __name__ == "__main__":
    say("Initializing Pluto. . ...")

    while True:


        r = sr.Recognizer()

        print("recognising...")


        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source)
            word = r.recognize_google(audio)
            # print(word)
            if (word.lower() == "pluto" or word.lower() == "pluto"):
                say("yes")
                # listen for my command
                with sr.Microphone() as source:
                    print("Pluto Active..")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)
                    command = r.recognize_google(audio)

        except sr.UnknownValueError:
            print("I'm sorry, I could not understand audio")
        except sr.RequestError as e:
            print("Pluto error; {0}".format(e))
        except sr.WaitTimeoutError as w:
            print(" ")
