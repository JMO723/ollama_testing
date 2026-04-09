ollama_testing/
  ollama_test  # A program that makes a call to a specific model (qwen) saying hello 
  ollama_client # Defines how we communicate with our AI model
  app.py # Shows the user available log files and prompts them to choose which one to analyze (log files in log directory {test.log and test2_no_oom.log})



Current implementation is very shaky. Currently having issues with not having enough RAM to run models with more parameters as well as issues with creating a good promt for the AI
  
