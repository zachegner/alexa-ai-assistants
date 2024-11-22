import os
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI()
        self.client.api_key = os.getenv('OPENAI_API_KEY')
    
    def get_response(self, conversation_history, model="gpt-4o-mini", max_tokens=150, temperature=0.7):
        try:
            logger.info(f"Sending to OpenAI: {conversation_history}")
            completion = self.client.chat.completions.create(
                model=model,
                messages=conversation_history,
                max_tokens=max_tokens,
                temperature=temperature
            )
            response_text = completion.choices[0].message.content
            logger.info(f"Response from OpenAI: {response_text}")
            return response_text
        except Exception as e:
            logger.error(f"Error communicating with OpenAI: {e}")
            return "I'm sorry, I couldn't process that request."