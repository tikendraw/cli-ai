# CLI-Agent
Talk to cli-agent and it will help you to write bash code to solve your problem.
### Installation
```bash
pip install cli-agent
```

### Configuration
- Set the default model to use. 

Based on Litellm , so most of the models are supported (https://github.com/BerriAI/litellm)
```bash
cli config default_model <model_name>
```

- Set the default ask user behavior, when code is about to run it asks user if he wants to run it or not
  - always      # ask user always
  - never       # ask user never
  - sometimes   # ask user when llms suggests to ask
```bash
cli config ask_user <always|never|sometimes>
```

- Set the retry if generation fails
```bash
cli config retry_generation <number>
```
### Usage
Commands:

cli : main cli command
ci : direct chat with cli


1. Make call through the cli command
```bash
cli run 'kill the chrome' --model cerebras/llama3.1-70b
```
or 
```bash
ci 'convert this.mp4  to 720p and remove the audio' 
```

2. If error happens, you can fix it with the following command.

Error-report takes account of the last command it executed, so it will fix the error with the last command
```bash
ci ' also flip the video' --model openai/gpt-3.5-turbo --error-report
```

### command line interface
```bash
$ cli --help
Usage: cli [OPTIONS] COMMAND [ARGS]...

  CLI AI: Natural Language Command Line Interface

Options:
  --help  Show this message and exit.

Commands:
  config  View or set configuration values
  run     Run the main CLI AI application

$ cli run --help

Usage: cli run [OPTIONS] [USER_INPUT]...

  Run the main CLI AI application

Options:
  --n-hist INTEGER             Number of history items to consider
  --model TEXT                 Model name to use
  -er, --error-report BOOLEAN  Fix the last error with current modifications
  --help                       Show this message and exit.

```

### Recommended models
- cerebras (https://github.com/cerebras) #fastest model inference in the world on llama3.1-70b
- groq (https://github.com/simonw/groq) # 2nd Fastest model inference