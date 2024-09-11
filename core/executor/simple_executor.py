# core/baseexecuter.py
# Objective: Implements the BaseExecuter class for handling execution of commands and prints output

from typing import List, Optional
from termcolor import colored
import subprocess
from .base_executor import BaseExecutor
        
class SimpleExecutor(BaseExecutor):
    def __init__(self, command: str=None):
        self.command = command
        
        
    def run(self, verbose:bool=True,**kwargs):
        """ returns output and eror  as tuple, if sucess shell output and none else shell output and error"""
        self.command = kwargs.get('command', self.command)
        self._verbose = kwargs.get('verbose', False)
        
        if self.command is None:
            raise ValueError("Command is not set")
        try:
            out = subprocess.run(self.command, shell=True, check=True, capture_output=True, text=True)
            if verbose:
                print(colored(out.stdout, 'green'))
            return out, None
        except subprocess.CalledProcessError as e:
            if verbose:
                print(colored(e.stdout, 'red'))
                print(colored(e.stderr, 'red'))
            return e.stdout, e.stderr
        except Exception as e:
            raise e
        
        
    def __str__(self):
        return f"BaseExecuter(command={self.command})"
    
    def __repr__(self):
        return f"BaseExecuter(command={self.command})"        