import requests
import json
import time
# Replace with your OpenRouter API key
API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def get_ai_response(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "openai/gpt-oss-20b:free",  # You can change the model
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

def main():
    while True:
        user_input = input("Enter your prompt (or 'quit' to exit): ")
        input_time = time.strftime("%Y-%m-%d %H:%M:%S")
        print(input_time)
        if user_input.lower() == "quit":
            break
        response = get_ai_response(user_input)
        print("\nAI Response:")
        print(response)
        output_time = time.strftime("%Y-%m-%d %H:%M:%S")
        print(output_time)
        print()

if __name__ == "__main__":
    main()