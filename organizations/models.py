from core import Base
from helpers import model

class Orders(model.Model, model.TimeMixin):
    __tablename__ = 'core_order'

