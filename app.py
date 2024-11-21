from openai import OpenAI
import base64
import os
from flask import Flask, request, jsonify, send_file
import pychromecast
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI()

# Set up OpenAI API key
client.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)

def get_chatgpt_response(user_input):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ],
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": "wav"}
    )
    
    # Extract the text response
    assistant_response_text = completion.choices[0].message.content
    
    # Extract and decode the audio data
    audio_data_base64 = completion.choices[0].message.audio.data
    audio_bytes = base64.b64decode(audio_data_base64)
    
    # Save the audio response to a file
    audio_filename = 'static/response.wav'
    with open(audio_filename, 'wb') as f:
        f.write(audio_bytes)
    
    return assistant_response_text, audio_filename

def play_audio_on_google_home(audio_filename):
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=["Your Google Home Mini Name"])
    if not chromecasts:
        logger.error("No Chromecast devices found")
        return
    cast = chromecasts[0]
    cast.wait()

    mc = cast.media_controller
    media_url = f'http://your_server_ip:5000/get_audio?filename={audio_filename}'
    mc.play_media(media_url, 'audio/wav')
    mc.block_until_active()

    while mc.status.player_state == 'PLAYING':
        time.sleep(0.1)

    pychromecast.discovery.stop_discovery(browser)

@app.route('/process', methods=['POST'])
def process_request():
    data = request.json
    user_input = data.get('query')
    if not user_input:
        return jsonify({'status': 'error', 'message': 'No query provided'}), 400

    try:
        # Get responses from ChatGPT
        response_text, audio_filename = get_chatgpt_response(user_input)
        logger.info(f"ChatGPT Response: {response_text}")
    except Exception as e:
        logger.error(f"Error with OpenAI API: {e}")
        return jsonify({'status': 'error', 'message': 'OpenAI API Error'}), 500

    try:
        # Play audio on Google Home Mini
        play_audio_on_google_home(audio_filename)
    except Exception as e:
        logger.error(f"Error playing audio on Google Home: {e}")
        return jsonify({'status': 'error', 'message': 'Playback Error'}), 500

    return jsonify({'status': 'success'}), 200

@app.route('/get_audio')
def get_audio():
    audio_filename = request.args.get('filename', default='static/response.wav', type=str)
    if os.path.exists(audio_filename):
        return send_file(audio_filename, mimetype='audio/wav')
    else:
        return jsonify({'status': 'error', 'message': 'Audio file not found'}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))