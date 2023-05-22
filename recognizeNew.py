import functions as f
import tts
# № для машинного обучения
import words
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
#! КОМАНДЫ И ИХ РАБОТА ! КОМАНДЫ И ИХ РАБОТА ! КОМАНДЫ И ИХ РАБОТА ! КОМАНДЫ И ИХ РАБОТА ! КОМАНДЫ И ИХ РАБОТА !


def do_this_command(request_result, vectorizer, clf):
    trg = words.TRIGGERS.intersection(request_result.split())
    # # удаление имя бота
    try:
        request_result = request_result.replace(list(trg)[0], '')
    except:
        """"""
    # # формирование запроса пользователя
    text_vector = vectorizer.transform([request_result]).toarray()[0]
    answer = clf.predict([text_vector])[0]

    func_name = answer.split()[0]
    if ((request_result != '') & (answer == 'passive ')):
        tts.va_speak("Я вас не понял, повторит е")
    else:
        try:
            tts.va_speak(answer.replace(func_name, ''))
        except:
            """"""

    exec('f.'+func_name + '()')
    # *Cписок команд


def say_message(message):
    match message.split():
        case["привет"]: tts.va_speak('Привет')
        case["подкинь"]: f.flip_coin()
        case["спой"]: f.sing_songs()
        case["открой"]: f.open_programs()
        case["создай"]: f.create_txt()
        case["удали"]: f.delete_txt()
        case["прочитай"]: f.read_txt()
        case["перепиши"]: f.rewrite_txt()
        case["напиши"]: f.write_txt()
        case["список"]: f.commands_print()
        case["пока"]: tts.va_speak('пока-пока')

# *Действия команд

# # ОСНОВНАЯ ЧАСТЬ ПРОГРАММЫ # ОСНОВНАЯ ЧАСТЬ ПРОГРАММЫ # ОСНОВНАЯ ЧАСТЬ ПРОГРАММЫ # ОСНОВНАЯ ЧАСТЬ ПРОГРАММЫ #


def main():
    print("Чтобы начать скажите: Джарвис")
    print("Список команд:")
    for i in range(len(f.command_list)):
        print(f.command_list[i]+' - '+f.discription_list[i])
    # # передача образцов фраз, чтобы найти закономерность
    vectorizer = CountVectorizer()
    vectors = vectorizer.fit_transform(list(words.data_set.keys()))

    # # передача образцов фраз для ответа бота
    clf = LogisticRegression()
    clf.fit(vectors, list(words.data_set.values()))

    # # освобождение оперативной памяти
    del words.data_set
    while True:
        print("...")
        last_command = ''

        command = f.listen_command()
        trg = words.TRIGGERS.intersection(command.split())

        if trg:
            tts.va_speak('привет')
            tts.va_speak('Слушаю вас')
            print("Слушаю вас...")
            while True:

                if ("пока" in last_command) or ("пока-пока" in last_command) or ("аривилерчи" in last_command) or ("выключись" in last_command) or ("отключись" in last_command):
                    break

                command = f.listen_command()
                print("Прошлая команда:" + last_command)
                last_command = command
                print("Вы сказали:" + command)
                do_this_command(command, vectorizer, clf)

        elif 'пока' in command:
            tts.va_speak('до свидания')
            break
        else:
            print()


main()
