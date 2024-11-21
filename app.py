from openai import OpenAI
import os
from flask import Flask, request, jsonify
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI()

# Set up OpenAI API key
client.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

def get_chatgpt_response(user_input):
    try:
        completion = client.chat.completions.create(
            model="gpt-4",  # Ensure this model is available in your OpenAI account
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.7
        )
        response_text = completion.choices[0].message.content
        return response_text
    except Exception as e:
        logger.error(f"Error communicating with OpenAI: {e}")
        return "I'm sorry, I couldn't process that request."

@app.route('/alexa', methods=['POST'])
def alexa_webhook():
    data = request.get_json()
    logger.info(f"Received request: {data}")

    if not data:
        return jsonify({'status': 'failure', 'message': 'No data received'}), 400

    request_type = data.get('request', {}).get('type')

    if request_type == 'LaunchRequest':
        response = {
            'version': '1.0',
            'response': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': 'Welcome to Egner AI Assistant. How can I help you today?'
                },
                'shouldEndSession': False
            }
        }
        return jsonify(response)

    elif request_type == 'IntentRequest':
        intent_name = data['request']['intent']['name']
        logger.info(f"Intent: {intent_name}")

        if intent_name == 'ChatGPTIntent':
            user_query = data['request']['intent']['slots']['Query']['value']
            logger.info(f"User Query: {user_query}")
            chatgpt_response = get_chatgpt_response(user_query)

            response = {
                'version': '1.0',
                'response': {
                    'outputSpeech': {
                        'type': 'PlainText',
                        'text': chatgpt_response
                    },
                    'shouldEndSession': False
                }
            }
            return jsonify(response)

        else:
            response = {
                'version': '1.0',
                'response': {
                    'outputSpeech': {
                        'type': 'PlainText',
                        'text': "I'm sorry, I didn't get that. Can you repeat?"
                    },
                    'shouldEndSession': False
                }
            }
            return jsonify(response)

    else:
        response = {
            'version': '1.0',
            'response': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': "I'm sorry, I can't dooo that."
                },
                'shouldEndSession': True
            }
        }
        return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))