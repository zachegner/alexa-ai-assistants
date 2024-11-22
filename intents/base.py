from abc import ABC, abstractmethod

class BaseIntent(ABC):
    def __init__(self, get_chatgpt_response):
        """
        Constructor for all intents.
        :param get_chatgpt_response: Function to get responses from OpenAI
        """
        self.get_chatgpt_response = get_chatgpt_response

    def manage_conversation_history(self, session_attributes, user_query):
        """
        Adds the user query to the conversation history
        and ensures the system message is present.
        :param session_attributes: The session attributes from the Alexa request
        :param user_query: The user's query (text)
        :return: Updated conversation history
        """
        history = session_attributes.get('history', [])
        
        # Inject the system prompt at the start if not already present
        if not any(msg.get("role") == "system" for msg in history):
            system_prompt = self.get_system_prompt()
            history.insert(0, {"role": "system", "content": system_prompt})
        
        # Add the user query
        history.append({"role": "user", "content": user_query})
        return history

    def create_response(self, history, session_attributes):
        """
        Calls the OpenAI API and creates the Alexa skill response.
        :param history: The updated conversation history
        :param session_attributes: The session attributes
        :return: Alexa-compliant JSON response
        """
        # Get the assistant response from OpenAI
        assistant_response = self.get_chatgpt_response(history)
        
        # Add the response to the conversation history
        history.append({"role": "assistant", "content": assistant_response})
        session_attributes['history'] = history

        # Return the response
        return {
            'outputSpeech': {
                'type': 'PlainText',
                'text': assistant_response
            },
            'shouldEndSession': False,
            'sessionAttributes': session_attributes
        }

    @abstractmethod
    def get_system_prompt(self):
        """
        Abstract method that should be implemented by child classes
        to define a system prompt specific to the intent.
        :return: System prompt string
        """
        pass

    def handle(self, data, session_attributes):
        """
        Processes the intent request.
        :param data: Request JSON data from Alexa
        :param session_attributes: The session attributes
        :return: Response dict
        """
        user_query = data['request']['intent']['slots']['Query']['value']

        # Update the conversation history
        history = self.manage_conversation_history(session_attributes, user_query)

        # Create Alexa response after querying ChatGPT
        return self.create_response(history, session_attributes)