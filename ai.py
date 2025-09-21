import requests
import json
import time

API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def stream_ai_response(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-oss-20b:free",
        "messages": [{"role": "user", "content": prompt}],
        "stream": True,
    }

    with requests.post(API_URL, headers=headers, json=data, stream=True) as r:
        for line in r.iter_lines(decode_unicode=True):
            if not line or not line.startswith("data: "):
                continue

            data_str = line[6:]
            if data_str == "[DONE]":
                return

            try:
                data_obj = json.loads(data_str)
                content = data_obj["choices"][0]["delta"].get("content")
                if content:
                    print(content, end="", flush=True)
            except json.JSONDecodeError:
                pass


def main():
    while True:
        user_input = input("\nEnter your prompt (or 'quit' to exit): ")
        if user_input.lower() == "quit":
            break
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] AI Response:\n")
        stream_ai_response(user_input)
        print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Done.\n")

if __name__ == "__main__":
    main()
