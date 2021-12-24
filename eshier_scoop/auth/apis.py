from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.encoders import jsonable_encoder as jsonify
from binascii import hexlify
import hashlib
import os
from pathlib import Path
from strgen import StringGenerator as SG
from eshier_scoop.users.schemas import s_register, s_login
from eshier_scoop.users.models import Users, User_organization
# from core import db
from ._helpers import authHandler, registerFlow
from eshier_scoop.utils import settings
from ..helpers.google_drive import google
from ..organizations.models import Organizations

auth_r = APIRouter(prefix='/eshier/auth', tags=['Authentications'])


@auth_r.post('/login')
async def login(request: Request, cred=Depends(s_login)):
    _in, _out = Users().tortoise_to_pydantic()
    user = Users.get(email=cred.email)
    user_parse = await _in.from_queryset_single(user)
    handeler = authHandler()
    is_valid = await handeler.verify_password(cred.password, user_parse)

    if not user_parse.is_active:
        raise HTTPException(status_code=404, detail='user not found')

    if not is_valid:
        raise HTTPException(status_code=401, detail='username or pw wrong')
    else:
        base_response = await _out.from_queryset_single(user)
        response = base_response.dict()
        response['access_token'] = await handeler.jwt_encode_login(user_parse)
        response['token_type'] = 'Bearer'
        return jsonify(response)



@auth_r.post('/register')
async def register(request: Request, users_data=Depends(s_register.as_form)):
    salt = hexlify(authHandler().salt_generator()) # len [:128]
    hash_password = authHandler().hashes_password(salt, users_data.password) # len [128:]

    new_user = Users(
        first_name=users_data.first_name,
        last_name=users_data.last_name,
        email=users_data.email,
        password=hash_password.decode('utf-8'),
        phone_number=users_data.phone_number,
        origin_scoop=21,
        salt=salt.decode('utf-8')
    )

    if new_user:
        try:
            await new_user.save()
            register_handler = registerFlow(users_data.organization_logo)
            await register_handler.create_organization(
                org_name=users_data.organization_name,
                org_type=users_data.organization_type
            )

            # make relation of user and organization
            relation_user_org = User_organization(
                user_id=new_user.id,
                organization_id=register_handler.ORG_INSTANCE.id
            )
            await relation_user_org.save()
        except Exception as e:
            print(e)
            return jsonify({"message": "user already exists with this email"})
    return new_user
