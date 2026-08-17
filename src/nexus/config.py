from typing import Any, Literal
import httpx
from litellm import OpenAIWebSearchOptions 

from dataclasses import dataclass



@dataclass
class AgentConfig:
    model : str
    timeout: float | str | httpx.Timeout | None = None
    temperature: float | None = None
    top_p: float | None = None
    n: int | None = None
    stop=None
    max_completion_tokens: int | None = None
    max_tokens: int | None = None
    presence_penalty: float | None = None
    frequency_penalty: float | None = None
    reasoning_effort: Literal["none", "minimal", "low", "medium", "high", "xhigh", "default"] | None = None
    verbosity: Literal["low", "medium", "high"] | None = None
    

