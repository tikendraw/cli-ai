# cli/app.py
# Objective: Implements the CLI application using a library like Click or argparse
import os
from pprint import pprint
from core.basellm import BaseLLM, LLMConfig
from core.executor.base_executor import BaseExecutor
from core.bashcode import BashCode, BashCodeRun, CodeReport
import functools

from llms import LitellmLLM
from core.executor.sequential_shell_executor import SequentialShellExecutor
from core.basepermission import Permission, UserChoice
from termcolor import colored
import random
from core.prompts import ERROR_FIX_PROMPT

executor = SequentialShellExecutor()

models = {
    "groq": [
        "groq/llama3-groq-70b-8192-tool-use-preview",
        "groq/llama-3.1-8b-instant",
        "groq/gemma2-9b-it",
        "groq/llama-3.1-70b-versatile",
        "groq/llama3-8b-8192",
        "groq/llama3-70b-8192",
        "groq/llama-guard-3-8b",
        "groq/llama3-groq-8b-8192-tool-use-preview",
        "groq/mixtral-8x7b-32768",
    ],
    "ollama": [
        "ollama/gemma2:2b",
        "ollama/qwen2:1.5b",
        "ollama/qwen2:0.5b",
    ],
    "cerebras": [
        "cerebras/llama3.1-8b",
        "cerebras/llama3.1-70b",
    ],
    "google": [
        "gemini/gemini-1.5-flash",
        "gemini/gemini-1.5-pro",
        "gemini/gemini-1.0-pro",
        "gemini/gemini-1.5-pro-exp-0827",
        "gemini/gemini-1.5-flash-exp-0827",
        "gemini/gemini-1.5-flash-8b-exp-0827",
        "gemini/gemini-1.0-pro",
    ],
    "openrouter": [
        "openrouter/openai/gpt-3.5-turbo",
        "openrouter/openai/gpt-3.5-turbo-16k",
        "openrouter/openai/gpt-4",
        "openrouter/openai/gpt-4-32k",
        "openrouter/anthropic/claude-2",
        "openrouter/anthropic/claude-instant-v1",
        "openrouter/google/palm-2-chat-bison",
        "openrouter/google/palm-2-codechat-bison",
        "openrouter/meta-llama/llama-2-13b-chat",
        "openrouter/meta-llama/llama-2-70b-chat",
    ],
}


def get_model(
    provider: str = None, model_name: str = None, model_dict: dict = None
) -> str:
    provider = (
        provider
        if provider in model_dict.keys()
        else random.choice(list(model_dict.keys()))
    )
    model_name = (
        model_name
        if model_name in model_dict[provider]
        else random.choice(model_dict[provider])
    )
    return model_name


@functools.cache
def load_model(model: str):
    llm_config = LLMConfig(model_name=model)
    llm = LitellmLLM(config=llm_config)
    return llm


def handle_use_ask(a: str, permission_required: bool = True) -> bool:
    """a in [always, never, sometimes]"""
    a = a.strip().lower()

    if a == "always":
        return True
    elif a == "never":
        return False
    elif a == "sometimes":
        return permission_required


def app(
    user_input: str = None,
    n_hist: int = 2,
    model: str = None,
    error_report: bool = False,
    ask_user: str = True,
    n_try: int = 3,
):
    user_input = (
        input(colored("why you heya? : ", "cyan")) if not user_input else user_input
    )
    llm = load_model(model=model)

    if error_report:
        previous_coderuns = BashCodeRun(instructions="hi", logs=None).previous_runs()

        if previous_coderuns:
            last_bashcoderun = previous_coderuns[-1]
        else:
            print("No previous code runs found.")
            return

        last_bashcoderun.modifications = user_input

        user_input = format_error_fix_prompt(coderun=last_bashcoderun)
        n_hist = 2

    commands = llm.generate_response(user_prompt=user_input, n_hist=n_hist, n_try=n_try)

    output = command_execute(
        commands=commands.stepwise_bash_code,
        executor=executor,
        ask_user=handle_use_ask(
            a=ask_user, permission_required=commands.permission_required
        ),  # if commands.permission_required else False
    )
    bashcoderun = parse_codereport_to_bashcoderun(bashcode=commands, outputs=output)
    bashcoderun.write_log()

    return


def format_error_fix_prompt(coderun: BashCodeRun, **kwargs):
    user_prompt = ERROR_FIX_PROMPT.format(
        instructions=coderun.instructions,
        error_logs=coderun.logs[-1].model_dump_json(indent=4),
        modifications=coderun.modifications,
    )
    return user_prompt


def parse_codereport_to_bashcoderun(bashcode: BashCode, outputs: list[CodeReport]):
    return BashCodeRun(
        instructions=bashcode.instructions,
        modifications=bashcode.modifications,
        stepwise_bash_code=bashcode.stepwise_bash_code,
        warnings=bashcode.warnings,
        permission_required=bashcode.permission_required,
        logs=outputs,
    )


def command_execute(commands: list[str], executor: BaseExecutor, ask_user: bool = True):
    permission = Permission(commands=commands)
    user_choice = permission.run() if ask_user else UserChoice.YES
    if user_choice == UserChoice.YES:
        results = executor.run(commands=commands, verbose=True)
        command, stdout, stderr, exit_code = results
        code_logs = []
        code_logs.append(
            CodeReport(code=command, run=True, stderr=stderr, stdout=stdout)
        )

        return code_logs

    else:
        print(colored("Command execution cancelled.", "yellow"))
        return None, None
