# from core import Base
from eshier_scoop.helpers import model
from tortoise.models import Model
from tortoise import fields

class Organizations(Model, model.Model, model.TimeMixin):
    name = fields.CharField(max_length=255, null=False)
    is_subscribe = fields.BooleanField(default=False)
    date_expire = fields.DateField(null=True)
    class Meta:
        table='core_organizations'

