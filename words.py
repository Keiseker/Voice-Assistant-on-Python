TRIGGERS = {'джарвис'}


data_set = {
    '': 'passive ',
    ' ': 'passive ',
    # # общие фразы для диалога
    'привет': 'passive и тебе привет',
    'хай': 'passive привет-привет',
    'здравствуй': 'passive привет',
    # # погода
    'какая погода': 'choose_city сейчас скажу',
    'какая погода на улице': 'choose_city боишься замерзнуть?',
    'что там на улице': 'choose_city сейчас гляну...',
    'сколько градусов': 'choose_city можешь выглянуть в окно, но сейчас проверю',
    # # подкинь монетку
    'подкинь': 'flip_coin сейчас подкину',
    'подбрось': 'flip_coin сейчас подброшу',
    'подкинь монетку': 'flip_coin сейчас подкину',
    'подбрось монетку': 'flip_coin сейчас подброшу',
    # # справка
    'что ты умеешь?': 'commands_print сейчас расскажу',
    'какой твой функционал': 'commands_print сейчас расскажу',
    'что ты можешь?': 'commands_print сейчас расскажу',
    'какие у тебя команды?': 'commands_print сейчас расскажу',
    # # отключение бота
    'отключись': 'passive отключаюсь',
    'выключись': 'passive выключаюсь',

    # # общие фразы для диалога
    'как у тебя дела': 'passive работаю в фоне, не переживай',
    'что делаешь': 'passive жду очередной команды, хоть мог бы и сам на кнопку нажать',
    'расскажи анекдот': 'passive Вчера помыл окна, теперь у меня рассвет на два часа раньше...',
    'работаешь': 'passive как видишь',
    'ты тут': 'passive вроде да',
    'что ты умеешь': 'passive я умею узнавать погоду, могу открыть браузер, запустить exe файл, выключить пк, отключиться, рассказать анекдот и еще тому чему ты меня научишь',


}