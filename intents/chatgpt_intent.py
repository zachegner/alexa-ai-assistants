# intents/chatgpt_intent.py
from intents.base import BaseSkill

class ChatGPTSkill(BaseSkill):
    def get_system_prompt(self):
        return "You are a helpful, knowledgeable assistant. Keep responses informative and concise."

    def get_welcome_message(self):
        return "Welcome to Eggy Bot! What's up man?"