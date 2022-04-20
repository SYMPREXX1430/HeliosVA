# -*- coding: utf-8 -*-

import speech_recognition
import sys
import os
import pyttsx3
import webbrowser as wb
from fuzzywuzzy import process
from config import owm_token
import requests

config = {'commands':
              {
                  'create_task': ['добавить задачу', 'список дел', 'задача'],
                  'weather_report': ['прогноз погоды', 'погода'],
                  'close': ['захлопнись', 'закройся', 'брысь', 'завершить работу', 'выйти', 'досвидания', 'досвидос', 'пока'],
                  'restart_pc': ['перезагрузка', 'перезагрузить компьютер'],
                  'cancel_restart_pc': ['отмена перезагрузки', 'отменить перезагрузку'],
                  'shutdown_pc': ['выключение', 'выключить компьютер'],
                  'cancel_shutdown_pc': ['отмена выключения', 'отменить выключение'],
                  'browser': ['браузер', 'открыть браузер', 'поиск']
              }
          }

class Helios():
    def __init__(self):
        # Инициализация голосового движка
        self.engine = pyttsx3.init()
        # Выбор голоса
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[5].id)
        # Выбор скорости произношения
        self.engine.setProperty('rate', 150)
        self.sr = speech_recognition.Recognizer()

    # Распознование команды
    def hear(self):
        try:
            with speech_recognition.Microphone(device_index=1) as mic:
                # Учет уровня шума
                self.sr.adjust_for_ambient_noise(source=mic, duration=0.5)
                audio = self.sr.listen(source=mic)
                query = self.sr.recognize_google(audio_data=audio, language='ru_RU').lower()
            return query
        except speech_recognition.UnknownValueError:
            self.talk('Повторите команду')

    # Воспроизведение ответа
    def talk(self, message):
        self.engine.say(message)
        self.engine.runAndWait()
        # engine.say() не выводит реплики мгновенно, а собирает их в очередь,
        # которую затем нужно запустить на воспроизведение командой engine.runAndWait().

    # Добавление задачи в список дел
    def create_task(self):
        self.talk('Что добавить в список дел?')
        task = self.hear()
        if task != None:
            with open('to-do_list.txt', 'a') as file:
                file.write(f'- {task}\n')
            self.talk(f'Задача {task} добавлена в список дел')


    # Закрытие программы
    def close(self):
        self.talk('До свидания.')
        sys.exit()

    # Перезагрузка ПК
    def restart_pc(self):
        os.system('shutdown -r +5')
        self.talk('Компьютер будет перезагружен через 5 минут. Введите "shutdown - c" для отмены перезагрузки')

    # Отмена перезагрузки ПК
    def cancel_restart_pc(self):
        os.system('shutdown -c')
        self.talk('Перезагрузка была успешно отменена')

    # Выключение ПК
    def shutdown_pc(self):
        os.system('shutdown +5')
        self.talk('Компьютер будет выключен через 5 минут. Введите "shutdown - c" для отмены выключения')

    # Отмена перезагрузки ПК
    def cancel_shutdown_pc(self):
        os.system('shutdown -c')
        self.talk('Выключение было успешно отменено')

    # Веб-браузер
    def browser(self):
        self.talk('Что ищем?')

        query = self.hear()
        if 'видео' in query:
            query.replace('видео', '')
            query = query.split()
            wb.open('https://www.youtube.com/results?search_query=' + '+'.join(query[1::]))

        elif 'музыка' in query:
            query.replace('музыка', '')
            query = query.split()
            wb.open('https://music.youtube.com/search?q=' + '+'.join(query[1::]))

        else:
            wb.open(f'https://yandex.ru/search/?text={query}')

    # Получение прогноза погоды и подготовка сообщения
    def get_weather(self, city, token):
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={token}&lang=ru&units=metric')
        data = r.json()

        city_name = data['name']
        weather_description = data['weather'][0]['description']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        wind_speed = data['wind']['speed']
        wind_gust = data['wind']['gust']

        msg_to_say = f'Погода в городe {city_name}: {temp} градусов Цельсия, {weather_description}. ' \
                     f'Ощущается как {feels_like}. Скорость ветра {wind_speed} метров в секунду, с порывами до {wind_gust} метров в секунду'

        self.talk(msg_to_say)

    # Определение города и запуск get_weather
    def weather_report(self):
        self.talk('Погода в каком городе Вас интересует?')
        try:
            city = self.hear()
            if city != None:
                self.get_weather(city, owm_token)
        except Exception as e:
            self.talk('Ошибка в прогнозе погоды')
            print('Error ', e)


