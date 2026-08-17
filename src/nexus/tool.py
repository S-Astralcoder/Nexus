from typing import Any, Callable


class ToolBook:
    tool_book = {}
    def __init__(self) -> None:
        pass


    def tool(self, name : str, description : str, tags : list[str]):
        def decorator(func : Callable[..., Any]):
            return func
        return decorator