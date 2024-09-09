from typing import List, Optional, Any
from .basemodel import BaseModel
from .prompts import SYSTEM_PROMPT, ERROR_FIX_PROMPT
from .basemessage import AssistantMessage, LLMHistory, UserMessage

N_HIST = 5
class BaseLLM(BaseModel):
    model_name = ''
    system_prompt = SYSTEM_PROMPT
    history = LLMHistory()
    api_key = None
        
    def generate_response(self,user_prompt:str, n_hist:int=N_HIST, include_system_prompt:bool=True,**kwargs) -> str:
        history = self.history.get_last_n_messages_as_dict(
            n=n_hist,
            include_system_prompt=include_system_prompt
            )
        

        response = self._generate_response(
            user_prompt=user_prompt, 
            history=history,
            **kwargs
            )
        
        self.history.add_message(UserMessage(content=user_prompt))
        self.history.add_message(AssistantMessage(content=response))
        return response
    
    def _generate_response(self,user_prompt:str, history:list[dict], **kwargs):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def _response_parser(self,response:Any):
        ''' return message text out of generated response'''
        raise NotImplementedError("Subclass should implement this to get the text message out fo generated response")

    def fix_error(self, previous_user_prompt:str, command:str, error:str,modifications:str,**kwargs):
        user_prompt = ERROR_FIX_PROMPT.format(
            previous_user_prompt=previous_user_prompt,
            command=command,
            error=error,
            modifications=modifications,
            )
        return self.generate_response(user_prompt=user_prompt, n_hist=2)

    def run(self, *args, **kwargs):
        self.generate_response(**kwargs)
        
