from intents.base import BaseIntent

class ChatGPTIntent(BaseIntent):
    def get_system_prompt(self):
        """
        Returns the system prompt for a helpful assistant.
        :return: System prompt as a string
        """
        return "You are a helpful, knowledgeable assistant. Keep responses informative and concise."