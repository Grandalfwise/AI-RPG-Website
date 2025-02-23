import os

from flask import Flask, render_template, request, jsonify
import requests
import re
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv('.env')
API_TOKEN = os.getenv('API_TOKEN')

API_BASE_URL = "https://teatree.chat/api/chat/completions"
HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}


# Sample RPG story prompts
STORIES = {
    "dark_forest": "You find yourself lost in a dark forest, surrounded by eerie sounds.",
    "space_adventure": "You wake up in a spaceship, alarms blaring. Something is wrong.",
    "medieval_quest": "A royal messenger hands you a scroll. The king needs your help."
}


def clean_choice(choice):
    """Cleans AI-generated choice text by removing numbers, colons, and extra spaces."""
    return re.sub(r"^\s*CHOICE\s*\d+\s*[:.-]?\s*", "", choice, flags=re.IGNORECASE).strip()


def run_ai(model, messages):
    """Send a conversation to the AI and return its response."""
    try:
        response = requests.post(
            API_BASE_URL,
            headers=HEADERS,
            json={
                "model": model,
                "messages": messages
            }
        )

        if response.status_code != 200:
            print(f"AI Request Failed: {response.status_code} - {response.text}")  # Debugging
            return {"error": f"AI request failed with status {response.status_code}"}

        return response.json()

    except Exception as e:
        print(f"AI Request Exception: {e}")  # Debugging
        return {"error": "Exception during AI request"}


def parse_ai_response(ai_response_data):
    #Parses AI response into story and choices, ensuring no missing choices.
    if not isinstance(ai_response_data, str):
        print(f"Unexpected AI Response Format: {ai_response_data}")  # Debugging
        return "Something went wrong in the story.", ["Try again", "Reload", "Wait"]

    parts = ai_response_data.split("###")

    # Ensure at least 4 parts (Story + 3 Choices)
    while len(parts) < 4:
        parts.append(f"Option {len(parts)}")  # Fill missing choices

    story_update = parts[0].replace("STORY_TEXT:", "").strip()

    choices = [clean_choice(choice) for choice in parts[1:4]]

    return story_update, choices


@app.route('/')
def home():
    return render_template('index.html', stories=STORIES)


@app.route('/start_game', methods=['POST'])
def start_game():
    """Start the game with a selected story."""
    data = request.json
    story_key = data.get('story_key')

    if story_key not in STORIES:
        return jsonify({"error": "Invalid story selected"}), 400

    initial_story = STORIES[story_key]

    # Ask AI to generate three choices with clear structure
    messages = [
        {"role": "system",
         "content": "You are an AI Dungeon Master. Keep responses under 100 words. Format response as: STORY_TEXT###CHOICE 1###CHOICE 2###CHOICE 3."},
        {"role": "user",
         "content": f"The story starts: {initial_story}. What happens next, and what are three choices the player can make?"}
    ]

    response = run_ai("roleplay-ai", messages)

    if "error" in response:
        return jsonify({"error": "AI request failed"}), 500

    # Extract and parse the AI response properly
    ai_response_data = response.get("choices", [{}])[0].get("message", {}).get("content", "")
    story_update, choices = parse_ai_response(ai_response_data)

    return jsonify({"story": story_update, "choices": choices})


@app.route('/next_move', methods=['POST'])
def next_move():
    data = request.json
    user_choice = data.get('choice')

    if not user_choice:
        return jsonify({"error": "Invalid choice"}), 400

    messages = [
        {"role": "system",
         "content": "You are an AI Dungeon Master. Keep responses under 100 words. Format response as: STORY_TEXT###CHOICE1###CHOICE2###CHOICE3."},
        {"role": "user",
         "content": f"The player chooses: {user_choice}. What happens next, and what are three choices the player can make?"}
    ]

    response = run_ai("roleplay-ai", messages)

    if "error" in response:
        return jsonify({"error": "AI request failed"}), 500

    # Extract and parse the AI response properly
    ai_response_data = response.get("choices", [{}])[0].get("message", {}).get("content", "")
    story_update, choices = parse_ai_response(ai_response_data)

    return jsonify({"story_update": story_update, "choices": choices})


if __name__ == '__main__':
    app.run(debug=True)