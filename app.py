import os

from flask import Flask, render_template, request, flash, redirect
from random import choice

# revisit for authentication 
# from flask import session, g

from flask_debugtoolbar import DebugToolbarExtension

from forms import PhraseForm
from models import db, connect_db, Phrase, DrawnPhrase
# from secrets import SECRET_KEY

# Come back to idea of authentication later
# CURR_USER_KEY = "curr_user"

CURR_MODEL = Phrase
OTHER_MODEL = DrawnPhrase
CURR_ROUND = 1

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
os.environ.get('DATABASE_URL', 'postgres:///fishbowl'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secretshh')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

db.create_all()

# revisit techniques to "dry up" some of this repetition
# in pulling values from the form


def switch_models():
    global CURR_MODEL
    global OTHER_MODEL

    CURR_MODEL, OTHER_MODEL = OTHER_MODEL, CURR_MODEL


@app.route('/', methods=['GET', 'POST'])
def homepage():
    """
    Shows the form to add a phrase to the fishbowl.
    """

    form = PhraseForm()

    if form.validate_on_submit():
        phrase = form.phrase.data
        phrase = Phrase(phrase=phrase)

        db.session.add(phrase)
        db.session.commit()
        
        return redirect('/')

    else:
        return render_template('phrase-form.html', form=form)


@app.route('/reset-game')
def reset_game():
    """
    Deletes all rows from the phrases table to start a new game.
    Reset all the default global variables for current round and models.
    """

    global CURR_ROUND
    global CURR_MODEL
    global OTHER_MODEL
    
    CURR_ROUND = 1
    CURR_MODEL = Phrase
    OTHER_MODEL = DrawnPhrase

    db.drop_all()
    db.create_all()

    return redirect('/')


@app.route('/start-game')
def start_game():
    """
    Starts the game by rendering a new page that doesn't have a submit button 
    but has a new button that allows you to draw a card
    """

    return render_template('draw-card.html')


@app.route('/draw-card')
def draw_card():
    """
    Picks a random card from database, add it to another table (drawn_cards), 
    and remove it from the current table (phrases).
    """

    rand_phrase = choice(CURR_MODEL.query.all())

    phrase = OTHER_MODEL(phrase=rand_phrase.phrase)
    phrase_curr_model = CURR_MODEL.query.filter(
                        CURR_MODEL.phrase == phrase.phrase).one()

    print("\n\n\n\nthe phrase from the current model is", phrase_curr_model.phrase)

    db.session.add(phrase)
    db.session.commit()

    db.session.delete(phrase_curr_model)
    db.session.commit()

    if db.session.query(CURR_MODEL).count() == 0:
        switch_models()

        global CURR_ROUND
        flash(f'Round {CURR_ROUND} complete!')
        CURR_ROUND += 1

        return render_template('new-round.html', phrase=phrase_curr_model)

    return render_template('draw-card.html', phrase=phrase_curr_model)
    