# Alexa AI Personal Assistant

![Amazon Alexa](https://img.shields.io/badge/amazon%20alexa-52b5f7?style=for-the-badge&logo=amazon%20alexa&logoColor=white) ![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) ![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white)
![GitHub repo size](https://img.shields.io/github/repo-size/zachegner/alexa-ai-assistants) ![GitHub language count](https://img.shields.io/github/languages/count/zachegner/alexa-ai-assistants) ![License](https://img.shields.io/github/license/zachegner/alexa-ai-assistants) ![GitHub stars](https://img.shields.io/github/stars/zachegner/alexa-ai-assistants?style=social)

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