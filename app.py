from flask import Flask
from routes.wordle import wordle_game

app = Flask(__name__)

app.register_blueprint(wordle_game)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)