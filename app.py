import os

from flask import Flask, render_template, request, flash, redirect

# revisit for authentication 
# from flask import session, g

from flask_debugtoolbar import DebugToolbarExtension

from forms import PhraseForm
from models import db, connect_db, Phrase
from secrets import SECRET_KEY

# Come back to idea of authentication later
# CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
os.environ.get('DATABASE_URL', 'postgres:///fishbowl'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', SECRET_KEY)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

db.create_all()

# revisit techniques to "dry up" some of this repetition
# in pulling values from the form
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
    """
    
    Phrase.query.delete()
    db.session.commit()

    return redirect('/')