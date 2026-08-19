# Nexus

Nexus is a lightweight, extensible framework for building AI Agents in Python. It simplifies agent orchestration, memory management, and tool integration using the `litellm` interface.

## Features

*   **Modular Architecture**: Separate concerns with dedicated classes for Config, Memory, Instructions, and Tools.
*   **Tool Integration**: Effortlessly define and execute custom tools using simple decorators.
*   **Persistent Memory**: Easily manage agent conversation history and state.
*   **LiteLLM Powered**: Access hundreds of LLMs (OpenAI, Anthropic, Ollama, etc.) with a unified API.

---

## Installation

You can install Nexus using your preferred Python package manager:

**Using pip:**
```bash
pip install nexus
```

**Using uv (Recommended):**
```bash
uv add nexus
```

*(Requires Python 3.10+)*

---

## Project Structure

The core logic of the framework is located within the `src/nexus/` directory:

```text
src/nexus/
├── agent.py         # Main Agent orchestration logic
├── config.py        # Configuration management
├── memory.py        # Conversation and state history
├── tool.py          # Tool registration and execution
└── instruction.py   # System instruction handling
```

---

## Quick Start

```python
from nexus import Agent, AgentConfig, AgentMemory, ToolBook

# 1. Configure the Agent
config = AgentConfig(model="gpt-4o")

# 2. Setup Memory
memory = AgentMemory()

# 3. Define Tools
tools = ToolBook()

@tools.add_tool(description="Get the weather for a city")
def get_weather(city: str):
    return f"The weather in {city} is sunny."

# 4. Initialize and Run
agent = Agent(agent_config=config, agent_memory=memory, tool_book=tools)

response = agent.send_prompt("What is the weather in Paris?")
print(response)
```

---

## Core Components

| Component | Description |
| :--- | :--- |
| **`Agent`** | The central orchestrator that manages the loop between LLM calls and tool execution. |
| **`AgentConfig`** | Holds model parameters and settings for your LLM. |
| **`AgentMemory`** | Handles chat history, tool call results, and system instructions. |
| **`ToolBook`** | A collection/registry for tools that the agent can invoke. |

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
