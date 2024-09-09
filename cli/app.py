# cli/app.py
# Objective: Implements the CLI application using a library like Click or argparse
import os
print(os.getcwd())
from llms import TestLLM, GroqLLM, OllamaLLM
from core.baseexecuter import BaseExecuter
from core.basepermission import Choice, UserChoice
from termcolor import colored
import subprocess


def app():
    # Get user input
    user_input = input(colored("Enter your command: ", "cyan"))
    # llm = OllamaLLM(model_name="qwen2:1.5b")  # Replace with actual model name    
    llm = GroqLLM(api_key=os.getenv("GROQ_API_KEY"), model_name="llama3-8b-8192")
    command = llm.generate_response(user_prompt=user_input, n_hist=0)
    result = command_execute(command=command, ask_user=True)
    handle_command_error(result=result, previous_user_input=user_input, command=command, llm=llm, depth=3)
    return


def handle_command_error(result, previous_user_input, command, llm,  depth=3):
    if isinstance(result, subprocess.CalledProcessError):
        user_input_modify = str(input("Modify instructions:(rewrite prompt to modify code / press 'Enter' to skip but will regenerate / press 'q' to Quit)"))
        
        if user_input_modify.lower()=='q' or depth<=0:
            return
        
        command_fix=llm.fix_error(previous_user_prompt=previous_user_input, command=command, error=result.stderr, modifications=user_input_modify)
        result_fix = command_execute(command=command_fix, ask_user=True)
        depth -= 1
        handle_command_error(
            result_fix, 
            previous_user_input=f"{previous_user_input} {user_input_modify}",
            command=command_fix,
            llm=llm,
            depth=depth
        )
        return
    return
        


def command_execute(command:str, ask_user:bool=True):
    choice = Choice(command=command)
    user_choice = choice.run() if ask_user else UserChoice.YES

    if user_choice == UserChoice.YES:
        # Execute command
        executer = BaseExecuter(command)
        result = executer.run(verbose=True)
        return result
    else:
        print(colored("Command execution cancelled.", "yellow"))
        return None