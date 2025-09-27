# ai_stream.py อย่าลบ
import requests
import json
import time
import os
from dotenv import load_dotenv

# โหลด environment variables
load_dotenv()

# ดึง API key จาก environment variable
API_KEY = os.getenv('OPENROUTER_API_KEY')
if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in environment variables")

API_URL = "https://openrouter.ai/api/v1/chat/completions"

model = "x-ai/grok-4-fast:free"

# โหลดรายชื่อโมเดลจากไฟล์ config/model_ai.json (ลำดับสำรอง model_1 -> model_2 -> ...)
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "model_ai.json")
SYSTEM_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "system_ai.json")

def load_models_from_config():
    models = []
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        keys = [k for k in cfg.keys() if k.startswith("model_")]
        keys.sort(key=lambda k: int(k.split("_")[1]) if k.split("_")[1].isdigit() else 9999)
        for k in keys:
            v = cfg.get(k)
            if isinstance(v, str) and v.strip():
                models.append(v.strip())
    except Exception:
        pass
    if not models:
        models.append("x-ai/grok-4-fast:free")
    return models

# โหลด system prompt จากไฟล์ config/system_ai.json
def load_system_prompt():
    try:
        with open(SYSTEM_CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        s = cfg.get("system", "")
        if isinstance(s, str):
            return s.strip()
    except Exception:
        pass
    return ""

# รายการโมเดลที่จะลองใช้งานตามลำดับ
MODELS = load_models_from_config()
SYSTEM_PROMPT = load_system_prompt()

def process_ai_response(prompt):
    print("เริ่มส่งคำถาม:", time.strftime('%Y-%m-%d %H:%M:%S'))
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response_text = ""
    last_error = None

    # ลองใช้โมเดลตามลำดับ หากล้มเหลวจะสลับไปโมเดลถัดไปอัตโนมัติ
    for m in MODELS:
        try:
            messages = []
            if SYSTEM_PROMPT:
                messages.append({"role": "system", "content": SYSTEM_PROMPT})
            messages.append({"role": "user", "content": prompt})

            data = {
                "model": m,
                "messages": messages,
                "stream": False,
            }

            response = requests.post(API_URL, headers=headers, json=data, timeout=60)
            response.raise_for_status()

            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                response_text = result["choices"][0]["message"]["content"]
                print(f"สำเร็จด้วยโมเดล: {m}")
                print("AI ตอบเสร็จ:", time.strftime('%Y-%m-%d %H:%M:%S'))
                return response_text

            # หาก API ตอบกลับโดยไม่มี choices ให้ถือว่าล้มเหลวและลองโมเดลถัดไป
            if "error" in result:
                last_error = result.get("error")
                print(f"โมเดลล้มเหลว: {m} -> {last_error}")
            else:
                last_error = f"No choices returned for model {m}"
                print(f"โมเดลล้มเหลว: {m} -> ไม่มีผลลัพธ์")
        except Exception as e:
            last_error = str(e)
            print(f"โมเดลล้มเหลว: {m} -> {e}")
            continue

    # หากลองทุกโมเดลแล้วไม่สำเร็จ ให้ส่งข้อความแจ้งผู้ใช้แทนการโยน exception เพื่อไม่ให้ระบบล่ม
    print("AI ตอบเสร็จ (ล้มเหลวทุกโมเดล):", time.strftime('%Y-%m-%d %H:%M:%S'))
    return f"ขออภัย ระบบไม่สามารถติดต่อโมเดลได้ในขณะนี้ (สาเหตุ: {last_error})"

if __name__ == "__main__":
    # ทดสอบฟังก์ชัน
    test_prompt = "อากาศที่ประเทศไทยกี่องศาครับ ตอบสั้นๆ"
    print("ทดสอบ AI Response:")
    print(f"Prompt: {test_prompt}")
    print("-" * 50)

    try:
        ai_response = process_ai_response(test_prompt)
        print("AI Response:")
        print(ai_response)
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
        