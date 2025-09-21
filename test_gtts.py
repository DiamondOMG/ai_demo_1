from gtts import gTTS
import os

def text_to_speech(text, lang='th', output_file='output.mp3'):
    # สร้าง object gTTS
    tts = gTTS(text=text, lang=lang, slow=False)
    
    # บันทึกไฟล์เสียง
    tts.save(output_file)
    
    # เล่นไฟล์เสียง (สำหรับ Windows)
    os.system(f'start {output_file}')

# ตัวอย่างการใช้งาน
if __name__ == "__main__":
    text = "เปิด top แจ้งวัฒนะเรียบร้อยแล้วครับ"
    text_to_speech(text, lang='th')  # ใช้ภาษาไทย