# intents/base.py
from abc import ABC, abstractmethod

class BaseSkill:
    def __init__(self, get_chatgpt_response):
        """
        Initialize the base skill with a method to get responses from OpenAI.
        """
        self.get_chatgpt_response = get_chatgpt_response

    @abstractmethod
    def get_system_prompt(self):
        """
        Define the system prompt for the skill.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def get_welcome_message(self):
        """
        Define the welcome message for the skill.
        Must be implemented by subclasses.
        """
        pass

    def handle_intent(self, data, session_attributes):
        """
        Handle the incoming intent request.
        """
        user_query = data['request']['intent']['slots']['Query']['value']
        history = session_attributes.get('history', [])

        # Inject system prompt if not present
        if not any(msg.get("role") == "system" for msg in history):
            history.insert(0, {"role": "system", "content": self.get_system_prompt()})

        # Add user query to history
        history.append({"role": "user", "content": user_query})

        # Get response from OpenAI
        assistant_response = self.get_chatgpt_response(history)

        # Add assistant response to history
        history.append({"role": "assistant", "content": assistant_response})
        session_attributes['history'] = history

        # Create Alexa response
        response = {
            'outputSpeech': {
                'type': 'PlainText',
                'text': assistant_response
            },
            'shouldEndSession': False,
            'sessionAttributes': session_attributes
        }

        return response