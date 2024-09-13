import requests
import json

# https://www.arliai.com/quick-start

url = "https://api.arliai.com/v1/chat/completions"

payload = json.dumps({
  "model": "Meta-Llama-3.1-8B-Instruct",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"},
    {"role": "assistant", "content": "Hi!, how can I help you today?"}
  ],
  "repetition_penalty": 1.1,
  "temperature": 0.7,
  "top_p": 0.9,
  "top_k": 40,
  "max_tokens": 1024,
  "stream": True
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': f"Bearer {ARLIAI_API_KEY}"
}

response = requests.request("POST", url, headers=headers, data=payload)