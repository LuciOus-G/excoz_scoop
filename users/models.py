from datetime import datetime

import sqlalchemy as db
from helpers import model
from utils import settings
from core import Base

class Users(Base, model.Model, model.TimeMixin):
    __tablename__ = 'glob_users'

    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(512))
    salt = db.Column(db.String(512))
    profile_pic = db.Column(db.String(1000), nullable=True, default=settings.DEFAULT_PIC)
    origin_scoop = db.Column(db.Integer())
    phone_number = db.Column(db.String(20), nullable=True)
    last_login = db.Column(db.DateTime, default=datetime.now())
