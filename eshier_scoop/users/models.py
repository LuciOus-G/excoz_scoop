from datetime import datetime
from tortoise import fields
from tortoise.models import Model
from eshier_scoop.helpers import model
from tortoise.contrib.pydantic import pydantic_model_creator

class Users(Model, model.Model, model.TimeMixin):
    first_name = fields.CharField(max_length=25)
    last_name = fields.CharField(max_length=20, null=False)
    email = fields.CharField(max_length=250, unique=True)
    password = fields.CharField(max_length=512)
    salt = fields.CharField(max_length=512)
    origin_scoop = fields.IntField()
    phone_number = fields.CharField(max_length=20, null=True)
    last_login = fields.DateField(default=datetime.now())
    has_organization = fields.BooleanField(default=True, null=True)
    error_message = fields.TextField(null=True)

    def tortoise_to_pydantic(self):
        _pydantic = pydantic_model_creator(Users, name='Users')
        in_pydantic = pydantic_model_creator(Users, name='UsersIn', exclude_readonly=True)
        return _pydantic, in_pydantic

    class Meta:
        table = 'glob_users'

class User_organization(Model):
    id = fields.BigIntField(pk=True)
    user = fields.ForeignKeyField('models.Users', related_name='user_organization')
    organization = fields.ForeignKeyField('models.Organizations', related_name='organization_user')

    def tortoise_to_pydantic(self):
        _pydantic = pydantic_model_creator(Users, name='UsersId')
        in_pydantic = pydantic_model_creator(Users, name='UsersIdIn', exclude_readonly=True)
        return _pydantic, in_pydantic

    class Meta:
        table = 'glob_user_organizations'
