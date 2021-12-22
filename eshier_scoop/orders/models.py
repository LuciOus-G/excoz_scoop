# from core import Base
from eshier_scoop.helpers import model
from tortoise.models import Model
from tortoise import fields

from eshier_scoop.organizations.models import Organizations


class Orders(Model, model.Model, model.TimeMixin):
    organization = fields.ForeignKeyField('models.Organizations')
    order_number = fields.IntField(unique=True, null=False)
    total_price = fields.DecimalField
    client_scoop = fields.IntField()
    is_complete = fields.BooleanField(default=False)
    purchase_type = fields.IntField()

    class Meta:
        table="core_orders"

