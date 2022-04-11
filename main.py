from Helios import *

def main():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[5].id)
    engine.setProperty('rate', 150)

    sr = speech_recognition.Recognizer()
    va = Helios()

    while True:
        try:
            with speech_recognition.Microphone(device_index=1) as mic:
                engine.say('Я вас слушаю')
                engine.runAndWait()

                # Учет уровня шума
                sr.adjust_for_ambient_noise(source=mic, duration=0.5)
                audio = sr.listen(source=mic)

                engine.say('Вас понял')
                engine.runAndWait()

                query = sr.recognize_google(audio_data=audio, language='ru_RU').lower()
                for k, v in config['commands'].items():
                    fuzzy_comparison = process.extractOne(query, v)
                    print(fuzzy_comparison)
                    if fuzzy_comparison[1] >= 80:
                        execute = getattr(va, k)
                        execute()
        except Exception as _ex:
            print(_ex, 'Команда не распознана')
            pass

if __name__ == '__main__':
    main()