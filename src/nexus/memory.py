# External
from typing import Any


class AgentMemory:
    def __init__(self) -> None:
        self.memory : list[dict[Any, Any]]= []

    def get_all_memory(self):
        return self.memory

    def add_memory(self, role : str, content : str):
        self.memory.append({"role": role, "content" : content})

    def add_tool_call_memory(self, tool_call_content): #pyright: ignore
        self.memory.append(tool_call_content) #pyright: ignore

    def add_tool_call_result(self, tool_call_id : int, result_content : dict[Any, Any] | str):
        self.memory.append({"role" : "tool", "tool_call_id" : tool_call_id, "content" : result_content})