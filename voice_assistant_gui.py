import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import pyautogui
import pyjokes
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

# Initialize TTS engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)


def speak(audio) -> None:
    engine.say(audio)
    engine.runAndWait()


def time() -> None:
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    log_output(f"Time: {current_time}")
    speak(f"The current time is {current_time}")


def date() -> None:
    now = datetime.datetime.now()
    log_output(f"Date: {now.day}/{now.month}/{now.year}")
    speak(f"The current date is {now.day} {now.strftime('%B')} {now.year}")


def wishme() -> None:
    speak("Welcome back, sir!")
    log_output("Welcome back, sir!")

    hour = datetime.datetime.now().hour
    greeting = (
        "Good morning!" if 4 <= hour < 12 else
        "Good afternoon!" if 12 <= hour < 16 else
        "Good evening!" if 16 <= hour < 24 else
        "Good night, see you tomorrow."
    )

    speak(greeting)
    log_output(greeting)

    assistant_name = load_name()
    speak(f"{assistant_name} at your service. Please tell me how may I assist you.")
    log_output(f"{assistant_name} at your service.")


def screenshot() -> None:
    img = pyautogui.screenshot()
    img_path = os.path.expanduser("~\\Pictures\\screenshot.png")
    img.save(img_path)
    speak("Screenshot saved.")
    log_output(f"Screenshot saved at {img_path}")


def takecommand() -> str:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        log_output("Listening...")
        try:
            audio = r.listen(source, timeout=5)
        except sr.WaitTimeoutError:
            speak("Timeout occurred. Please try again.")
            return None

    try:
        log_output("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        log_output(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand that.")
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
    return None


def play_music(song_name=None) -> None:
    song_dir = os.path.expanduser("~\\Music")
    songs = os.listdir(song_dir)

    if song_name:
        songs = [song for song in songs if song_name.lower() in song.lower()]

    if songs:
        song = random.choice(songs)
        os.startfile(os.path.join(song_dir, song))
        speak(f"Playing {song}")
        log_output(f"Playing: {song}")
    else:
        speak("No song found.")
        log_output("No song found.")


def set_name() -> None:
    name = simpledialog.askstring("Set Assistant Name", "What would you like to name me?")
    if name:
        with open("assistant_name.txt", "w") as file:
            file.write(name)
        speak(f"Alright, I will be called {name} from now on.")
        log_output(f"Assistant renamed to {name}")


def load_name() -> str:
    try:
        with open("assistant_name.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "Ionix"


def search_wikipedia() -> None:
    query = simpledialog.askstring("Wikipedia Search", "What do you want to search on Wikipedia?")
    if query:
        try:
            speak("Searching Wikipedia...")
            result = wikipedia.summary(query, sentences=2)
            speak(result)
            log_output(result)
        except wikipedia.exceptions.DisambiguationError:
            speak("Multiple results found. Please be more specific.")
        except Exception:
            speak("I couldn't find anything on Wikipedia.")


def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)
    log_output(joke)


def listen_and_execute():
    query = takecommand()
    if not query:
        return

    if "time" in query:
        time()
    elif "date" in query:
        date()
    elif "wikipedia" in query:
        search_wikipedia()
    elif "play music" in query:
        song_name = query.replace("play music", "").strip()
        play_music(song_name)
    elif "open youtube" in query:
        wb.open("https://www.youtube.com")
    elif "open google" in query:
        wb.open("https://www.google.com")
    elif "change your name" in query:
        set_name()
    elif "screenshot" in query:
        screenshot()
    elif "tell me a joke" in query:
        tell_joke()
    elif "shutdown" in query:
        speak("Shutting down.")
        os.system("shutdown /s /f /t 1")
    elif "restart" in query:
        speak("Restarting.")
        os.system("shutdown /r /f /t 1")
    elif "offline" in query or "exit" in query:
        speak("Going offline.")
        root.destroy()


# GUI setup
root = tk.Tk()
root.title("Python Voice Assistant")
root.geometry("700x500")
root.config(bg="#1f1f2e")

output_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Segoe UI", 12), bg="#2a2a40", fg="white")
output_box.place(x=20, y=20, width=660, height=300)


def log_output(text):
    output_box.insert(tk.END, text + "\n")
    output_box.see(tk.END)


# Buttons
btn_frame = tk.Frame(root, bg="#1f1f2e")
btn_frame.place(x=20, y=340)

tk.Button(btn_frame, text="Listen", width=15, command=listen_and_execute, bg="#282c34", fg="white").grid(row=0, column=0, padx=10, pady=10)
tk.Button(btn_frame, text="Time", width=15, command=time, bg="#282c34", fg="white").grid(row=0, column=1, padx=10, pady=10)
tk.Button(btn_frame, text="Date", width=15, command=date, bg="#282c34", fg="white").grid(row=0, column=2, padx=10, pady=10)
tk.Button(btn_frame, text="Wikipedia", width=15, command=search_wikipedia, bg="#282c34", fg="white").grid(row=1, column=0, padx=10, pady=10)
tk.Button(btn_frame, text="Play Music", width=15, command=lambda: play_music(), bg="#282c34", fg="white").grid(row=1, column=1, padx=10, pady=10)
tk.Button(btn_frame, text="Screenshot", width=15, command=screenshot, bg="#282c34", fg="white").grid(row=1, column=2, padx=10, pady=10)
tk.Button(btn_frame, text="Joke", width=15, command=tell_joke, bg="#282c34", fg="white").grid(row=2, column=0, padx=10, pady=10)
tk.Button(btn_frame, text="Rename Assistant", width=15, command=set_name, bg="#282c34", fg="white").grid(row=2, column=1, padx=10, pady=10)
tk.Button(btn_frame, text="Exit", width=15, command=root.destroy, bg="red", fg="white").grid(row=2, column=2, padx=10, pady=10)

wishme()
root.mainloop()
