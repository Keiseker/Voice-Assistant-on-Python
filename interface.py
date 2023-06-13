from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QListWidget, QLineEdit, QListWidgetItem
import sys


class App(QWidget):
    def setupUi(self):

        # Создание основного окна
        self.resize(300, 500)
        self.setWindowTitle("Голосовой помощник Джарвис")
        self.setFixedSize(300, 500)

        # Установка нулевых отступов
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        #! Создание upbar_frame
        self.upbar_frame = QWidget()
        self.upbar_frame.setStyleSheet("background-color: #011a27;")
        self.upbar_frame.setFixedSize(300, 50)

        #! Создание заголовка
        self.name = QLabel("Джарвис")
        self.name.setStyleSheet(
            "color: #99ee44; font-size: 18px;font-family: Roboto; font-weight: bold;")

        #! Создание кнопки Помощь ?
        self.btn_help = QPushButton()
        #! Устанавливаем уникальный идентификатор для кнопки
        self.btn_help.setObjectName("BtnHelp")
        self.btn_help.setStyleSheet("""
            QPushButton#BtnHelp {
                background-color: #99ee44;
                border-radius: 17px;
                font-size: 16px;
                font-family: Roboto;
                font-weight: bold;
            }

            QPushButton#BtnHelp:hover {
                background-color: #59a30f;
            }
            
        """)
        self.btn_help.setFixedSize(35, 35)
        self.btn_help.setText("?")
        self.btn_help.clicked.connect(self.get_assistant_messages)

        #! Добавление элементов на upbar_frame
        self.upbar_frame.layout = QHBoxLayout()
        self.upbar_frame.layout.setContentsMargins(10, 0, 10, 0)
        self.upbar_frame.layout.addWidget(self.name)
        self.upbar_frame.layout.addWidget(self.btn_help)
        self.upbar_frame.setLayout(self.upbar_frame.layout)

        # ? Создание textbox_frame
        self.textbox_frame = QWidget()
        self.textbox_frame.setStyleSheet("background-color: #092a36;")
        self.textbox_frame.setFixedSize(300, 400)

        # ? Создание text_box
        self.text_box = QListWidget()
        self.text_box.addItem("Текст, который должен озвучиваться 1")
        self.text_box.addItem("Текст, который должен озвучиваться 1")
        self.text_box.addItem("Текст, который должен озвучиваться 1")
        self.text_box.setStyleSheet("""
            QTextEdit {
                border: 1px solid #99ee44;
                border-radius: 5px;
                color: #99ee44;
                font-size: 16px;
                font-family: Roboto;
                padding :5px;

            }
            QScrollBar:vertical {
                width: 10px;
                background-color: #092a36;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background-color: #011a27;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                background-color: #e0e0e0;
                height: 10px;
            }
            QScrollBar::up-arrow:vertical,
            QScrollBar::down-arrow:vertical {
                background-color: #999999;
                height: 10px;
                width: 10px;
            }
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background-color: #092a36;
            }

            """)

        # ? Добавление элементов на textbox_frame
        self.textbox_frame.layout = QHBoxLayout()
        self.textbox_frame.layout.addWidget(self.text_box)
        self.textbox_frame.setLayout(self.textbox_frame.layout)

        # # Создание downbar_frame
        self.downbar_frame = QWidget()
        self.downbar_frame.setStyleSheet("background-color: #011a27;")
        self.downbar_frame.setFixedSize(300, 50)

        # # Создание поля ввода
        self.text_edit = QLineEdit()
        self.text_edit.setFixedSize(225, 30)
        self.text_edit.setStyleSheet("""
            QLineEdit {
                background-color: #092a36;
                border: 1px solid #99ee44;
                border-radius: 5px;
                color: #99ee44;
                font-size: 14px;
                font-family: Roboto;
                padding :5px;

            }""")

        # # Создание кнопки "Говорить"
        self.btn_micro = QPushButton()
        # # Устанавливаем уникальный идентификатор для кнопки
        self.btn_micro.setObjectName("BtnMicro")
        self.btn_micro.setStyleSheet("""
            QPushButton#BtnMicro {
                background-color: #99ee44;
                border-radius: 17px;
                font-size: 14px;
                font-family: Roboto;
                font-weight: bold;
            }

            QPushButton#BtnMicro:hover {
                background-color: #59a30f;
            }
        """)
        self.btn_micro.setFixedSize(35, 35)
        self.btn_micro.setText("J")
        self.btn_micro.setCheckable(True)
        self.btn_micro.clicked.connect(self.start_voice_assistant)

        # # Добавление элементов на downbar_frame
        self.downbar_frame.layout = QHBoxLayout()
        self.downbar_frame.layout.setContentsMargins(10, 0, 10, 0)
        self.downbar_frame.layout.addWidget(self.text_edit)
        self.downbar_frame.layout.addWidget(self.btn_micro)
        self.downbar_frame.setLayout(self.downbar_frame.layout)

        # Установка выравнивания виджета вверху
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(0)
        # Добавление дочернего виджета в компоновщик
        self.layout.addWidget(self.upbar_frame)
        self.layout.addWidget(self.textbox_frame)
        self.layout.addWidget(self.downbar_frame)
        # Установка компоновщика для родительского виджета
        self.setLayout(self.layout)
