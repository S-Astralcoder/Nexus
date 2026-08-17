# External
from litellm import completion #pyright: ignore
from dataclasses import asdict
# Internal
from nexus.config import AgentConfig
from nexus.memory import AgentMemory
from nexus.tool import ToolBook


class Agent:
    def __init__(self, agent_config : AgentConfig, agent_memory : AgentMemory, tool_book : ToolBook | None = None) -> None:
        self.agent_config = agent_config
        self.agent_memory = agent_memory


    def get_response(self, message : str):
        try:
            response = completion(**asdict(self.agent_config), messages=self.agent_memory.get_all_memory())
            return response
        except Exception as e:
            print(f"Error Occurred : {e}")
            raise SystemExit("Aboding Operation...")

    def send_prompt(self, message : str, max_iteration : int = 10) -> str:
        self.agent_memory.add_memory(role="user", content=message)
        for _ in range(max_iteration):
            response = self.get_response(message=message)
            if response.choices[0].message.tool_calls: #pyright: ignore
                pass
            return response.choices[0].message.content #pyright: ignore
        return "[ALERT] Max Iteration Reached"