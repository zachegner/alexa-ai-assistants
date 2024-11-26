# Alexa AI Personal Assistant

**Have you ever wished Siri or Alexa could truly understand and assist you like a personal assistant?** This project integrates OpenAI's ChatGPT with Amazon Alexa using Python and Flask to create a more intelligent and conversational voice assistant.

## Features
- **Natural Language Understanding**: Engage in more natural and context-aware conversations.
- **Customizable Skills**: Easily add new skills tailored to specific needs.
- **Persistent Session Management**: Maintain conversation history for better context retention.
- **Scalable Architecture**: Modular design allows seamless integration of additional functionalities.


## Technologies Used
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [OpenAI GPT-4-mini](https://openai.com/)
- [Amazon Alexa Skills Kit](https://developer.amazon.com/en-US/docs/alexa/ask-overviews/what-is-the-alexa-skills-kit.html)

## Setup Instructions
1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/chatgpt-alexa-assistant.git
   cd chatgpt-alexa-assistant
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ``` 

3. **Configure Environment Variables**
    ```bash
    OPENAI_API_KEY=your_openai_api_key
    CHAT_SKILL_ID=your_chat_skill_id
    FUNNY_SKILL_ID=your_funny_skill_id
    PORT=5000
    ```    

4. **Run the Flask App**
   ```bash
   python app.py
   ```       
  
5. **Configure Alexa Skill**
Link the webhook URL to your Alexa skill in the Amazon Developer Console.

## Usage
##### Launch the Skill
- "Alexa, open ChatGPT Assistant."

##### Interact with ChatGPT
- "Tell me a joke."
- "What's the weather like today?"

## License
This project is licensed under the MIT License.

## Contact
LinkedIn: zach-egner
Email: zach@zachegner.com