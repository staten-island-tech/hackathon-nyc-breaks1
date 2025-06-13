from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'secrekey'

# Neighborhoods organized by borough
neighborhoods = {
    "Manhattan": [
        {"name": "Harlem", "hint": "Known for its rich African-American culture and the Apollo Theater."},
        {"name": "Chelsea", "hint": "Famous for art galleries and the High Line."},
        {"name": "SoHo", "hint": "Name stands for 'South of Houston Street', full of boutiques and lofts."},
        {"name": "Tribeca", "hint": "Hosts a major film festival and is known for cobblestone streets."},
        {"name": "Inwood", "hint": "Northern tip of Manhattan, near Inwood Hill Park."},
        {"name": "Battery Park", "hint": "Located at Manhattan’s southern tip, near ferries to the Statue of Liberty."},
        {"name": "Upper East Side", "hint": "Known for luxury shopping and Museum Mile."},
        {"name": "Washington Heights", "hint": "Home to the Cloisters and large Dominican population."}
    ],
    "Brooklyn": [
        {"name": "Williamsburg", "hint": "Hipster central with street art and indie music."},
        {"name": "Bushwick", "hint": "Rising art scene and former industrial vibe."},
        {"name": "Park Slope", "hint": "Family-friendly with historic brownstones."},
        {"name": "DUMBO", "hint": "Acronym for 'Down Under the Manhattan Bridge Overpass'."},
        {"name": "Flatbush", "hint": "Diverse area known for Caribbean culture."},
        {"name": "Crown Heights", "hint": "Known for the West Indian Day Parade."},
        {"name": "Red Hook", "hint": "Isolated waterfront area with great lobster rolls."}
    ],
    "Queens": [
        {"name": "Astoria", "hint": "Famous for Greek food and museums."},
        {"name": "Flushing", "hint": "Home to a large Chinatown and the Mets stadium."},
        {"name": "Jamaica", "hint": "Major transit hub with cultural diversity."},
        {"name": "Forest Hills", "hint": "Tennis history and Tudor-style homes."},
        {"name": "Long Island City", "hint": "Rapidly developing with art spaces and skyscrapers."},
        {"name": "Sunnyside", "hint": "Known for its historic gardens and quiet streets."}
    ],
    "Bronx": [
        {"name": "Fordham", "hint": "Home to Fordham University and the Bronx Zoo."},
        {"name": "Riverdale", "hint": "Leafy suburban-style neighborhood near the Hudson."},
        {"name": "Mott Haven", "hint": "Up-and-coming arts district."},
        {"name": "Pelham Bay", "hint": "Next to NYC’s largest park—Pelham Bay Park."},
        {"name": "Belmont", "hint": "Known as the Bronx’s Little Italy."}
    ],
    "Staten Island": [
        {"name": "St. George", "hint": "Staten Island Ferry terminal and harbor views."},
        {"name": "Tottenville", "hint": "Southernmost neighborhood in NYC."},
        {"name": "Great Kills", "hint": "Known for its marina and natural beauty."},
        {"name": "New Dorp", "hint": "One of the oldest Staten Island settlements."},
        {"name": "Stapleton", "hint": "Historic district with a waterfront redevelopment."}
    ]
}



@app.route('/')
def index():
    return render_template('index.html', boroughs=neighborhoods.keys())


@app.route('/start', methods=['POST'])
def start():
    borough = request.form['borough']
    chosen = random.choice(neighborhoods[borough])
    session['answer'] = chosen['name'].lower()
    session['hints'] = {
        "borough": borough,
        "first_letter": chosen['name'][0],
        "length": len(chosen['name']),
        "extra_hint": chosen['hint']  # new hint string
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
