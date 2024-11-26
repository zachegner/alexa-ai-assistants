from intents.base import BaseSkill

class FunnyResponseSkill(BaseSkill):
    def get_system_prompt(self):
        return "You are a funny assistant. Respond to the user with humor, wit, and jokes when appropriate."