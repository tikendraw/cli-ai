#utils.py
from typing import List, Optional

def get_kwargs(kwargs: dict, keys: List[str], default: Optional[dict] = None) -> dict:
    return {k: kwargs[k] for k in keys if k in kwargs}

class DotDict:
    def __init__(self, dictionary: dict):
        for key, value in dictionary.items():
            if isinstance(value, dict):
                setattr(self, key, DotDict(value))
            else:
                setattr(self, key, value)
    
    def __getattr__(self, attr):
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"

    def __str__(self):
        return f"{self.__class__.__name__}({self.__dict__})"
    
    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        setattr(self, key, value)
