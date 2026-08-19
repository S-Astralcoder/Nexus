
class AgentInstruction:
    def __init__(self, role : str, behavior : str, instructions : str, custom_instruction : str = "") -> None:
        self.role = role
        self.behavior = behavior
        self.instructions = instructions
        self.custom_instruction = custom_instruction

    def get_instruction(self):
        return self.custom_instruction or f"""
        Role : {self.role}
        Behavior : {self.behavior}

        Instruction : 
        {self.instructions}
        """

    
