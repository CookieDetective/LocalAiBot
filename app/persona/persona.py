class Persona:
    def __init__(
        self,
        name="Jarvis",
        description=None,
        style="curious and serious",
        goals=None,
        preferences=None,
        tools=None,
        prompt_suffix=None
    ):
        self.name = name
        self.description = description or (
            "Hello! I'm Jarvis, your personal file manager. Ask me questions about documentation, databases, and . "
            "I can help you with messaging, file referencing, citing sources, and creative writing."
        )
        self.style = style
        self.goals = goals or [
            "Provide clarification on documentation",
            "Reference and summarize local files",
            "Retrieve data from databases",
            "Run regression tests"
        ]
        self.preferences = preferences or {
            "humor_level": "mid",
            "fact_checking": "strict",
            "response_length": "balanced"
        }
        self.tools = tools or []
        self.prompt_suffix = prompt_suffix or ""

        self.custom = {}

    def intro(self):
        return self.description

    def persona_prompt(self, user_input):
        # Generates a persona-augmented prompt for LLM
        persona_desc = f"You are {self.name}, {self.style}.\n{self.description}\n"
        prompt = f"{persona_desc}{self.prompt_suffix}\nUser: {user_input}\n{self.name}:"
        return prompt

    def add_tool(self, tool):
        if tool not in self.tools:
            self.tools.append(tool)

    def set_custom_field(self, key, value):
        self.custom[key] = value

    def get_custom_field(self, key):
        return self.custom.get(key)