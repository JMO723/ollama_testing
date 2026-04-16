# Project Goals

  The goal of this project is to understand how to communicate/interact with an AI model on my local machine, as well as to understand the concept of parameters and how they affect responses from AI models. To accomplish this goal, a Linux log analyzer program was created. The program would ask an AI model (qwen/qwen2.5:7b) to analyze the text and provide an actionable response to the user. I started this project in python, but had to use Google Colab in order to run the qwen:7b model. 

# Project Structure

```text
ollama_testing/
    ├── ollama_test.py      # A test program that makes a call to a specific model (qwen) saying hello
    ├── ollama_client.py    # Defines how we communicate with our AI model 
    ├── app.py              # Shows available log files and prompts user to choose one to analyze
    └── logs/
        ├── test.log
        └── test2_no_oom.log

ollama_test_qwen7b_colab_test/
    ├── colab_ollama_log_analyzer.ipynb    #Accomplishes the same task as the files in ollama_testing by using Google Colab. My local machine does not suffice to run a 7b parameter model, Colab allows us to see the differences in a response from qwen vs qwen:7b. 

```
# Model Responses

The different responses from our implementations highlight the importance of hardware resources and models with more parameters. While developing the Python implementation, all testing was performed on my local machine. Even with a 12th Gen Intel(R) Core processor and 8 GB of RAM, I was only able to run smaller models reliably, and larger models were difficult or impossible to use effectively. Google Colab allowed me to implement a larger model because the virtual hardware resources were dedicated to that single task. This, in turn, resulted in better responses, as the model had more parameters. A parameter can be thought of as a weight in a neural network; increasing the number of parameters provides more connections, more learned patterns, and more ways to model relationships within the data.

There are also several minor differences between the two implementations. The Google Colab version used a reduced log size (max_chars = 4000) and an increased timeout (timeout = 600). The reduced log size helped keep responses more focused, while the increased timeout ensured that the model had enough time to generate a complete response. Additionally, Colab uses the official Python wrapper for Ollama when making requests (response = ollama.chat(...)), which improves reliability when handling structured JSON output.

When examining the responses from the Python implementation, it is clear that the model tends to copy text directly from the log file rather than abstracting meaningful insights. The response is limited in the information it provides and does not offer many actionable solutions. In contrast, the Colab implementation is able to extract deeper meaning from the log data and provide more useful, actionable recommendations (although the Colab code itself can still be further refined).

**Python implementation**
![App Response](ollama_personal_test/ollama_qwen_run_response_image/ollama_run.png)

**Google Colab implementation**
![App Response](ollama_test_qwen7b_colab_test/ollama_qwen7b_run_response_image/ollama_run_7b.png)

