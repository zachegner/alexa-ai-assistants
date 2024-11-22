from intents.base import BaseIntent

class FunnyResponseIntent(BaseIntent):
    def get_system_prompt(self):
        """
        Returns the system prompt for a funny assistant.
        :return: System prompt as a string
        """
        return "You are a funny assistant. Respond to the user with humor, wit, and jokes when appropriate."