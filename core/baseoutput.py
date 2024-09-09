# core/baseoutput.py
# Objective: Implements the BaseOutput class for handling output from LLMs

from .basemodel import BaseModel
from typing import List, Optional
from termcolor import colored

class BaseOutput(BaseModel):
    def __init__(self, output_type: str):
        self.output_type = output_type
        
    def run(self, **kwargs):
        print(colored(self.output_type, 'green'))