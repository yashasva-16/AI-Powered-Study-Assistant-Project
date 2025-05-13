import os
import time
import pyttsx3
import speech_recognition as sr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from plyer import notification
import json
import random
import requests

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

# Weather API Key
WEATHER_API_KEY = 'your_api_key_here'

# Motivational Quotes
quotes = [
    "Keep pushing, you're doing great!",
    "Stay focused and never give up.",
    "Success is the sum of small efforts repeated daily.",
    "Every hour you study is a step closer to your dream."
]

# Study Data
study_data = {'Subject': [], 'Topic': [], 'Hours': [], 'Date': []}

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in TTS: {e}")



# Listen to User Commands
def listen_command():
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
    except Exception as e:
        print(f"Error: {e}")
        return ""

# Task Management
tasks = []

def add_task(task):
    tasks.append(task)
    speak("Task added successfully.")

def show_tasks():
    if tasks:
        for i, task in enumerate(tasks):
            print(f"{i+1}. {task}")
        speak("Here are your tasks.")
    else:
        speak("You have no tasks.")

# Weather Information
def get_weather():
    try:
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q=Delhi&appid={WEATHER_API_KEY}&units=metric")
        weather_data = response.json()
        temp = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        return f"The current temperature is {temp}°C with {description}."
    except Exception as e:
        print(f"Weather API error: {e}")
        return "Weather data not available."

# Study Data Logging
def log_study_data(subject, topic, hours):
    date = datetime.now().strftime("%Y-%m-%d")
    study_data['Subject'].append(subject)
    study_data['Topic'].append(topic)
    study_data['Hours'].append(hours)
    study_data['Date'].append(date)
    df = pd.DataFrame(study_data)
    df.to_csv('study_log.csv', index=False)
    speak(f"Logged {hours} hours for {subject} - {topic}")

# Study Timer
def start_study_timer(minutes):
    speak(f"Starting a study session for {minutes} minutes.")
    time.sleep(minutes * 60)
    speak("Time is up! Take a short break.")

# Main Function
def main():
    speak("Hello, I am your personal study assistant. How can I help you today?")

    while True:
        command = listen_command()

        if "log study" in command:
            speak("What subject did you study?")
            subject = listen_command()
            speak("What topic did you cover?")
            topic = listen_command()
            speak("How many hours did you spend?")
            try:
                hours = float(listen_command())
                log_study_data(subject, topic, hours)
            except ValueError:
                speak("Please enter a valid number of hours.")

        elif "add task" in command:
            speak("What is the task?")
            task = listen_command()
            add_task(task)

        elif "show tasks" in command:
            show_tasks()

        elif "weather" in command:
            weather = get_weather()
            speak(weather)

        elif "study timer" in command:
            speak("For how many minutes?")
            try:
                minutes = int(listen_command())
                start_study_timer(minutes)
            except ValueError:
                speak("Please enter a valid number.")

        elif "motivate" in command:
            quote = random.choice(quotes)
            speak(quote)

        elif "exit" in command:
            speak("Goodbye! Stay focused and keep studying.")
            break

        else:
            speak("I am here to assist you. You can ask me to log study, add a task, check weather, or set a study timer.")

if __name__ == "__main__":
    main()
