# Project Goals

The goal of this project is to understand how to communicate/interact with an AI model on my local machine, as well as to understand the concept of parameters and how they affect responses from AI models. To accomplish this goal, a Linux log analyzer program was created. The program would ask an AI model (qwen/qwen:7b) to analyze the text and provide an actionable response to the user. I started this project in python, but had to use Google Colab in order to run the qwen:7b model. 

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
    ├── Junaid_ollama_log.ipynb    #Accomplishes the same task as the files in ollama_testing by using Google Colab. My local machine does not suffice to run a 7b parameter model, Colab allows us to see the differences in a response from qwen vs qwen:7b. 
