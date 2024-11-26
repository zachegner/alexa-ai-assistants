import os
from intents.chatgpt_intent import ChatGPTSkill
from intents.funny_response_intent import FunnyResponseSkill

SKILLS = {
    os.getenv('CHAT_SKILL_ID'): ChatGPTSkill,
    os.getenv('FUNNY_SKILL_ID'): FunnyResponseSkill,
}