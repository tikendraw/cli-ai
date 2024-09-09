from typing import Any
import ollama
from core.basellm import BaseLLM
from pydantic import BaseModel

from core.prompts import SYSTEM_PROMPT
from .utils import DotDict
import os
from core.basemessage import SystemMessage, UserMessage, AssistantMessage, LLMHistory

'''
{'model': 'qwen2:0.5b', 'created_at': '2024-09-07T15:30:44.63660434Z', 'message': {'role': 'assistant', 'content': 'ls -al'}, 
'done_reason': 'stop', 'done': True, 'total_duration': 11481524274, 'load_duration': 34653324, 'prompt_eval_count': 996, 
'prompt_eval_duration': 10787977000, 'eval_count': 4, 'eval_duration': 143595000}
'''
class OllamaOutput(BaseModel):
    model:str
    created_at:str
    message:AssistantMessage
    done_reason:str
    done:bool
    total_duration:int
    load_duration:int
    prompt_eval_count:int
    prompt_eval_duration:int
    eval_count:int
    eval_duration:int
    
class OllamaLLM(BaseLLM):
    
    def __init__(self, model_name: str, **kwargs):
        super().__init__()
        self.model_name = model_name
        self.history = LLMHistory(load_history=True, system_prompt=SYSTEM_PROMPT)
        
    def _response_parser(self, response:Any):
        
        response = OllamaOutput(**response)
        return response.message.content

        
    def _generate_response(self, user_prompt:str,history:list[dict], **kwargs):
        response = ollama.chat(
            messages=[*history,
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            model=self.model_name,
            **kwargs
        )

        response = self._response_parser(response=response)            
        return response
        
    

