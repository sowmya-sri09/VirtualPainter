# VoiceModule.py
import speech_recognition as sr

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Say a command...")
        audio = recognizer.listen(source, phrase_time_limit=3)
        try:
            command = recognizer.recognize_google(audio).lower()
            print("🗣️ You said:", command)
            return command
        except:
            print("❌ Voice not recognized")
            return ""
