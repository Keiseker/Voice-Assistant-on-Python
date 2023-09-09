import torch
import sounddevice as sd
import time

language = 'ru'
model_id = 'ru_v3'
sample_rate = 48000
speaker = 'kseniya'
put_accent = True
put_yo = True
device = torch.device('cpu')  # cpu или gpu


model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language=language,
                          speaker=model_id)
model.to(device)

ssml_sample = """
              <speak>
              <p>
                <s>Привет, я голосовой ассистент Ева!</s>
                <s>Я могу принять решение за вас, подкинув монетку, рассказать анекдот,<break time="300ms"/> найти нужный сайт или видео.</s>
                <s>Приятно с вами познакомиться!</s>
              </p>
              </speak>
              """

# синтез речи
text = "Привет, я голосовой ассистент Ева! Я могу принять решение за вас, подкинув монетку, рассказать анекдот, найти нужный сайт или видео. Приятно с вами познакомиться!"


def va_speak(text):
    text = text.split()
    ssml_sample = "<speak><s>"
    for i in text:
        if (i[len(i)-1] == '!') or (i[len(i)-1] == '.') or (i[len(i)-1] == '?'):
            ssml_sample += ' ' + i+'</s>'+'<s>'
        elif (i[len(i)-1] == ',' or i[len(i)-1] == ':'):
            ssml_sample += ' ' + i + '<break time="300ms"/>'
        else:
            ssml_sample += ' '+i
    ssml_sample = ssml_sample[:len(ssml_sample)-3]
    ssml_sample += "</speak>"
    audio = model.apply_tts(ssml_text=ssml_sample,
                            speaker=speaker,
                            sample_rate=sample_rate,
                            put_accent=put_accent,
                            put_yo=put_yo)

    sd.play(audio, sample_rate * 1.05)
    time.sleep((len(audio) / sample_rate) + 0.5)
    sd.stop()
