Pluto is a Python-based virtual assistant that leverages speech recognition, text-to-speech, and Google Generative AI to perform various tasks.
It can:-

    Open websites: Navigate to popular websites like Google, Instagram, LinkedIn, YouTube, and WhatsApp.
    Provide information: Fetch and read news headlines, announce the current weather, time, and date.
    Interact with AI: Use Google Generative AI to generate responses to your questions and requests.

Requirements:-

    Python 3.x
    speech_recognition
    webbrowser
    pyttsx3
    requests
    google.generativeai
    sys
    datetime
    An API key for Google Generative AI and News API (stored in a separate keys.py file)

Additional Notes:-

    Ensure you have a working microphone for speech recognition.
    The script assumes the default system voice. You may need to install additional voices for customization.
    For better accuracy, consider training a custom speech recognition model.
    Replace "bangalore" in the weather code with your desired city.
