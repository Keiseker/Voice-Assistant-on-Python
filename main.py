
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
from bs4 import BeautifulSoup as b
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


class VoiceAssistant(QMainWindow, threading.Thread, Ui_MainWindow):
    def __init__(self):
        super(VoiceAssistant, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.thread = None
        self.ui.btn_start.clicked.connect(self.start_thread_assist)
        self.ui.btn_stop.clicked.connect(self.off)
        self.ui.btn_stop.setEnabled(False)

        # № для main
        self.work = True
        # № для машинного обучения
        # # передача образцов фраз, чтобы найти закономерность
        self.vectorizer = CountVectorizer()
        self.vectors = self.vectorizer.fit_transform(
            list(words.data_set.keys()))

        # # передача образцов фраз для ответа бота
        self.clf = LogisticRegression()
        self.clf.fit(self.vectors, list(words.data_set.values()))

        # # освобождение оперативной памяти
        del words.data_set

# ? КОМАНДЫ ГОЛОСОВОГО ПОМОЩНИКА
    def youtube_search(self):
        self.Eva('Скажите название ролика, который я должна найти.')
        search = self.listen_command()
        self.user(search)
        self.Eva('Ищу ролик на ютубе.')
        webbrowser.open(
            f'https://www.youtube.com/results?search_query={search}')

    def web_search(self):
        self.Eva('Повторите, что вы хотите найти.')
        search = self.listen_command()
        self.user(search)
        self.Eva('Сейчас.')
        webbrowser.open(
            f'https://www.google.com/search?q={search}&oq={search}'f'81&aqs=chrome..69i57j46i131i433j0l5.2567j0j7&sourceid=chrome&ie=UTF-8')

    def get_anekdote(self):
        r = requests.get('https://anekdotme.ru/anekdoti_aforizmi/')
        soup = b(r.text, 'html.parser')
        anekdots = soup.find_all('div', class_='anekdot_text')
        anekdots = [c.text for c in anekdots]
        anekdots = [c.replace('\r\n                    ', '')
                    for c in anekdots]
        an = ''
        index = random.randint(0, len(anekdots)-1)
        for j in range(len(anekdots[index])):
            if j % 45 == 0:
                an = anekdots[index][:j]+'\n'+anekdots[index][j:]
            else:
                an = anekdots[index]
            anekdots[index] = an
        return anekdots[index]

    def send_anekdote(self):
        anekdote = self.get_anekdote()
        print(type(anekdote))
        self.Eva(anekdote)

    # # Функция Справка, о функционале ассистента

    def info(self):
        self.Eva('Привет, я голосовой ассистент Ева!\nЯ могу принять решение за вас, подкинув монетку,\nрассказать анекдот, найти нужный сайт или видео.\nПриятно с вами познакомиться!')
    # #Функция-заглушка для разговоров

    def passive(self):
        ''''''

    # #Функция "Подбрось монетку"()

    def flip_coin(self):
        m = random.randint(0, 1)
        if m == 0:
            self.Eva("Выпала решка.")
        else:
            self.Eva("Выпал орел.")
#! КОМАНДЫ ОСНОВНЫЕ ДЛЯ РАБОТЫ
    # # Сообщение Евы

    def Eva(self, text):
        if text != '':
            item = QtWidgets.QListWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
            item.setText('  Ева: ' + text)
            self.ui.listWidget.addItem(item)
            tts.va_speak(text)

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
            request_result = request_result
        # ? формирование запроса пользователя
        text_vector = vectorizer.transform([request_result]).toarray()[0]
        answer = clf.predict([text_vector])[0]

        func_name = answer.split()[0]

        if ((request_result != '') & (answer == 'passive')):
            self.Eva('Я вас не поняла, повторите.')
        elif (request_result == '' or request_result == ' '):
            func_name = 'passive'
        else:
            try:
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
        self.ui.btn_start.setEnabled(True)
        self.ui.btn_stop.setEnabled(False)
        self.work = False
        if self.thread is not None:  # Если есть запущенный поток
            self.thread.join()  # Дождитесь завершения потока
            self.thread = None  # Удалите ссылку на завершенный поток
        sys.exit()

    # # Запуск ассистента
    def main(self):
        item = QtWidgets.QListWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        item.setText('\nЧтобы начать работу с ассистентом скажите: Ева')
        self.ui.listWidget.addItem(item)
        while self.work:
            command = self.listen_command()
            trg = words.TRIGGERS.intersection(command.split())
            if trg:
                self.Eva('Привет, слушаю вас.')

                while self.work:
                    command = self.listen_command()
                    self.user(command)
                    self.do_this_command(command, self.vectorizer, self.clf)
            elif 'пока' in command or 'до свидания' in command:
                self.Eva('До свидания.')
                break
            else:
                """"""

    def start_thread_assist(self):
        self.ui.btn_start.setEnabled(False)
        self.ui.btn_stop.setEnabled(True)
        # Начать новый поток только в том случае, если нет активного.
        if self.thread is None or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.main, args=())
            self.thread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VoiceAssistant()
    window.show()
    sys.exit(app.exec())
