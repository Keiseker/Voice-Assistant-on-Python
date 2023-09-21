# Voice-Assistant-on-Python app for Windows
## О проекте
Это десктопное приложение голосового помощника на Python 3 с графическим интерефейсом, которое находится на стадии разработки.

На данный момень использованы следующие библиотеки:
* PyQt6 для создания графического интерфейса
* Scikit-Learn для машинного обучения
* TTS(Text-to-Speech) model Silero для синтеза речи
* Vosk для распознавания речи
* Threading для реализации многопоточности
  
  Остальные библиотеки были использованы для реализации конкретных функций в приложении.
  
## Реализованные функции
* офлайн распознавание и синтез речи (без учета использования функций, требующих подключение к интернету)
* "подбрасывание монетки"
* справка о возможностях голосового помощника
* воспроизведение анекдотов с [сайта](https://anekdotme.ru/anekdoti_aforizmi/)
* найти видео на youtube по вашему запросу
* найти сайт по вашему запросу
## Установка
Чтобы запустить голосового помощника на Python 3 необходимо:
1. Открыть эту папку или только файл main.py в вашей среде разработки.
2. В терминале запустить команду:
pip install -r requirements.txt
3. После установки всех зависимостей прописать в терминале команду:
python main.py
4. Далее 1 раз нажать на кнопку "Начать" и следовать инструкции на экране.
