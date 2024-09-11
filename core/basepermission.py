
from enum import Enum
from pickle import NONE
from termcolor import colored

class UserChoice(Enum):
    YES = "yes"
    NO = "no"
    
class Permission:
    def __init__(self, commands: list[str]):
        self.choice = None
        self.commands = commands

    def ask_for_permission(self):
        
        print(colored(f"Command : {self.commands}", 'blue'))
        choice = input(colored("Do you want to proceed? (yes/no): ", 'red'))

        if str(choice).lower() in ["yes", 'y', 'Y', 'Yes', 'YES']:
            self.choice = UserChoice.YES
        else:
            self.choice = UserChoice.NO

    def run(self, **kwargs):
        self.commands = kwargs.get('commands', self.commands)
        self.ask_for_permission()
        return self.choice

    def get_choice(self) -> UserChoice:
        return self.choice
    
    def get_command(self) -> str:
        return self.commands
