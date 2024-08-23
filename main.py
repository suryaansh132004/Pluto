import speech_recognition as sr  # Library for recognizing speech
import webbrowser  # Library for opening webpages
import pyttsx3  # Library for text-to-speech
import requests  # Library for making HTTP requests (e.g., for news and weather)
import google.generativeai as genai  # Library for interacting with Google Generative AI
import sys  # Library for system-related functions (e.g., exiting the program)
import keys  # A separate file likely containing API keys (not shown here for security)
import datetime  # Library for working with dates and times

# Initialize recognizer for speech input
recognizer = sr.Recognizer()

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Set the default voice for text-to-speech (optional)
"""VOICE"""
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def say(text):
  """
  This function takes text as input and speaks it aloud using the text-to-speech engine.
  """
  engine.say(text)
  engine.runAndWait()


def aiProcess(command):
  """
  This function processes a user command using Google Generative AI.
  It retrieves the API key from the 'keys' module and uses the 'gemini-1.5-flash' model
  to generate a response based on the command.
  """
  genai.configure(api_key=keys.api_key_gemini)
  model = genai.GenerativeModel('gemini-1.5-flash')
  response = model.generate_content(command)
  return response.text


def processCommand(command):
  """
  This function takes a user command as input and performs actions based on the command.
  - Opens websites like Google, Instagram, etc.
  - Fetches and reads news headlines.
  - Retrieves and announces weather information for a specific city.
  - Tells the current time.
  - Announces the current date.
  - Exits the program if "stop" is said.
  - For other commands, it uses the aiProcess function to generate a response using Google Generative AI.
  """
  if "open google" in command.lower():
    webbrowser.open("https://www.google.com/")
  elif "open instagram" in command.lower():
    webbrowser.open("https://www.instagram.com/")
  # ... similar logic for other website opening commands ...
  elif "news" in command.lower():
    # Get news headlines using News API
    r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={keys.newsapi}")
    if r.status_code == 200:
      data = r.json()
      articles = data.get('articles', [])
      for article in articles:
        say(article['title'])
  elif "weather" in command.lower():
    # Get weather information for a specific city (replace "bangalore" with your desired city)
    api_key = keys.weatherapi
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    city_name = "bangalore"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    data = response.json()
    try:
      # Extract weather data
      current_temperature = round(data["main"]["temp"] - 273.15)  # Convert Kelvin to Celsius
      current_pressure = data["main"]["pressure"]
      current_humidity = data["main"]["humidity"]
      weather_description = data["weather"][0]["description"]
      say(f"The weather in {city_name} is {weather_description}. The temperature is {current_temperature} degrees Celsius, with a pressure of {current_pressure} hPa and humidity of {current_humidity}%.")
    except KeyError:
      say("Sorry, I couldn't find weather information for that city.")
  elif "time" in command.lower():
    # Get current time
    current_time = datetime.datetime.now()
    hour = current_time.hour
    minute = current_time.minute
    meridian = "AM" if hour < 12 else "PM"
    say(f"It is {hour}:{minute:02d} {meridian}")
  elif "date" in command.lower():
    # Get current date
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
  elif "stop" in command.lower():
    # Exit the program
    sys.exit()

  else:
    # Process the command using Google Generative AI
    output = aiProcess(command)
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
