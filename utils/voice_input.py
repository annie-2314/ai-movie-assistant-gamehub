import speech_recognition as sr

def transcribe_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, could not understand."
    except sr.RequestError:
        return "Speech recognition service failed."
