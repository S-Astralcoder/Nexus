import json
from typing import Any


class AgentMemory:
    def __init__(self) -> None:
        self.memory : list[dict | Any] = []

    def add_interaction(self, role : str, content : str):
        self.memory.append({"role" : role, "content" : content})
    
    def add_tool_call_result(self, tool_call_id : str, tool_call_result):
        self.memory.append({"role" : "tool", "tool_call_id" : tool_call_id, "content" : json.dumps(tool_call_result)})

    def add_memory(self, memory_content : Any):
        self.memory.append(memory_content)
    
    def clear_memory(self):
        self.memory.clear()

    def over_write_memory(self, memory : list[dict | Any]):
        self.memory = memory
    
    def get_memory(self):
        return self.memory
    
    