import pvporcupine
import sounddevice as sd
import numpy as np
from click import click_center_screen

# กำหนด AccessKey ของคุณ
ACCESS_KEY = '2y1dzvmFcGA9iYAibaEOYF+WapB23vkO3h/AO+Kw4J2lg8OaJ/D+IQ=='

# กำหนด wake word ที่ต้องการตรวจจับ
keywords = ['bumblebee']

# สร้าง instance ของ Porcupine
porcupine = pvporcupine.create(
    access_key=ACCESS_KEY,
    keywords=keywords,
    sensitivities=[0.7] 
)

# กำหนด sample rate และ frame length
SAMPLE_RATE = 16000
FRAME_LENGTH = porcupine.frame_length

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    pcm = (indata * 32767).astype(np.int16).flatten()
    keyword_index = porcupine.process(pcm)
    if keyword_index >= 0:
        click_center_screen()

# เริ่มต้นการบันทึกเสียง
with sd.InputStream(callback=audio_callback, channels=1, samplerate=SAMPLE_RATE, blocksize=FRAME_LENGTH):
    print("Listening for wake word...")
    input()  # รอให้ผู้ใช้กด Enter เพื่อหยุด