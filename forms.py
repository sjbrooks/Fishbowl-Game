from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class PhraseForm(FlaskForm):
    """Form for adding phrases."""

    phrase = StringField('Word or Phrase', validators=[DataRequired()])