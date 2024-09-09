
# config.py
# Objective: Stores configuration variables
# - Loads environment variables and provides a central place for app settings

from logging import config
import os

config_folder = os.path.expanduser("~/.config/cliai")
os.makedirs(config_folder, exist_ok=True)

history_file = os.path.join(config_folder, "history.jsonl")
