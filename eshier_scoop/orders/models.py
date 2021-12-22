# from core import Base
from eshier_scoop.helpers import model
from tortoise.models import Model
from tortoise import fields

from eshier_scoop.organizations.models import Organizations


class Orders(Model, model.Model, model.TimeMixin):
    organization = fields.ForeignKeyField('models.Organizations')

    class Meta:
        table="core_orders"

