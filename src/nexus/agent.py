# External
import json
from litellm import completion #pyright: ignore
from dataclasses import asdict
from rich.console import Console

# Internal
from nexus.config import AgentConfig
from nexus.instruction import AgentInstruction
from nexus.memory import AgentMemory
from nexus.tool import ToolBook


import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")


class Agent:
    def __init__(self ,agent_config : AgentConfig, agent_memory : AgentMemory, instruction : AgentInstruction | None = None, tool_book : ToolBook | None = None, show_tool_calls : bool = True) -> None:
        self.agent_config = agent_config
        self.agent_memory = agent_memory
        self.instruction = instruction
        self.tool_book = tool_book
        self.show_tool_calls = show_tool_calls

        self.console = Console()

        self._add_instruction_if_exists()


    def _add_instruction_if_exists(self):
        if self.instruction is None:
            return
        self.agent_memory.add_memory("system", self.instruction.get_instruction())

    def get_response(self, message : str):
        try:
            tools : list[dict] | None =  None
            if self.tool_book is not None:
                tools = self.tool_book.get_tools_schema()                
            response = completion(**asdict(self.agent_config), messages=self.agent_memory.get_all_memory(), tools=tools)
            return response
        except Exception as e:
            print(f"Error Occurred : {e}")
            raise SystemExit("Aboding Operation...")

    def execute_tool(self, function_name : str, arguments : dict):
        if self.tool_book is None:
            raise Exception("Tool call has been called when no function exists")
        tool_links = self.tool_book.get_tool_call_links()
        return tool_links[function_name](**arguments)


    def execute_tool_calls(self, tool_calls):
        for tool_call in tool_calls:
            tool_call_id = tool_call.id
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            if self.show_tool_calls:
                self.console.print(f"[yellow]Tool {function_name} was called with arguments {json.dumps(arguments)}\n")
            try:
                result = self.execute_tool(function_name=function_name, arguments=arguments) #pyright: ignore
            except Exception as e:
                self.console.print(f"[red]Error Occurred while calling tool : {e}")
                self.agent_memory.add_tool_call_result(tool_call_id=tool_call_id, result_content=f"{e}")
                continue
            if self.show_tool_calls:
                self.console.print(f"[yellow]Tool {function_name} call resulted with response :\n{result}\n")
            self.agent_memory.add_tool_call_result(tool_call_id=tool_call_id, result_content=result)

    def send_prompt(self, message : str, max_iteration : int = 10) -> str:
        self.agent_memory.add_memory(role="user", content=message)
        for _ in range(max_iteration):
            response = self.get_response(message=message)
            if response.choices[0].message.tool_calls: #pyright: ignore
                self.agent_memory.add_tool_call_memory(response.choices[0].message) #pyright: ignore
                self.execute_tool_calls(tool_calls=response.choices[0].message.tool_calls) #pyright: ignore
                continue
            return response.choices[0].message.content #pyright: ignore
        return "[ALERT] Max Iteration Reached"