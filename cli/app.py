# cli/app.py
# Objective: Implements the CLI application using a library like Click or argparse
import os
from core.basellm import BaseLLM, LLMConfig
from core.executor.base_executor import BaseExecutor
from core.bashcode import BashCode, BashCodeRun, CodeReport
from llms import LitellmLLM, GroqLLM, OllamaLLM, get_model_class, extract_model_class_and_model_name
from core.executor.sequential_shell_executor import SequentialShellExecutor
from core.basepermission import Permission, UserChoice
from termcolor import colored
import subprocess
from core.prompts import SYSTEM_PROMPT
from llms.llmconfigs import configs

executor = SequentialShellExecutor()

models = [
        #groq
        'groq/llama3-groq-70b-8192-tool-use-preview',
        'groq/llama-3.1-8b-instant',
        'groq/gemma2-9b-it',
        'groq/llama-3.1-70b-versatile',
        'groq/llama3-8b-8192',
        'groq/llama3-70b-8192',
        'groq/llama-guard-3-8b',
        'groq/llama3-groq-8b-8192-tool-use-preview',
        'groq/mixtral-8x7b-32768',
        #ollama
        'ollama/gemma2:2b',
        'ollama/qwen2:1.5b',
        'ollama/qwen2:0.5b',
        #cerebras
        'cerebras/llama3.1-8b',
        'cerebras/llama3.1-70b',
        #google
        'google/gemini-1.5-flash',
        'google/gemini-1.5-pro',
        'google/gemini-1.0-pro',
        'google/gemini-1.5-pro-exp-0827',
        'google/gemini-1.5-flash-exp-0827',
        'google/gemini-1.5-flash-8b-exp-0827',
        'groq/llama3-8b-8192',
        'gemini/gemini-1.0-pro',
        #openrouter
        'openrouter/openai/gpt-3.5-turbo',
        'openrouter/openai/gpt-3.5-turbo-16k',
        'openrouter/openai/gpt-4',
        'openrouter/openai/gpt-4-32k', 
        'openrouter/anthropic/claude-2', 
        'openrouter/anthropic/claude-instant-v1', 
        'openrouter/google/palm-2-chat-bison', 
        'openrouter/google/palm-2-codechat-bison', 
        'openrouter/meta-llama/llama-2-13b-chat', 
        'openrouter/meta-llama/llama-2-70b-chat', 

    ]


def app(user_input:str=None, n_hist:int=2, model:str=models[-2]):
    # Get user input
    user_input = input(colored("Enter your command: ", "cyan")) if not user_input else user_input
    llm_config = LLMConfig(model_name=model)
    llm = TestLLM(config=llm_config)
    commands = llm.generate_response(user_prompt=user_input, n_hist=n_hist)
    output = command_execute(commands=commands.stepwise_bash_code, executor=executor, ask_user=True)
    # print('got output')
    bashcoderun = parse_codereport_to_bashcoderun(bashcode=commands, outputs=output)
    # print('got coderun')
    
    if bashcoderun.error:
        # print('gor code error')
        handle_command_error(coderun=bashcoderun, llm=llm, depth=3)
    
    print('ending')
    return

def parse_codereport_to_bashcoderun(bashcode:BashCode, outputs:list[CodeReport]):
    return BashCodeRun(
        instructions=bashcode.instructions,
        modifications=bashcode.modifications,
        stepwise_bash_code=bashcode.stepwise_bash_code,
        warnings=bashcode.warnings,
        permission_required=bashcode.permission_required,
        logs=outputs
    )

def handle_command_error(coderun:BashCodeRun, llm:BaseLLM,  depth=3):
    user_input_modify = str(input("Modify instructions:(rewrite prompt to modify code / press 'Enter' to skip but will regenerate / press 'q' to Quit) \n: "))
    
    if user_input_modify.lower()=='q' or depth<=0:
        return
    
    coderun.modifications = user_input_modify
    command_fix=llm.fix_error(coderun=coderun)
    output_fix = command_execute(commands=command_fix.stepwise_bash_code, executor=executor, ask_user=True)
    coderun_fix = parse_codereport_to_bashcoderun(bashcode=command_fix, outputs=output_fix)
    
    depth -= 1
    if coderun_fix.error:
        handle_command_error(
            coderun=coderun_fix,
            llm=llm,
            depth=depth 
        )
        return
        

def command_execute(commands:list[str],executor:BaseExecutor,  ask_user:bool=True):
    permission = Permission(commands=commands)
    user_choice = permission.run() if ask_user else UserChoice.YES
    if user_choice == UserChoice.YES:
        results =  executor.run(commands=commands, verbose=True)
        command, stdout, stderr, exit_code = results
        code_logs = []
        code_logs.append(CodeReport(code=command,run=True, stderr=stderr, stdout=stdout))
        
        
        return code_logs
        
    else:
        print(colored("Command execution cancelled.", "yellow"))
        return None, None