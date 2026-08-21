# External
from dataclasses import asdict
import json
from litellm import ModelResponse, completion
import warnings


# Internal
from nexus.environment import AgentEnvironment
from nexus.memory import AgentMemory
from nexus.tool_registry import ToolRegistry
from src.nexus.model import ModelBase


warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")



class Agent:
    def __init__(self, model_base : ModelBase , memory : AgentMemory = AgentMemory(), instruction : str = "", tool_registry : ToolRegistry | None = None, show_tool_calls : bool = True) -> None:
        # assign memory to get control over agents memory or just leave it if you don't want to tamper with agent memory

        self.model_base = model_base
        self.memory = memory 
        self.tools = tool_registry
        self.environment = AgentEnvironment(tool_registry=tool_registry)
        self.show_tool_call = show_tool_calls
        
        self.memory.add_interaction(role="system", content=instruction)

    def _send_message_payload(self) -> ModelResponse:
        response = completion(model=self.model_base.model, temperature=self.model_base.temperature, top_p=self.model_base.top_p, messages=self.memory.get_memory(), tools=self.tools.get_tool_schema() if isinstance(self.tools, ToolRegistry) else None)
        return response

    def run_agent(self, message : str, max_iteration : int = 10):
        self.memory.add_interaction(role="user", content=message)
        for _ in range(max_iteration):
            response = self._send_message_payload()
            if response.choices[0].message.tool_calls:
                self.memory.add_memory(memory_content=response.choices[0].message)
                for tool_call in response.choices[0].message.tool_calls:
                    function_name = tool_call.function.name
                    tool_call_id = tool_call.id
                    function_arguments = json.loads(tool_call.function.arguments)
                    if self.show_tool_call:
                        print(f"[TOOL CALL] function_name={function_name} with arguments={function_arguments}")
                    result = self.environment.execute_function_link(function_name=function_name, function_arguments=function_arguments)
                    if self.show_tool_call:
                        print(f"[Result] : {result}")
                    self.memory.add_tool_call_result(tool_call_id=tool_call_id, tool_call_result=result)
                continue

            return response.choices[0].message.content

    
        
            



