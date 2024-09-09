from groq import Groq
from core.basellm import BaseLLM
from core.prompts import SYSTEM_PROMPT
from .utils import DotDict
import os
from core.basemessage import SystemMessage, UserMessage, AssistantMessage, LLMHistory
from typing import Any


class GroqLLM(BaseLLM):
    model_name = "Groq"
    
    def __init__(self, api_key: str, model_name: str, **kwargs):
        super().__init__()
        self.model_name = model_name
        self.client = Groq(api_key=api_key)
        self.history = LLMHistory(load_history=True, system_prompt=SYSTEM_PROMPT)

    def _response_parser(self, response:Any):
        return response.choices[0].message.content
    
    def _generate_response(self,user_prompt:str, history:list[dict]=None, **kwargs):
        response = self.client.chat.completions.create(
            messages=[*history,
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            model=self.model_name,
            **kwargs
        )
        
        return self._response_parser(response=response)
    
        

    

