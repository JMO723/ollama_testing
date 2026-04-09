import requests

URL = "http://localhost:11434/api/chat"
MODEL = "qwen"

SCHEMA = {
    "type": "object",
    "properties": {
        "summary": {"type": "string"},
        "confirmed_errors": {
            "type": "array",
            "items": {"type": "string"}
        },
        "warnings": {
            "type": "array",
            "items": {"type": "string"}
        },
        "security_events": {
            "type": "array",
            "items": {"type": "string"}
        },
        "possible_causes": {
            "type": "array",
            "items": {"type": "string"}
        },
        "recommended_next_steps": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": [
        "summary",
        "confirmed_errors",
        "warnings",
        "security_events",
        "possible_causes",
        "recommended_next_steps"
    ]
}


def ask_ollama(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a Linux log analysis assistant. "
                    "Return concise, accurate findings only. "
                    "Do not invent facts. "
                    "Do not copy raw log lines into possible_causes unless explicitly asked."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "stream": False,
        "format": SCHEMA,
        "options": {
            "temperature": 0
        }
    }

    response = requests.post(URL, json=payload, timeout=120)
    response.raise_for_status()

    data = response.json()
    return data["message"]["content"]