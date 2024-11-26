
from intents.base import BaseSkill

class ChatGPTSkill(BaseSkill):
    def get_system_prompt(self):
        return "You are a helpful, knowledgeable assistant. Keep responses informative and concise."