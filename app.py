from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'secrekey'

# Neighborhoods organized by borough
neighborhoods = {
    "Manhattan": ["Harlem", "Chelsea", "SoHo", "Tribeca", "Inwood", "Battery Park"],
    "Brooklyn": ["Williamsburg", "Bushwick", "Park Slope", "DUMBO", "Flatbush"],
    "Queens": ["Astoria", "Flushing", "Jamaica", "Forest Hills", "Long Island City"],
    "Bronx": ["Fordham", "Riverdale", "Mott Haven", "Pelham Bay"],
    "Staten Island": ["St. George", "Tottenville", "Great Kills"]
}

@app.route('/')
def index():
    return render_template('index.html', boroughs=neighborhoods.keys())

@app.route('/start', methods=['POST'])
def start():
    borough = request.form['borough']
    answer = random.choice(neighborhoods[borough])
    session['answer'] = answer.lower()
    session['hints'] = {
        "borough": borough,
        "first_letter": answer[0],
        "length": len(answer)
    }
    session['guesses'] = []
    return redirect(url_for('game'))

@app.route('/game', methods=['GET', 'POST'])
def game():
    message = ""
    if request.method == 'POST':
        guess = request.form['guess'].lower()
        session['guesses'].append(guess)

        if guess == session['answer']:
            message = "🎉 Correct! You guessed the neighborhood!"
        else:
            message = "❌ Nope! Try again."

    return render_template(
        'game.html',
        hints=session['hints'],
        guesses=session['guesses'],
        message=message
    )

if __name__ == '__main__':
    app.run(debug=True)
