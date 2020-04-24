"""Create data schema."""

from app import db
from models import Game, Clue, Player, Team, Round, RoundType, RoundClue


db.drop_all()
db.create_all()