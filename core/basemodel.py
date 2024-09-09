# core/basemodel.py
# Objective: Implements the BaseModel class for handling models

from ast import Dict
from typing import List, Optional, TypedDict
from dataclasses import dataclass

        

class BaseModel:
    context: list[Dict]
    
    def run(self, **kwargs):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def get_context(self) -> List[dict]:
        return self.context
    
    def set_context(self, context: List[dict]):
        self.context = context