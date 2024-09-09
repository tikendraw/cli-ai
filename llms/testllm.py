from core.basellm import BaseLLM

class TestLLM(BaseLLM):
    model_name = "test"
    
    def __init__(self, model_name: str):
        self.model_name = model_name

    def generate_response(self, **kwargs):
        # Simulate LLM response for this example
        return "echo 'Hello, World!'"
    

