"""SQLAlchemy models for Fish Bowl."""

# revisit when we have game id's and want to verify which game you're a part of
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


class Game(db.Model):
    """Games class."""

    __tablename__ = 'games'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    current_team = db.Column(db.Text,
                             nullable=False)

    current_round = db.Column(db.Integer,
                              nullable=False)

    def __repr__(self):
        g = self
        return f"<Like #{g.id}: {g.current_team} {g.current_round}>"


class Clue(db.Model):
    """Clue class."""

    __tablename__ = 'clues'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    phrase = db.Column(db.Text,
                       nullable=False)

    player_id = db.Column(db.Text,
                          db.ForeignKey('players.id'))

    game_id = db.Column(db.Text,
                        db.ForeignKey('games.id'))

    player = db.relationship('Player', backref='clues')

    game = db.relationship('Game', backref='clues')

    def __repr__(self):
        c = self
        return f"<Like #{c.id}: {c.phrase} {c.player_id} {c.game_id}>"


class Player(db.Model):
    """Player class."""

    __tablename__ = 'players'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = db.Column(db.Text,
                     nullable=False)

    turn = db.Column(db.Boolean,
                     default=False)

    team_id = db.Column(db.Text,
                        db.ForeignKey('teams.id'))

    team = db.relationship('Team', backref='players')

    def __repr__(self):
        p = self
        return f"<Like #{p.id}: {p.name} {p.turn} {p.team_id}>"


class Team(db.Model):
    """Team class."""

    __tablename__ = 'teams'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = db.Column(db.Text,
                     nullable=False)

    game_id = db.Column(db.Text,
                        db.ForeignKey('games.id'))

    game = db.relationship('Game', backref='teams')

    def __repr__(self):
        t = self
        return f"<Like #{t.id}: {t.name} {t.game_id}>"


class Round(db.Model):
    """Round class."""

    __tablename__ = 'rounds'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    number = db.Column(db.Integer,
                       nullable=False)

    game_id = db.Column(db.Text,
                        db.ForeignKey('games.id'))

    game = db.relationship('Game', backref='rounds')

    clues = db.relationship('Clue',
                            secondary='round_clues',
                            backref='rounds')

    def __repr__(self):
        r = self
        return f"<Like #{r.id}: {r.round} {r.game_id}>"


class RoundType(db.Model):
    """RoundType class."""

    __tablename__ = 'round_types'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    round_type = db.Column(db.Text,
                           nullable=False)

    round_id = db.Column(db.Text,
                         db.ForeignKey('rounds.id'))

    round = db.relationship('Round', backref='round_types')

    def __repr__(self):
        rt = self
        return f"<Like #{rt.id}: {rt.round_type} {rt.round_id}>"


class RoundClue(db.Model):
    """RoundClue class."""

    __tablename__ = 'round_clues'

    clue_id = db.Column(db.Integer,
                        db.ForeignKey('clues.id'),
                        primary_key=True)
    round_id = db.Column(db.Integer,
                         db.ForeignKey('rounds.id'),
                         primary_key=True)

    drawn = db.Column(db.Boolean,
                      default=False)

    def __repr__(self):
        rc = self
        return f"<Like #{rc.clue_id} {rc.round_id}: {rc.drawn}>"
