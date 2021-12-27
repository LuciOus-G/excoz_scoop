from datetime import datetime
from tortoise import fields
from tortoise.models import Model
from eshier_scoop.helpers import model
from tortoise.contrib.pydantic import pydantic_model_creator

class Items(Model, model.Model, model.TimeMixin):
    name = fields.CharField(max_length=255)
    stock_left = fields.IntField()
    used_stock = fields.IntField(null=True)
    total_restock = fields.IntField(null=True)
    single_price = fields.DecimalField(max_digits=50, decimal_places=2, null=True)
    organization: fields.ForeignKeyRelation = fields.ForeignKeyField('models.Organizations',
                                                                     related_name='item_organization')
    created_by: fields.ForeignKeyRelation = fields.ForeignKeyField('models.Users',
                                                                   related_name='item_users')

    def tortoise_to_pydantic(self):
        _pydantic = pydantic_model_creator(Items, name='Items')
        in_pydantic = pydantic_model_creator(Items, name='ItemsIn', exclude_readonly=True)
        return _pydantic, in_pydantic

    class Meta:
        table = 'core_items'

class ItemsPieces(Model, model.SoftModel, model.SoftTimeMixin):
    restock = fields.IntField()
    items: fields.ForeignKeyRelation = fields.ForeignKeyField('models.Items', related_name='item_id')
    created_by: fields.ForeignKeyRelation = fields.ForeignKeyField('models.Users', related_name='item_pieces_users')

    def tortoise_to_pydantic(self):
        _pydantic = pydantic_model_creator(ItemsPieces, name='ItemsPieces')
        in_pydantic = pydantic_model_creator(ItemsPieces, name='ItemsPiecesIn', exclude_readonly=True)
        return _pydantic, in_pydantic

    class Meta:
        table = 'core_items_pieces'