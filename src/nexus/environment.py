from typing import Any, Callable

from nexus.tool_registry import ToolRegistry


class AgentEnvironment:
    def __init__(self, tool_registry : ToolRegistry) -> None:
        self.tool_registry = tool_registry

    def execute_function_link(self, function_name : str, function_arguments : dict):
        try:
            return self.tool_registry.get_tool_link()[function_name](**function_arguments)
        except Exception as e:
            return f"{e}"



        
