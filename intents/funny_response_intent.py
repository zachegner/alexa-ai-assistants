# intents/funny_response_intent.py
from intents.base import BaseSkill

class FunnyResponseSkill(BaseSkill):
    def get_system_prompt(self):
        return "You are a funny assistant. Keep responses humorous and engaging."

    def get_welcome_message(self):
        return "Hey there! Ready for some laughs? How can I tickle your funny bone today?"