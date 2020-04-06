from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, URL, InputRequired


class PhraseForm(FlaskForm):
    """Form for adding phrases."""

    phrase = TextAreaField('Word or Phrase', validators=[DataRequired()])