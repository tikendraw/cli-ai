from groq import Groq
from core.basellm import BaseLLM, LLMConfig
from core.prompts import SYSTEM_PROMPT
from .utils import DotDict
import os
from core.basemessage import SystemMessage, UserMessage, AssistantMessage, LLMHistory
from typing import Any, Dict, Any, Optional
from core.bashcode import BashCode
import os
import google.generativeai as genai
from google.generativeai.types.generation_types import GenerationConfig


class GoogleLLM(BaseLLM):
    api_key_var_name = 'GOOGLE_API_KEY'

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        self.client = genai.GenerativeModel(model_name=config.model_name)
        self.generative_config = None

    def get_api_key_from_environment(self):
        return os.getenv(self.api_key_var_name)
    
    def _response_parser(self, response:Any) -> str:
        try:
            return response.text
        except AttributeError as e:
            print(response)
            raise e    
    
    def _generate_response(self,user_prompt:str, history:list[dict]=None, **kwargs) -> Any:
        config = self._parse_kwargs_to_generative_config(kwargs)
        chat_history = self._bulk_change_message_type_to_google_message_type(messages=history)
        chat = self.client.start_chat(
            history=[*chat_history]
        )
        response = chat.send_message(user_prompt, generation_config=config)
        
        return response
    
    def _parse_kwargs_to_generative_config(self, kwargs:Dict) -> GenerationConfig:
        return GenerationConfig(
            candidate_count = kwargs.get("candidate_count",None),
            stop_sequences = kwargs.get("stop_sequences",None),
            max_output_tokens = kwargs.get("max_output_tokens",None),
            temperature = kwargs.get("temperature",None),
            top_p = kwargs.get("top_p",None),
            top_k = kwargs.get("top_k",None),
            response_mime_type = kwargs.get("response_mime_type",None),
            response_schema = kwargs.get("response_schema",None),
        )
        
    def _change_message_type_to_google_message_type(self, message:dict) -> Dict:
        ''' unlike openai based apis which uses role and content in message , 
        google uses role and parts '''
        role = message.get('role',' ')
        part = message.get('content', ' ')
        return dict(role=role, parts=part)

    def _bulk_change_message_type_to_google_message_type(self, messages:list[dict]) -> list[Dict]:
        return [self._change_message_type_to_google_message_type(message) for message in messages]
        
        