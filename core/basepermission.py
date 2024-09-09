# core/basepermission.py
# Objective: Implements the BasePermission class for handling permissions
# use enum for permission types, this class should ask for permission from the user, and store the permission as enum

from enum import Enum
from pickle import NONE
from termcolor import colored

class UserChoice(Enum):
    YES = "yes"
    NO = "no"
    
class Choice:
    def __init__(self, command: str):
        self.choice = None
        self.command = command

    def ask_for_permission(self):
        
        print(colored(f"Command : {self.command}", 'blue'))
        choice = input(colored("Do you want to proceed? (yes/no): ", 'red'))

        if str(choice).lower() in ["yes", 'y', 'Y', 'Yes', 'YES']:
            self.choice = UserChoice.YES
        else:
            self.choice = UserChoice.NO

    def run(self, **kwargs):
        self.command = kwargs.get('command', self.command)
        self.ask_for_permission()
        return self.choice

    def get_choice(self) -> UserChoice:
        return self.choice
    
    def get_command(self) -> str:
        return self.command
