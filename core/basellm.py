from os import system
from typing import List, Optional, Any
import os
from abc import ABC, abstractmethod
from pydantic import ValidationError
from termcolor import colored
from .basemodel import BaseModel
from .prompts import SYSTEM_PROMPT, ERROR_FIX_PROMPT
from .basemessage import AssistantMessage, LLMHistory, UserMessage
from .bashcode import BashCode, BashCodeRun
from dataclasses import dataclass

N_TRY:int = 3
N_HIST = 5

@dataclass
class LLMConfig:
    model_name: str
    api_key: Optional[str] = None
    system_prompt: str = SYSTEM_PROMPT


class BaseLLM(BaseModel, ABC):
    def __init__(self, config: LLMConfig):
        self.config = config
        self.api_key = config.api_key or self.get_api_key_from_environment()
        self.history = LLMHistory(system_prompt=config.system_prompt)
        
    def generate_response(self,user_prompt:str, n_hist:int=N_HIST,n_try:int=N_TRY, include_system_prompt:bool=True,**kwargs) -> BashCode:        
        parsable_response=False
        
        while not parsable_response and n_try>0:
            response = self._gen(user_prompt=user_prompt, n_hist=n_hist, include_system_prompt=include_system_prompt)
            response = self._response_parser(response=response)
            print(colored(response, 'red', 'on_black'))
            
            try:
                response = self.code_parser(response)
                parsable_response = True
            except ValidationError as e:
                print(f"Error parsing response: {e}")
                n_try -= 1
                print('Regenerating...')
        
        if not parsable_response:
            raise ValueError("Failed to generate a parsable response")
        
        self.history.add_message(UserMessage(content=user_prompt))
        self.history.add_message(AssistantMessage(content=str(response)))
        
        return response
    
    def _gen(self, user_prompt, n_hist, include_system_prompt,**kwargs):
        history = self.history.get_last_n_messages_as_dict(
            n=n_hist,
            include_system_prompt=include_system_prompt
            )
        

        response = self._generate_response(
            user_prompt=user_prompt, 
            history=history,
            **kwargs
            )  
        return response
          
    @abstractmethod
    def _generate_response(self,user_prompt:str, history:list[dict], **kwargs):
        pass

    @abstractmethod
    def get_api_key_from_environment(self):
        pass
    
    @abstractmethod
    def _response_parser(self,response:Any) -> BashCode:
        ''' return message text out of generated response'''
        pass
    
    def code_parser(self, text:str) -> BashCode :
        return BashCode.from_text(text=text)

    def fix_error(self, coderun:BashCodeRun,**kwargs):
        user_prompt = ERROR_FIX_PROMPT.format(
            instructions=coderun.instructions,
            commands='\n\n'.join(coderun.stepwise_bash_code),
            error_logs=' '.join([i.model_dump() for i in coderun.logs]),
            modifications=coderun.modifications,
            )
        return self.generate_response(user_prompt=user_prompt, n_hist=2)

    def run(self, *args, **kwargs):
        self.generate_response(**kwargs)
        
