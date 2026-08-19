from typing import Any, Callable


class ToolBook:
    _tool_book : list[dict] = []
    _tool_links : dict[Any, Any] = {} 
    def __init__(self, tags : list[str] | None = None) -> None:
        self.tags = tags


    def get_tools_schema(self):
        tool_list : list[dict] = []
        for tool in self._tool_book:
            if tool["tag"] == self.tags or tool["tag"] in self.tags:
                tool_list.append(tool["function_info"])
        return tool_list

    @classmethod
    def get_tool_call_links(cls):
        return cls._tool_links

    def _type_to_str(self, parameter_type) -> str:
        if parameter_type is str:
            return "string"
        if parameter_type is int:
            return "integer"
        if parameter_type is float:
            return "float"
        if parameter_type is bool:
            return "boolean"
        raise Exception(f"parameter type : {type} not supported")

    def _get_formatted_function_parameter(self, function_parameter : dict):
        parameter : dict[Any, Any] = {}
        for parameter_name, parameter_type in function_parameter.items():
            parameter.update({parameter_name : {"type" : self._type_to_str(parameter_type=parameter_type)}})
        return parameter

    def add_tool(self, name : str | None = None , description : str | None = None, tag : str | None = None):
        def decorator(func : Callable[..., Any]):
            function_name = name or func.__name__
            function_description = description or func.__doc__
            function_parameters = func.__annotations__

            self._tool_links.update({function_name : func})

            self._tool_book.append({
                "tag" : tag,
                "function_info" : {
                    "type" : "function",
                    "function" : {
                        "name" : function_name,
                        "description" : function_description or "",
                        "parameters" : {
                            "type" : "object",
                            "properties" : self._get_formatted_function_parameter(function_parameter=function_parameters)
                        }
                    }
                }
            })
            return func
        return decorator