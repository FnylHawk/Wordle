from flask import Blueprint, request, jsonify
import random

# Create a Blueprint
wordle_game_bp = Blueprint('wordle_game', __name__)

# Sample word list for Wordle
word_list = ["slate", "lucky", "maser", "gapes", "wages", "apple", "grape", "peach", "lemon", "berry"]

def evaluate_guess(guess, answer):
    feedback = []
    for i in range(5):
        if guess[i] == answer[i]:
            feedback.append('O')  # Correct position
        elif guess[i] in answer:
            feedback.append('X')  # Wrong position
        else:
            feedback.append('-')  # Not in word
    return ''.join(feedback)

def get_next_guess(guess_history, evaluation_history):
    if not guess_history:
        return random.choice(word_list)

    possible_guesses = set(word_list)

    for guess, evaluation in zip(guess_history, evaluation_history):
        for i in range(5):
            if evaluation[i] == 'O':
                # Keep only words with the same letter at this position
                possible_guesses.intersection_update({word for word in possible_guesses if word[i] == guess[i]})
            elif evaluation[i] == 'X':
                # Keep only words that contain the letter, but not at this position
                possible_guesses.intersection_update({word for word in possible_guesses if guess[i] in word and word[i] != guess[i]})
            elif evaluation[i] == '-':
                # Remove words that contain this letter
                possible_guesses.difference_update({word for word in possible_guesses if guess[i] in word})

    return random.choice(list(possible_guesses)) if possible_guesses else random.choice(word_list)


@wordle_game_bp.route('/wordle-game', methods=['POST'])
def wordle_game():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    guess_history = data.get("guessHistory", [])
    evaluation_history = data.get("evaluationHistory", [])
    
    next_guess = get_next_guess(guess_history, evaluation_history)
    
    return jsonify({"guess": next_guess})
