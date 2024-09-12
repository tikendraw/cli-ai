import subprocess
from typing import List, Tuple
from termcolor import colored
from .base_executor import BaseExecutor
import os

class SequentialShellExecutor(BaseExecutor):
    def __init__(self):
        self.shell = "/bin/bash"

    def run(self, commands: List[str], verbose: bool = True) -> Tuple[str, str, str, int]:
        env = {}  # To maintain environment changes between commands

        commands = self.clean_commands(commands=commands)
        command = '&&'.join(commands) # && to join so if a command fails other commands don't get executed
        # for command in commands:
        try:
            process = subprocess.Popen(
                f"{command}; echo $?",
                shell=True,
                executable=self.shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env={**os.environ, **env}
            )

            stdout, stderr = process.communicate()
            
            output_lines = stdout.strip().split('\n')
            if output_lines and output_lines[-1].isdigit():
                exit_code = int(output_lines[-1])
                stdout = '\n'.join(output_lines[:-1])
            else:
                exit_code = process.returncode  # Use the process's return code if available
                stdout = '\n'.join(output_lines)  # Keep all lines if no exit code is found

            if verbose:
                if stdout:
                    print(colored(stdout, 'white'))
                if stderr:
                    print(colored(stderr, 'white'))
                print(colored(f"Exit code: {exit_code}", 'yellow'))

            return command, stdout, stderr, exit_code

        except Exception as e:
            if verbose:
                print(colored(f"Error executing command '{command}': {str(e)}", 'red'))
            return command, "", str(e), -1

    def _parse_env_changes(self, output: str) -> dict:
        """Parse the output for any environment variable changes."""
        env_changes = {}
        for line in output.split('\n'):
            if line.startswith('export '):
                parts = line.split('=', 1)
                if len(parts) == 2:
                    key = parts[0].split()[-1]
                    value = parts[1].strip("'\"")
                    env_changes[key] = value
        return env_changes
