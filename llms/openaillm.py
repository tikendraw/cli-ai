from typing import List, Dict, Any, Optional
import os
from openai import OpenAI
from core.basellm import BaseLLM, LLMConfig
from core.prompts import SYSTEM_PROMPT

class OpenAILLM(BaseLLM):
    api_key_var_name = 'OPENAI_API_KEY'

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=config.base_url if hasattr(config, 'base_url') else None
        )

    def get_api_key_from_environment(self) -> str:
        return os.getenv(self.api_key_var_name)

    def _response_parser(self, response: Any) -> str:
        try:
            return response.choices[0].message.content
        except AttributeError as e:
            print(response)
            raise e

    def _generate_response(self, user_prompt: str, history: List[Dict[str, str]] = None, **kwargs) -> Any:
        messages = [*history, {"role": "user", "content": user_prompt}]
        return self.client.chat.completions.create(
            model=self.config.model_name,
            messages=messages,
            **kwargs
        )

    @classmethod
    def from_env(cls, model_name: str, system_prompt: Optional[str] = None, base_url: Optional[str] = None):
        api_key = os.getenv(cls.api_key_var_name)
        if not api_key:
            raise ValueError(f"API key not found in environment variable {cls.api_key_var_name}")
        
        config = LLMConfig(
            model_name=model_name,
            api_key=api_key,
            system_prompt=system_prompt or SYSTEM_PROMPT
        )
        if base_url:
            config.base_url = base_url
        
        return cls(config)