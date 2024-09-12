        
class BaseExecutor:
    def __init__(self, command: str=None):
        self.command = command
        
    def clean_commands(self, commands:list[str]) -> list[str]:
        n_commands = []
        for command in commands:
            n_commands.append(self._clean_command(command))
        
        return n_commands
            
        
    def run(self, verbose:bool=True,**kwargs):
        raise NotImplementedError('Implement run')        
        
    def __str__(self):
        return f"BaseExecuter(command={self.command})"
    
    def __repr__(self):
        return f"BaseExecuter(command={self.command})"        
    
    def _clean_command(self, command:str) -> str:
        # remove spaces
        command = command.strip()
        # remove ;
        command = command.rstrip(';')
        return command