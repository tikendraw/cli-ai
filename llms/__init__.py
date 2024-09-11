from .testllm import TestLLM
from .ollamallm import OllamaLLM 
from .groqllm import GroqLLM
from .utils import DotDict

models = {
    'groq':GroqLLM,
    'ollama':OllamaLLM,
}

def get_model_class(model_class:str):
    model_class =  models.get(model_class, None)
    if model_class:
        return model_class  
    else: 
        raise ValueError("Model not supported")
    

def extract_model_class_and_model_name(model_str:str):
    '''splits str from first / (slash)'''
    try:
        l = model_str.split('/')
        model_class = l[0]
        model_name = '/'.join(l[1:])
        return model_class, model_name
    except IndexError as e:
        raise ValueError("Not a valid model name, do this: groq/llama3-8b-8192 or ollama/qwen2:0.5b")

__all__ = ["TestLLM", "GroqLLM", "OllamaLLM", 'get_model_class', 'extract_model_class_and_model_name', 'DotDict']
