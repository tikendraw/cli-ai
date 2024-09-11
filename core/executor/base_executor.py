# core/baseexecuter.py
# Objective: Implements the BaseExecuter class for handling execution of commands and prints output

from typing import List, Optional
from termcolor import colored
import subprocess

        
class BaseExecutor:
    def __init__(self, command: str=None):
        self.command = command
        
        
    def run(self, verbose:bool=True,**kwargs):
        raise NotImplementedError('Implement run')        
        
    def __str__(self):
        return f"BaseExecuter(command={self.command})"
    
    def __repr__(self):
        return f"BaseExecuter(command={self.command})"        