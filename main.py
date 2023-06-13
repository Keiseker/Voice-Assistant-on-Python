
# № для машинного обучения
import words
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
# № для интерфейса
import sys
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow
from design import Ui_MainWindow
# № для потоков
import threading
# № для распознавания речи
import queue
import sounddevice as sd
import vosk
import json
# № для синтеза речи
import tts
# № для функцмй
import random
import requests
from num2t4ru import num2text
import sqlite3
import webbrowser

# № для распознавания


def callback(indata, frames, time, status):
    q.put(bytes(indata))


q = queue.Queue()

# ? device - используем девайс по умолчанию
device = sd.default.device
# ? samplerate - частота дискретизации(сколько раз в секунду микро замеряет шум)
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])
model = vosk.Model('vosk_model_small')

# № для машинного обучения
# # передача образцов фраз, чтобы найти закономерность
vectorizer = CountVectorizer()
vectors = vectorizer.fit_transform(list(words.data_set.keys()))

# # передача образцов фраз для ответа бота
clf = LogisticRegression()
clf.fit(vectors, list(words.data_set.values()))

# # освобождение оперативной памяти
del words.data_set

# № для main
work = True


class VoiceAssistant(QMainWindow, threading.Thread, Ui_MainWindow):
    def __init__(self):
        super(VoiceAssistant, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_start.clicked.connect(self.start_thread_assist)
        self.ui.btn_stop.clicked.connect(self.off)

# ? КОМАНДЫ ГОЛОСОВОГО ПОМОЩНИКА
    def youtube_search(self):
        tts.va_speak('Скажите название ролика, который я должна найти')
        search = self.listen_command()
        self.user(search)
        tts.va_speak('Ищу ролик на ютубе')
        self.Eva('Ищу ролик на ютубе')
        webbrowser.open(
            f'https://www.youtube.com/results?search_query={search}')

    def web_search(self):
        tts.va_speak('Повторите, что вы хотите найти')
        search = self.listen_command()
        self.user(search)
        tts.va_speak('Сейчас')
        self.Eva('Сейчас')
        webbrowser.open(
            f'https://www.google.com/search?q={search}&oq={search}'f'81&aqs=chrome..69i57j46i131i433j0l5.2567j0j7&sourceid=chrome&ie=UTF-8')

    def get_anekdote(self):
        connection = sqlite3.connect('anekdot.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM anekdot ORDER BY RANDOM() LIMIT 1")
        anekdote_row = cursor.fetchone()
        connection.close()
        if anekdote_row:
            anekdote = anekdote_row[1]
        else:
            anekdote = "К сожалению, в базе данных пока нет анекдотов"
        return anekdote

    def send_anekdote(self):
        anekdote = self.get_anekdote()
        tts.va_speak(anekdote)
        self.Eva(anekdote)
    # # Функция Выбор города для просмотра погоды

    def choose_city(self):
        tts.va_speak('Назовите город, где хотите узнать погоду')
        request_result = self.listen_command()
        self.user(request_result)
        self.check_weather(request_result)

    # # Функция Проверка погоды в данный момент в данном городе

    def check_weather(self, city):
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
            self.Eva("На улице " + weather + num2text(temp)+"градусов")
        except:
            value = 1
            tts.va_speak("Я вас не понял, повторите")
            self.Eva('Я вас не поняла, повторите')
        if value == 1:
            self.choose_city()
    # # Функция Справка, о функционале ассистента

    def info(self):
        tts.va_speak("Привет, я голосовой ассистент Ева! Я могу принять решение за вас, подкинув монетку, посмотреть текущую погоду в вашем городе, рассказать анекдот, найти нужный сайт или видео. Приятно с вами познакомиться!")
        self.Eva('Привет, я голосовой ассистент Ева!\nЯ могу принять решение за вас, подкинув монетку, посмотреть текущую погоду в вашем городе,\nрассказать анекдот, найти нужный сайт или видео.\nПриятно с вами познакомиться!')
    # #Функция-заглушка для разговоров

    def passive(self):
        ''''''

    # #Функция "Подбрось монетку"

    def flip_coin(self):
        m = random.randint(0, 1)
        if m == 0:
            tts.va_speak('Выпала решка')
            self.Eva("Выпала решка")
        else:
            tts.va_speak('Выпал орел')
            self.Eva("Выпал орел")
#! КОМАНДЫ ОСНОВНЫЕ ДЛЯ РАБОТЫ
    # # Сообщение Евы

    def Eva(self, text):
        if text != '':
            item = QtWidgets.QListWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
            item.setText('  Ева: ' + text)
            self.ui.listWidget.addItem(item)

    # # Сообщение Пользователя

    def user(self, text):
        if text != '':
            item = QtWidgets.QListWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
            item.setText('  Вы: ' + text)
            self.ui.listWidget.addItem(item)
        # # Распознавание команды

    def do_this_command(self, request_result, vectorizer, clf):
        trg = words.TRIGGERS.intersection(request_result.split())
        # ? удаление имя бота
        try:
            request_result = request_result.replace(list(trg)[0], '')
        except:
            """"""
        # ? формирование запроса пользователя
        text_vector = vectorizer.transform([request_result]).toarray()[0]
        answer = clf.predict([text_vector])[0]

        func_name = answer.split()[0]
        print(request_result)
        print(answer)
        print(func_name)

        if ((request_result != '') & (answer == 'passive ')):
            tts.va_speak("Я вас не поняла, повторите")
            self.Eva('Я вас не поняла, повторите')
        elif (request_result == '' or request_result == ' '):
            func_name = 'passive'
        else:
            try:
                tts.va_speak(answer.replace(func_name, ''))
                self.Eva(answer.replace(func_name, ''))

            except:
                func_name = 'passive'
        exec('self.'+func_name + '()')

    # # Распознавание ответа пользователя

    def listen_command(self):
        with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device[0],
                               dtype="int16", channels=1, callback=callback):
            rec = vosk.KaldiRecognizer(model, samplerate)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    request_result = json.loads(rec.Result())['text']
                    return request_result.lower()

    # # Остановка ассистента

    def off(self):
        global work
        work = False

    # # Запуск ассистента
    def main(self):
        global work
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        item.setText('\nЧтобы начать работу с ассистентом скажите: Ева')
        self.ui.listWidget.addItem(item)
        while True:
            command = self.listen_command()
            trg = words.TRIGGERS.intersection(command.split())
            if trg:
                tts.va_speak('Привет')
                self.Eva('Привет')
                tts.va_speak('Слушаю вас')
                self.Eva('Слушаю вас')
                while work:
                    command = self.listen_command()
                    self.user(command)
                    self.do_this_command(command, vectorizer, clf)
            elif 'пока' in command or 'до свидания' in command:
                tts.va_speak('До свидания')
                self.Eva('До свидания')
                break
            else:
                """"""

    def start_thread_assist(self):
        thread = threading.Thread(target=self.main, args=())
        thread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoiceAssistant()
    window.show()
    sys.exit(app.exec())
