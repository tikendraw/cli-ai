import os
import json

config_folder = os.path.expanduser("~/.config/cliai")
os.makedirs(config_folder, exist_ok=True)

config_file = os.path.join(config_folder, "config.json")
history_file = os.path.join(config_folder, "history.jsonl")


config_dict = {
    "default_model": "openai/gpt-3.5-turbo",
    "api_key": None,
    "ask_user": "always",  # always, never, sometimes (only when llms suggest it)
    "retry_generation": 3,  # number of times to retry generation
}

if not os.path.exists(config_file):
    with open(config_file, "w") as f:
        f.writelines(json.dumps(config_dict, indent=2))
