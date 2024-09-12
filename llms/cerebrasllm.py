from groq import Groq
from core.basellm import BaseLLM
from core.prompts import SYSTEM_PROMPT
from .utils import DotDict
import os
from core.basemessage import SystemMessage, UserMessage, AssistantMessage, LLMHistory
from typing import Any
from core.bashcode import BashCode
import os
from cerebras.cloud.sdk import Cerebras

class CerebrasLLM(BaseLLM):
    api_key_var_name = 'CEREBRAS_API_KEY'
    
    def __init__(self, api_key: str=None, model_name: str = "llama3.1-8b", system_prompt: str = SYSTEM_PROMPT, **kwargs):
        super().__init__()
        self.client = Cerebras(api_key=api_key)
        self.history = LLMHistory(system_prompt=system_prompt)
        self.model_name = model_name
        
    def _response_parser(self, response:Any) -> str:
        try:
            return response.choices[0].message.content
        except AttributeError as e:
            print(response)
            raise e    
        
    def _generate_response(self,user_prompt:str, history:list[dict]=None, **kwargs) -> Any:
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
        
        return response
    
        