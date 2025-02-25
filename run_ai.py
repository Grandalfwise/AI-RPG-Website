import os
from dotenv import load_dotenv
import requests
import re

load_dotenv('.env')
API_TOKEN = os.getenv('API_TOKEN')
API_BASE_URL = "https://chat.teatree.chat/api/chat/completions"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

model = "roleplay-ai"
convo_history = []

instructions = [
    {"role": "system",
      "content": "You are an AI Dungeon Master. Keep responses under 100 words. Format response as: STORY_TEXT###CHOICE 1###CHOICE 2###CHOICE 3."},
]

def clean_choice(choice):
    return re.sub(r"^\s*(CHOICE)?\s*\d+\s*[-:.]?\s*", "", choice, flags=re.IGNORECASE).strip()

def run_ai():
    """Send a conversation to the AI and return its response."""
    try:
        response = requests.post(
            API_BASE_URL,
            headers=HEADERS,
            json={
                "model": model,
                "messages": convo_history + instructions
            }
        )

        if response.status_code != 200:
            print(f"AI Request Failed: {response.status_code} - {response.text}")  # Debugging
            return {"error": f"AI request failed with status {response.status_code}"}

        return response.json()

    except Exception as e:
        print(f"AI Request Exception: {e}")  # Debugging
        return {"error": "Exception during AI request"}