from core import Base
import sqlalchemy as db
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
from collections import namedtuple
from datetime import datetime


# DB EXTRAS
class Model:
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

class TimeMixin:
    created = db.Column(db.DateTime, default=datetime.utcnow)
    modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# END DB EXTRAS
