import pyttsx3
import speech_recognition as sr
import webbrowser
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog
from threading import Thread
import pydub
from pydub import AudioSegment
from pydub.playback import play

# إعداد المحرك الصوتي
wel = pyttsx3.init()
voices = wel.getProperty('voices')
wel.setProperty('voice', voices[0].id)
for voice in voices:
    if "female" in voice.name.lower() and ("arabic" in voice.name.lower() or "ar" in voice.id.lower()):
        wel.setProperty('voice', voice.id)
        break

def speak(audio):
    wel.say(audio)
    wel.runAndWait()

class CommandsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant")
        self.root.geometry("400x400")
        self.root.configure(bg="black")

        title_label = tk.Label(
            self.root, text="I'm Zaky ", font=("Times New Roman", 18, "bold"), fg="white", bg="black"
        )
        title_label.pack(pady=10)

        commands = """
        
"""
        commands_label = tk.Label(
            self.root, text=commands, font=("Arial", 14), fg="white", bg="black", justify="left"
        )
        commands_label.pack(pady=10)

        self.output_label = tk.Label(
            self.root, text="", font=("Arial", 14), fg="lightblue", bg="black", justify="center"
        )
        self.output_label.pack(pady=20)

    def update_output(self, message):
        self.output_label.config(text=message)

    def show(self):
        self.root.mainloop()

    def close(self):
        self.root.destroy()

def takecommand():
    command = sr.Recognizer()
    with sr.Microphone() as mic:
        print("Listening for a command...")
        command.pause_threshold = 1
        try:
            audio = command.listen(mic)
            print("Recognizing...")
            query = command.recognize_google(audio, language="en-US")
            print(f"You said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            print("Sorry, I did not understand that.")
            return None
        except Exception as e:
            print(f"Error: {e}")
            speak("An error occurred while processing your command.")
            return None

def tell_time(app):
    current_time = datetime.now().strftime("%H:%M:%S")
    message = f"The time is {current_time}"
    speak(message)
    app.update_output(message)

def play_alarm_sound():
    try:
        # تشغيل صوت البداية
        alarm_sound = AudioSegment.from_mp3("C:/Users/kh/OneDrive/Desktop/system _alarm/1.mp3")
        play(alarm_sound)
    except FileNotFoundError:
        print("Error: Alarm sound file (1.mp3) not found.")
        return

def set_alarm(app):
    # هنا نعرض نافذة إدخال الوقت في الخيط الرئيسي باستخدام `after`
    def get_alarm_time():
        user_time = simpledialog.askstring("Set Alarm", "Enter alarm time in HH:MM format:")
        if not user_time:
            app.update_output("No time entered for alarm.")
            return

        # تشغيل صوت البداية في خيط منفصل
        Thread(target=play_alarm_sound).start()

        app.update_output(f"Alarm set for {user_time}. Waiting...")

        # انتظار حتى الوقت المحدد في خيط منفصل
        def wait_for_alarm():
            while True:
                now = datetime.now().strftime( "%H:%M")
                if now == user_time:
                    try:
                        for _ in range(4):
                         alert_sound = AudioSegment.from_mp3("C:/Users/kh/OneDrive/Desktop/system _alarm/2.mp3")
                         print("Playing alarm!")
                         app.update_output("Alarm ringing!")
                         play(alert_sound)
                    except FileNotFoundError:
                        print("Error: Alert sound file (2.mp3) not found.")
                        app.update_output("Error: Alert sound file not found.")
                    break  # بعد تشغيل المنبه نخرج من الحلقة
        Thread(target=wait_for_alarm).start()

    app.root.after(100, get_alarm_time)  

if __name__ == "__main__":
    root = tk.Tk()
    app = CommandsApp(root)

    def run_voice_assistant():
        speak("Hello sir Mohamed, how can I help you?")
        while True:
            query = takecommand()
            if not query:
                app.update_output("Listening for a command...")
                continue

            if "hello" in query:
                message = "Hello Mohamed!"
                speak(message)
                app.update_output(message)

            elif "open youtube" in query:
                message = "Opening YouTube."
                speak(message)
                app.update_output(message)
                webbrowser.open_new_tab("https://www.youtube.com")

            elif "what is the time now" in query or "what is the time" in query:
                tell_time(app)

            elif "stop" in query:
                message = "I hope you have a good day!"
                speak(message)
                app.update_output(message)
                app.close()
                break

            elif "how are you" in query:
                message = "I am fine, thank you!"
                speak(message)
                app.update_output(message)

            elif "play music" in query:
                message = "Okay, opening Anghami."
                speak(message)
                app.update_output(message)
                webbrowser.open_new_tab("https://play.anghami.com/album/1023656909")

            elif "set alarm" in query or "alarm" in query:
                message = "Sure, let's set an alarm."
                speak(message)
                app.update_output(message)
                set_alarm(app)

            elif "what can you do" in query:
                message = "I can assist you with various tasks like setting alarms, opening websites, and more!"
                speak(message)
                app.update_output(message)

            elif "search for" in query:
                # استخراج كلمة البحث من الجملة
                search_query = query.replace("search for", " ").strip()
                if search_query:
                    message = f"بحثت عن {search_query} على يوتيوب."
                    speak(message)
                    app.update_output(message)
                    # فتح يوتيوب مع كلمة البحث
                    webbrowser.open_new_tab(f"https://www.youtube.com/results?search_query={search_query}")
                else:
                    message = "من فضلك، قل ما الذي تريد البحث عنه."
                    speak(message)
                    app.update_output(message)
            elif "google" in query:
                search_query1 = query.replace("google", " ").strip()
                if search_query1:
                    message = f"okay {search_query1}"
                    speak(message)
                    app.update_output(message)
                    # 
                    webbrowser.open_new_tab(f"https://www.google.com/search?q={search_query1}")
                else:
                    message = "what do you want "
                    speak(message)
                    app.update_output(message)
            else:
                message = "Command not recognized. Please try again."
                speak(message)
                app.update_output(message)


    Thread(target=run_voice_assistant).start()
    app.show()
