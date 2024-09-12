from core.basellm import BaseLLM, LLMConfig
from typing import List, Dict, Any
from core.prompts import SYSTEM_PROMPT
import os


class GroqLLM(BaseLLM):    
    api_key_var_name = 'GROQ_API_KEY'

    def __init__(self, config: LLMConfig):
        super().__init__(config)
        from groq import Groq
        self.client = Groq(api_key=self.api_key)

    def _response_parser(self, response: Any) -> str:
        try:
            return response.choices[0].message.content
        except AttributeError as e:
            print(response)
            raise e

    def _generate_response(self, user_prompt: str, history: List[Dict[str, str]] = None, **kwargs) -> Any:
        return self.client.chat.completions.create(
            messages=[*history, {"role": "user", "content": user_prompt}],
            model=self.config.model_name,
            **kwargs
        )

    def get_api_key_from_environment(self) -> str:
        return os.getenv(self.api_key_var_name)