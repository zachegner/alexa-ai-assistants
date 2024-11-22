import os
from flask import Flask, request, jsonify
import logging
from intents.chatgpt_intent import ChatGPTIntent
from intents.funny_response_intent import FunnyResponseIntent
from utils.openai_client import OpenAIClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

openai_client = OpenAIClient()

app = Flask(__name__)

INTENT_HANDLERS = {
    'ChatGPTIntent': ChatGPTIntent(openai_client.get_response),
    'FunnyResponseIntent': FunnyResponseIntent(openai_client.get_response),
}

@app.route('/alexa', methods=['POST'])
def alexa_webhook():
    data = request.get_json()
    logger.info(f"Received request: {data}")

    if not data:
        return jsonify({'status': 'failure', 'message': 'No data received'}), 400

    session_attributes = data.get('session', {}).get('attributes', {})
    request_type = data.get('request', {}).get('type')

    if request_type == 'LaunchRequest':
        session_attributes.setdefault('history', [{"role": "system", "content": "You are a helpful assistant. Keep your responses short."}])
        return jsonify({
            'version': '1.0',
            'sessionAttributes': session_attributes,
            'response': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': 'Welcome to Egner AI Assistant. How can I assist you today?'
                },
                'shouldEndSession': False
            }
        })

    elif request_type == 'IntentRequest':
        intent_name = data['request']['intent']['name']
        intent_handler = INTENT_HANDLERS.get(intent_name)

        if intent_handler:
            response_content = intent_handler.handle(data, session_attributes)
            return jsonify({
                'version': '1.0',
                'sessionAttributes': response_content.get('sessionAttributes', session_attributes),
                'response': {
                    'outputSpeech': response_content['outputSpeech'],
                    'shouldEndSession': response_content['shouldEndSession']
                }
            })

        else:
            logger.warning(f"No handler found for intent: {intent_name}")
            return jsonify({
                'version': '1.0',
                'response': {
                    'outputSpeech': {
                        'type': 'PlainText',
                        'text': "I'm sorry, I didn't understand that intent."
                    },
                    'shouldEndSession': False
                }
            })

    else:
        return jsonify({
            'version': '1.0',
            'response': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': "I'm sorry, I can't process that request."
                },
                'shouldEndSession': True
            }
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))