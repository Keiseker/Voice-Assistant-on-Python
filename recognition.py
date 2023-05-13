import queue
import sounddevice as sd
import vosk


q = queue.Queue()

# ? device - используем девайс по умолчанию
device = sd.default.device
# ? samplerate - частота дискретизации(сколько раз в секунду микро замеряет шум)
samplerate = int(sd.query_devices(device[0], 'input')['default_samplerate'])
model = vosk.Model('vosk_model_small')


def callback(indata, frames, time, status):
    q.put(bytes(indata))


# ? blocksize - размер информации, который отдается за 1 раз
with sd.RawInputStream(samplerate=samplerate, blocksize=16000, device=device[0],
                       dtype="int16", channels=1, callback=callback):

    rec = vosk.KaldiRecognizer(model, samplerate)
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            print(rec.Result())
        else:
            print(rec.PartialResult())
