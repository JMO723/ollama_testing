# Project Structure

```text
ollama_testing/
├── ollama_test.py      # A program that makes a call to a specific model (qwen) saying hello
├── ollama_client.py    # Defines how we communicate with our AI model
├── app.py              # Shows available log files and prompts user to choose one to analyze
└── logs/
    ├── test.log
    └── test2_no_oom.log
