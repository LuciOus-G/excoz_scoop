from tortoise import fields
from datetime import datetime


# DB EXTRAS
class Model:
    id = fields.BigIntField(pk=True)
    is_active = fields.BooleanField(null=False, default=True)

class TimeMixin:
    created = fields.DateField(default=datetime.utcnow())
    modified = fields.DateField(default=datetime.utcnow())

class SoftTimeMixin:
    created = fields.DateField(default=datetime.utcnow())

class SoftModel:
    id = fields.BigIntField(pk=True)


# END DB EXTRAS
