from flask import Flask, render_template, request, redirect, url_for, session
import random
from lists import neighborhoods, subway_lines  

app = Flask(__name__)
app.secret_key = 'lesecrekey'



@app.route('/')
def index():
    return render_template('index.html', boroughs=neighborhoods.keys())


@app.route('/start_game', methods=['POST'])
def start_game():
    mode = request.form['mode']
    session['lives'] = 5  # <-- Add this

    if mode == 'neighborhood':
        borough = request.form['borough']
        chosen = random.choice(neighborhoods[borough])
        session['game_mode'] = 'neighborhood'
        session['answer'] = chosen['name'].lower()
        session['hint'] = chosen['hint']
        session['extra_hint'] = chosen['extra_hint']
        session['borough'] = borough
        session['guesses'] = []
        return redirect(url_for('game_neighborhood'))

    elif mode == 'subway':
        chosen_line = random.choice(subway_lines)
        session['game_mode'] = 'subway'
        session['answer'] = chosen_line['line'].lower()
        session['start'] = chosen_line['start']
        session['end'] = chosen_line['end']
        session['guesses'] = []
        return redirect(url_for('game_subway'))


@app.route('/game/neighborhood', methods=['GET', 'POST'])
def game_neighborhood():
    borough = session.get('borough')
    answer = session.get('answer')
    hint = session.get('hint')
    extra_hint = session.get('extra_hint')
    guesses = session.get('guesses', [])
    lives = session.get('lives', 5)
    message = None
    game_over = False

    if request.method == "POST":
        guess = request.form.get("guess", "").strip().lower()

        if guess == answer:
            message = "Correct! ✅"
            game_over = True
        else:
            lives -= 1
            session['lives'] = lives
            guesses.append(guess)
            session['guesses'] = guesses

            if lives == 0:
                message = f"Out of lives! ❌ The answer was: {answer.title()}"
                game_over = True
            else:
                message = f"Wrong guess! ❌ You have {lives} lives left."

        return render_template("game_neighborhood.html",
            borough=borough,
            hint=hint,
            extra_hint=extra_hint,
            message=message,
            guesses=guesses,
            lives=lives,
            game_over=game_over)

    return render_template("game_neighborhood.html",
        borough=borough,
        hint=hint,
        extra_hint=extra_hint,
        message=None,
        guesses=guesses,
        lives=lives,
        game_over=False)


@app.route('/game/subway', methods=['GET', 'POST'])
def game_subway():
    message = ""
    start = session.get('start')
    end = session.get('end')
    answer = session.get('answer')
    guesses = session.get('guesses', [])
    lives = session.get('lives', 5)
    game_over = False

    if request.method == 'POST':
        guess = request.form['guess'].strip().lower()

        if guess == answer:
            message = "✅ You got the subway line right!"
            game_over = True
        else:
            lives -= 1
            session['lives'] = lives
            guesses.append(guess)
            session['guesses'] = guesses

            if lives == 0:
                message = f"Out of lives! ❌ The answer was: {answer.upper()}"
                game_over = True
            else:
                message = f"Wrong! ❌ You have {lives} lives left."

    return render_template(
        'game_subway.html',
        start=start,
        end=end,
        guesses=guesses,
        message=message,
        lives=lives,
        game_over=game_over
    )



if __name__ == '__main__':
    app.run(debug=True)
