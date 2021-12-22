# from core import Base
from eshier_scoop.helpers import model
from tortoise.models import Model
from tortoise import fields
from eshier_scoop.utils import settings

class Organizations(Model, model.Model, model.TimeMixin):
    name = fields.CharField(max_length=255, null=False)
    is_subscribe = fields.BooleanField(default=False)
    date_expire = fields.DateField(null=True)
    org_logo = fields.CharField(max_length=1000, null=False, default=settings.DEFAULT_PIC)
    max_user = fields.IntField(null=False, default=6)
    org_type = fields.CharField(max_length=1000, null=False)
    folder_id = fields.CharField(max_length=255, null=True)

    class Meta:
        table='core_organizations'

