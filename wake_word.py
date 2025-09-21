import pvporcupine
import sounddevice as sd
import numpy as np

ACCESS_KEY = '2y1dzvmFcGA9iYAibaEOYF+WapB23vkO3h/AO+Kw4J2lg8OaJ/D+IQ=='
keywords = ['bumblebee']

porcupine = pvporcupine.create(
    access_key=ACCESS_KEY,
    keywords=keywords,
    sensitivities=[0.7]
)

SAMPLE_RATE = 16000
FRAME_LENGTH = porcupine.frame_length

def start_listening(event_queue=None):
    def audio_callback(indata, frames, time, status):
        if status:
            print(status)
        pcm = (indata * 32767).astype(np.int16).flatten()
        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            print("Wake word detected!")
            if event_queue is not None:
                event_queue.put("detected")

    with sd.InputStream(
        callback=audio_callback,
        channels=1,
        samplerate=SAMPLE_RATE,
        blocksize=FRAME_LENGTH,
    ):
        print("🎤 Listening for wake word... (press Ctrl+C to stop)")
        while True:
            sd.sleep(1000)
