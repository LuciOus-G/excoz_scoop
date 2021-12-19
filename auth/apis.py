from fastapi import APIRouter, Request, Depends
from fastapi.encoders import jsonable_encoder as jsonify
from binascii import hexlify
import hashlib
import os

from users.schemas import s_users
from users.models import Users
from core import db
from ._helpers import salt_generator, hashes_password
from utils import settings

auth_r = APIRouter(prefix='/eshier/auth', tags=['Authentications'])


@auth_r.post('/login')
def login(request: Request):
    pass


@auth_r.post('/register')
def register(request: Request, users_data=Depends(s_users.as_form)):
    salt = hexlify(salt_generator())
    hash_password = hashes_password(salt, users_data.password)
    hash_salt = hash_password + salt

    new_user = Users(
        first_name=users_data.first_name,
        last_name=users_data.last_name,
        email=users_data.email,
        password=hash_salt,
        phone_number=users_data.phone_number,
        salt=salt,
        origin_scoop=21,
        profile_pic=users_data.profil_pic if users_data.profil_pic else settings.DEFAULT_PIC
    )

    if new_user:
        db.add(new_user)
        db.commit()
    return new_user
