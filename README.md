
# Natural Language CLI

# cli-ai

### Installation
```bash
pip install cliai
```

### Configuration
- Set the default model to use
Based on Litellm , so most of the models are supported (https://github.com/BerriAI/litellm)
```bash
cli config default_model <model_name>
```

- Set the default ask user behavior
  - always # ask user always
  - never  # ask user never
  - sometimes # ask user when llms suggests to ask
```bash
cli config ask_user <always|never|sometimes>
```

- Set the retry if generation fails
```bash
cli config retry_generation <number>
```
### Usage
1. Make call through the cli command
```bash
cli run 'kill the chrome' --model cerebras/llama3.1-70b
```
or 
```bash
ci 'convert this.mp4  to 720p and remove the audio' --model openai/gpt-3.5-turbo
```

2. If error happens, you can fix it with the following command
error-report takes account of the last command it executed, so it will fix the error with the last command
```bash
ci ' also change flip the video' --model openai/gpt-3.5-turbo --error-report
```

# Recommended models
- cerebras (https://github.com/cerebras) #fastest model inference in the world on llama3.1-70b
- groq (https://github.com/simonw/groq) # 2nd Fastest model inference