from flask import Blueprint, render_template, request, jsonify
from run_ai import run_ai, clean_choice, convo_history


# Sample RPG story prompts
STORIES = {
    "dark_forest": "You find yourself lost in a dark forest, surrounded by eerie sounds.",
    "space_adventure": "You wake up in a spaceship, alarms blaring. Something is wrong.",
    "medieval_quest": "A royal messenger hands you a scroll. The king needs your help."
}

main_bp = Blueprint('main', __name__)


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


@main_bp.route('/')
def home():
    return render_template('index.html', stories=STORIES)


@main_bp.route('/start_game', methods=['POST'])
def start_game():
    """Start the game with a selected story."""
    data = request.json
    story_key = data.get('story_key')

    if story_key not in STORIES:
        return jsonify({"error": "Invalid story selected"}), 400

    initial_story = STORIES[story_key]

    # Ask AI to generate three choices with clear structure
    messages = f"The story starts: {initial_story}. What happens next, and what are three choices the player can make?"

    convo_history.append({'role': 'user', 'content': messages})


    response = run_ai()

    if "error" in response:
        return jsonify({"error": "AI request failed"}), 500

    # Extract and parse the AI response properly
    ai_response_data = response.get("choices", [{}])[0].get("message", {}).get("content", "")
    story_update, choices = parse_ai_response(ai_response_data)

    return jsonify({"story": story_update, "choices": choices})


@main_bp.route('/next_move', methods=['POST'])
def next_move():
    data = request.json
    user_choice = data.get('choice')

    if not user_choice:
        return jsonify({"error": "Invalid choice"}), 400
    
    messages = f"The player chooses: {user_choice}. What happens next, and what are three choices the player can make?"

    convo_history.append({'role': 'user', 'content': messages})
    print(f"Conversation History: {convo_history}")

    response = run_ai()

    if "error" in response:
        return jsonify({"error": "AI request failed"}), 500

    # Extract and parse the AI response properly
    ai_response_data = response.get("choices", [{}])[0].get("message", {}).get("content", "")
    story_update, choices = parse_ai_response(ai_response_data)

    return jsonify({"story_update": story_update, "choices": choices})

@main_bp.route('/restart', methods=['POST'])
def restart():
    convo_history.clear()
    return jsonify({"message": "Game restarted."})