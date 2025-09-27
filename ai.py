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

def process_ai_response(prompt):
    print("เริ่มส่งคำถาม:", time.strftime('%Y-%m-%d %H:%M:%S'))
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }

    response_text = ""
    response = requests.post(API_URL, headers=headers, json=data)
    response.raise_for_status()

    result = response.json()
    if "choices" in result and len(result["choices"]) > 0:
        response_text = result["choices"][0]["message"]["content"]
    
    print("AI ตอบเสร็จ:", time.strftime('%Y-%m-%d %H:%M:%S'))
    return response_text

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
        