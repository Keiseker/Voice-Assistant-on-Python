from time import sleep
import random
import os
import tts
import threading
# # для распознавания
import queue
import sounddevice as sd
import vosk
import json
# # для погоды
import requests
from num2t4ru import num2text

command_list = ["привет", "подкинь", "погода", "справка", "пока"]
discription_list = ["приветствие", "подкидывает монетку",
                    "скажет погоду сейчас в заданном городе", "показывает список комманд", "прощание"]

# * ФУНКЦИИ ПРОГРАММЫ * ФУНКЦИИ ПРОГРАММЫ *  ФУНКЦИИ ПРОГРАММЫ * ФУНКЦИИ ПРОГРАММЫ * ФУНКЦИИ ПРОГРАММЫ *

q = queue.Queue()

# ? device - используем девайс по умолчанию
device = sd.default.device
# ? samplerate - частота дискретизации(сколько раз в секунду микро замеряет шум)
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])
model = vosk.Model('vosk_model_small')


def callback(indata, frames, time, status):
    q.put(bytes(indata))


def listen_command():
    with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device[0],
                           dtype="int16", channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, samplerate)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                request_result = json.loads(rec.Result())['text']
                return request_result.lower()
# #Функция "Слушай"


def commands_print():
    print("Список команд:")
    for i in range(len(command_list)):
        print(command_list[i]+' - '+discription_list[i])
# #Функция "Выведи список"


def flip_coin():
    m = random.randint(0, 1)
    if m == 0:
        tts.va_speak('Выпала решка')
        print("Выпала решка")
    else:
        tts.va_speak('Выпал орел')
        print("Выпал орел")
# #Функция "Подбрось монетку"


def open_programs():
    list1 = ['steam', 'telegram', "chrome", "discord"]
    link_list = ["C:\\Program Files (x86)\\Steam\\steam.exe",
                 "C:\\Users\\ADMIN\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe", "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe", "C:\\Users\\ADMIN\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Discord Inc\\Discord.lnk"]
    tts.va_speak('Выберите номер файла')
    for i in range(len(list1)):
        print(i+1, list1[i])
    choice = int(listen_command())
    os.startfile(link_list[choice-1])
    tts.va_speak('Открыл')
# #Функция "Открой приложение"

# # выбор города для просмотра погоды


def choose_city():
    tts.va_speak('Назовите город, где хотите узнать погоду')
    request_result = listen_command()
    check_weather(request_result)

# # проверка погоды сейчас


def check_weather(city):
    value = 0
    try:
        params = {'q': city, 'units': 'metric',
                  'lang': 'ru', 'appid': 'a7578a6bf6fc5cc5ad71e3efdee74eb8'}
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather', params=params)
        if not response:
            raise
        w = response.json()
        weather = w["weather"][0]['description']
        temp = round(w['main']['temp'])
        tts.va_speak("На улице " + weather + num2text(temp)+"градусов")
        # voice.speaker

    except:
        value = 1
        tts.va_speak("Я вас не понял, повторите")
    if value == 1:
        choose_city()


def passive():
    ''''''
# #Функция-заглушка для разговоров
