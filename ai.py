import requests
import json

# Replace with your OpenRouter API key
API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def get_ai_response(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "z-ai/glm-4.5-air:free",  # You can change the model
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
        if user_input.lower() == "quit":
            break
        response = get_ai_response(user_input)
        print("\nAI Response:")
        print(response)
        print()

if __name__ == "__main__":
    main()