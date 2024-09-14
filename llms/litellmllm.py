from core.basellm import BaseLLM, LLMConfig
import os
from litellm import completion

from core.basemessage import LLMHistory
from core.bashcode import BashCode
from typing import Any


class LitellmLLM(BaseLLM):

    api_key_var_name = "some_api_key"

    def __init__(self, config: LLMConfig):
        self.config = config
        self.history = LLMHistory(load_history=False)

    def _generate_response(self, user_prompt: str, history: list[dict], **kwargs):

        return completion(
            model=self.config.model_name,
            messages=[*history, {"role": "user", "content": user_prompt}],
            **kwargs
        )

    def _response_parser(self, response: Any) -> str:
        try:
            return response.choices[0].message.content
        except AttributeError as e:
            print(response)
            raise e

    def get_api_key_from_environment(self):
        return os.getenv(self.api_key_var_name)
