import requests

url = "http://localhost:11434/api/chat"

payload = {
    "model": "qwen",
    "messages": [
        {"role": "user", "content": "Hello, from my python environment!"}
    ],
    "stream": False
}

response = requests.post(url, json=payload)

# convert JSON response into Python dict
data = response.json()

# print ONLY the AI response
print(data["message"]["content"])