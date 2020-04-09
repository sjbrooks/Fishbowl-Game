"""SQLAlchemy models for Fish Bowl."""

# revisit when we
# from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

# bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect this database to provided Flask app.

    To be called in Flask app.
    """

    db.app = app
    db.init_app(app)


class Phrase(db.Model):
    """Phrases class."""

    __tablename__ = 'phrases'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    phrase = db.Column(db.Text,
                       nullable=False)

    def __repr__(self):
        return f"<Like #{self.id}: {self.phrase}>"


class DrawnPhrase(db.Model):
    """DrawnPhrase class."""

    __tablename__ = 'drawn_cards'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    phrase = db.Column(db.Text,
                       nullable=False)

    def __repr__(self):
        return f"<Like #{self.id}: {self.phrase}>"
