from typing import Callable, Dict, Any

class FunctionDefinition:
    def __init__(self, name: str, description: str, parameters: Dict[str, Any], code: Callable):
        self.type = "function"
        self.function = {
            "name": name,
            "description": description,
            "parameters": parameters
        }
        self.code = code

    def to_dict(self):
        return {
            "type": self.type,
            "function": self.function,
            "code": self.code
        }
