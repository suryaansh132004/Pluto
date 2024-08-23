import keys
import google.generativeai as genai

genai.configure(api_key=keys.api_key_gemini)
model = genai.GenerativeModel('gemini-1.5-flash')
system_role = "You are a female virtual assistant named Sidney skilled in general tasks like Alexa and Google Cloud."
user_role = "What is engineering?"
response = model.generate_content(f"{system_role}. {user_role} ")
print(response.text)





