from typing import Any, Callable

from nexus.exceptions import UnsupportedParameterType


class ToolRegistry:
    def __init__(self) -> None:
        self.tools_schema = []
        self.tool_link : dict[str, Callable] = {}



    def _type_to_string_type(self, type):
        if type == str:
            return "string"
        if type == int:
            return "integer"
        if type == float:
            return "number"
        if type == bool:
            return "boolean"
        raise UnsupportedParameterType(f"type : {type} is not supported in this current version. manually set parameters when adding tool")

    def _generate_tool_schema(self, function_name : str, function_description : str, function_type_parameters : dict, user_parameters_provided : bool):
        if user_parameters_provided:
            return {
                "type" : "function",
                "function" : {
                    "name" : function_name,
                    "description" : function_description,
                    "parameters" : {
                        "type" : "object",
                        "properties" : function_type_parameters
                    } 
                }
            }
        else :
            return {
                "type" : "function",
                "function" : {
                    "name" : function_name,
                    "description" : function_description,
                    "parameters" : {
                        "type" : "object",
                        "properties" : {parameter_name : { "type" : self._type_to_string_type(parameter_type) } for parameter_name, parameter_type in function_type_parameters.items()}
                    } 
                }
            }

    def add_tool(self, function : Callable[..., Any] | None = None ,name : str | None = None , description : str | None = None, function_parameter : dict | None = None):    
        def tool_meta_extractor(func : Callable[..., Any]):
            function_name = name or func.__name__
            function_description = description or func.__doc__
            function_type_parameters = function_parameter or func.__annotations__
            
            user_parameters_provided = False if function_parameter is None else True
            self.tools_schema.append(self._generate_tool_schema(function_name=function_name, function_description=function_description, function_type_parameters=function_type_parameters, user_parameters_provided=user_parameters_provided))
            self.tool_link.update({function_name : func})
            return func

        if function is not None:
            tool_meta_extractor(func=function)
            return
        
        return tool_meta_extractor

    def get_tool_link(self):
        return self.tool_link

    def get_tool_schema(self):
        return self.tools_schema