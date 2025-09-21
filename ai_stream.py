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

def process_ai_response(prompt, response_queue):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-oss-20b:free",
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
    }

    # ส่งเวลาเริ่มต้น
    response_queue.put({
        "type": "start",
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
    })

    with requests.post(API_URL, headers=headers, json=data, stream=True) as r:
        for chunk in r.iter_content(chunk_size=1024):
            chunk = chunk.decode("utf-8")
            buffer = chunk
            while True:
                line_end = buffer.find("\n")
                if line_end == -1:
                    break

                line = buffer[:line_end].strip()
                buffer = buffer[line_end + 1:]

                if line.startswith("data: "):
                    data_str = line[6:]
                    if data_str == "[DONE]":
                        # ส่งสัญญาณว่าเสร็จสิ้น
                        response_queue.put({
                            "type": "done",
                            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
                        })
                        return

                    try:
                        data_obj = json.loads(data_str)
                        content = data_obj["choices"][0]["delta"].get("content")
                        if content:
                            # ส่งเนื้อหาผ่านคิว
                            response_queue.put({
                                "type": "content",
                                "text": content,
                                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
                            })
                    except json.JSONDecodeError:
                        pass