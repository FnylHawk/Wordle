from flask import Flask #
from routes.wordle_game import wordle_game_bp 

app = Flask(__name__)

app.register_blueprint(wordle_game_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)