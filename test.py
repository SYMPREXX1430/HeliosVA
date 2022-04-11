import speech_recognition as sr
import pyttsx3

def talk(msg):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[5].id)
    engine.setProperty('rate', 150)
    engine.say(msg)
    engine.runAndWait()


def record_volume():
    r = sr.Recognizer()
    with sr.Microphone(device_index = 1) as source:
        talk('Настраиваюсь.')
        r.adjust_for_ambient_noise(source, duration=0.5) #настройка посторонних шумов
        talk('Слушаю...')
        audio = r.listen(source)
    talk('Услышала.')
    try:
        query = r.recognize_google(audio, language = 'ru-RU')
        text = query.lower()
        print(f'Вы сказали: {query.lower()}')
        talk(f'Вы сказали: {query.lower()}')
    except:
        talk('Error')

while True:
    record_volume()