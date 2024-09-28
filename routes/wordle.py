from flask import Blueprint, request, jsonify

wordle_game = Blueprint('wordle_game', __name__)

# Sample word list for Wordle guessing
WORD_LIST = ["slate", "lucky", "maser", "gapes", "wages", "input", "other", "words"]

# Function to determine the next guess based on previous evaluations
def get_next_guess(guess_history, evaluation_history):
    # Filter out already guessed words
    available_words = [word for word in WORD_LIST if word not in guess_history]
    
    if not available_words:
        return None

    # Simple logic to pick the next word from available words
    return available_words[0]

# POST endpoint for the Wordle game
@wordle_game.route('/wordle-game', methods=['POST'])
def handle_wordle():
    data = request.json

    # Retrieve guess and evaluation history from request data
    guess_history = data.get("guessHistory", [])
    evaluation_history = data.get("evaluationHistory", [])
    
    # Check if the game is won (evaluation has "OOOOO")
    if "OOOOO" in evaluation_history:
        return jsonify({
            "guess": guess_history[-1],
            "guessHistory": guess_history,
            "evaluationHistory": evaluation_history,
            "message": "Game already won!"
        })

    # Check if the game is over due to 6 guesses
    if len(guess_history) >= 6:
        return jsonify({
            "guess": guess_history[-1],
            "guessHistory": guess_history,
            "evaluationHistory": evaluation_history,
            "message": "Game over, maximum number of guesses reached!"
        }), 400

    # Find the next guess based on previous guesses and evaluations
    next_guess = get_next_guess(guess_history, evaluation_history)

    if not next_guess:
        return jsonify({"error": "No more guesses available"}), 400
    
    # Add the next guess to the guess history
    guess_history.append(next_guess)

    # Placeholder: pretend we get masked evaluations (as per the game rules)
    # In reality, you would calculate the actual evaluation based on the word
    if len(evaluation_history) < 5:
        evaluation_history.append("?-X-X")
    else:
        evaluation_history.append("OOOOO")  # Correct guess feedback on the final guess

    # Check if the current guess wins the game
    if evaluation_history[-1] == "OOOOO":
        return jsonify({
            "guess": next_guess,
            "message": "Correct! Game won in {} guesses".format(len(guess_history))
        })

    # Otherwise, return the next guess
    return jsonify({
        "guess": next_guess,
    })
