import os
from flask import Flask, request, jsonify
import logging
from utils.openai_client import OpenAIClient
from config.skills_config import SKILLS

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
openai_client = OpenAIClient()

# Initialize Flask app
app = Flask(__name__)

def get_chatgpt_response(conversation_history):
    return openai_client.get_response(conversation_history)

@app.route('/alexa', methods=['POST'])
def alexa_webhook():
    data = request.get_json()
    logger.info(f"Received request: {data}")

    if not data:
        return jsonify({'status': 'failure', 'message': 'No data received'}), 400

    # Extract applicationId to identify the skill
    application_id = data.get('session', {}).get('application', {}).get('applicationId')
    logger.info(f"Application ID: {application_id}")

    # Validate if the application_id is recognized
    SkillClass = SKILLS.get(application_id)
    if not SkillClass:
        logger.warning(f"Unrecognized application ID: {application_id}")
        return jsonify({
            'version': '1.0',
            'response': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': "I'm sorry, I don't recognize that skill."
                },
                'shouldEndSession': True
            }
        })

    # Instantiate the skill handler
    skill_handler = SkillClass(get_chatgpt_response)

    # Get session attributes
    session_attributes = data.get('session', {}).get('attributes', {})
    request_type = data.get('request', {}).get('type')

    if request_type == 'LaunchRequest':
        # Initialize session history if not present
        if 'history' not in session_attributes:
            session_attributes['history'] = [{
                "role": "system",
                "content": skill_handler.get_system_prompt()
            }]

        response = {
            'version': '1.0',
            'sessionAttributes': session_attributes,
            'response': {
                'outputSpeech': {
                    'type': 'PlainText',
                    'text': 'Welcome! How can I assist you today?'
                },
                'shouldEndSession': False
            }
        }
        return jsonify(response)

    elif request_type == 'IntentRequest':
        intent_name = data['request']['intent']['name']
        logger.info(f"Intent: {intent_name}")

        if intent_name == 'HelpIntent':
            response = {
                'version': '1.0',
                'response': {
                    'outputSpeech': {
                        'type': 'PlainText',
                        'text': 'How can I assist you today?'
                    },
                    'shouldEndSession': False
                }
            }
            return jsonify(response)

        elif intent_name == 'CancelIntent' or intent_name == 'StopIntent':
            return jsonify({
                'version': '1.0',
                'response': {
                    'outputSpeech': {
                        'type': 'PlainText',
                        'text': 'Goodbye!'
                    },
                    'shouldEndSession': True
                }
            })

        else:
            # Delegate intent handling to the skill-specific handler
            response_content = skill_handler.handle_intent(data, session_attributes)
            return jsonify({
                'version': '1.0',
                'sessionAttributes': response_content.get('sessionAttributes', session_attributes),
                'response': {
                    'outputSpeech': response_content['outputSpeech'],
                    'shouldEndSession': response_content['shouldEndSession']
                }
            })

    else:
        logger.warning(f"Unhandled request type: {request_type}")
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