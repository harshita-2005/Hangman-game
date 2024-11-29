import random
from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)

# Generate a random secret key
app.secret_key = os.urandom(24)  # Securely generate a random secret key

# List of words for the hangman game
words = ['python', 'flask', 'hangman', 'developer', 'flaskapp', 'coding']

# Route to show the game page
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'word' not in session:
        # Initialize a random word and other game variables
        session['word'] = random.choice(words)
        session['guessed_letters'] = []
        session['wrong_guesses'] = 0

    word = session['word']
    guessed_letters = session['guessed_letters']
    wrong_guesses = session['wrong_guesses']

    if request.method == 'POST':
        letter = request.form['letter'].lower()
        if letter not in guessed_letters and letter.isalpha() and len(letter) == 1:
            guessed_letters.append(letter)

            if letter not in word:
                wrong_guesses += 1

        # Save the updated game state to the session
        session['guessed_letters'] = guessed_letters
        session['wrong_guesses'] = wrong_guesses

        if wrong_guesses >= 6:  # Max incorrect guesses allowed
            return render_template('index.html', word=word, guessed_letters=guessed_letters, wrong_guesses=wrong_guesses, game_over=True)

        # Check if the word is fully guessed
        if all(letter in guessed_letters for letter in word):
            return render_template('index.html', word=word, guessed_letters=guessed_letters, wrong_guesses=wrong_guesses, game_won=True)

    return render_template('index.html', word=word, guessed_letters=guessed_letters, wrong_guesses=wrong_guesses)


# Route to reset the game
@app.route('/reset', methods=['GET'])
def reset():
    session.pop('word', None)
    session.pop('guessed_letters', None)
    session.pop('wrong_guesses', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
