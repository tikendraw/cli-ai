from dataclasses import dataclass
from typing import List
from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str

class UserMessage(Message):
    role: str = "user"

class AssistantMessage(Message):
    role: str = "assistant"
    
class SystemMessage(Message):
    role: str = "system"
    
from config import history_file
from .prompts import SYSTEM_PROMPT

class LLMHistory:
    def __init__(self, load_history:bool=False, system_prompt:str=SYSTEM_PROMPT):
        self.history = []        
        self.history.append(SystemMessage(content=system_prompt))

        if load_history:
            self.history.extend(self.read_history_from_jsonl(history_file)[1:])

    def add_message(self, message: Message):
        self.history.append(message)
        self.append_to_jsonl(history_file, message)
        
    def get_history(self) -> List[Message]:
        return self.history
        
    def get_last_n_messages(self, n: int = 10, include_system_prompt: bool = True) -> List[Message]:
        if n <= 0:
            return [self.history[0]]
        
        if include_system_prompt:
            if len(self.history) == 1 or n >= len(self.history):
                return self.history  # Return all, including system prompt
            else:
                return [self.history[0]] + self.history[-(n-1):]
        else:
            return self.history[-min(n, len(self.history)):]
    
    def clear_history(self):
        self.history = []
        
    def get_history_as_dict(self) -> List[dict]:
        return [message.model_dump() for message in self.history]
    
    def get_last_n_messages_as_dict(self, n:int=10, include_system_prompt:bool=True) -> List[dict]:
        return [message.model_dump() for message in self.get_last_n_messages(n, include_system_prompt)]
    
    def write_history_to_jsonl(self, filename: str):
        import json
        with open(filename, 'w') as f:
            for message in self.history:
                json.dump(message.model_dump(), f)
                f.write('\n')

    def append_to_jsonl(self, filename: str, message: Message):
        import json
        with open(filename, 'a') as f:
            json.dump(message.model_dump(), f)
            f.write('\n')


        
    @classmethod
    def read_history_from_jsonl(cls, filename: str) -> 'LLMHistory':
        import json
        history = []
        try:
            with open(filename, 'r') as f:
                for line in f:
                    message_data = json.loads(line.strip())
                    role = message_data['role']
                    content = message_data['content']
                    if role == 'user':
                        message = UserMessage(content=content)
                    elif role == 'assistant':
                        message = AssistantMessage(content=content)
                    elif role == 'system':
                        message = SystemMessage(content=content)
                    else:
                        raise ValueError(f"Unknown role: {role}")
                    history.append(message)
        except Exception as e:
            print(f"Error reading history from {filename}: {e}")

        return history