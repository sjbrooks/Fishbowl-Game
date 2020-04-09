"""Create data schema."""

from app import db
from models import Phrase, DrawnPhrase


db.drop_all()
db.create_all()