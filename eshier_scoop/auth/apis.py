from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.encoders import jsonable_encoder as jsonify
from binascii import hexlify
from tortoise.exceptions import DoesNotExist

from eshier_scoop.users.schemas import s_register, s_login
from eshier_scoop.users.models import Users, User_organization
from ._helpers import authHandler, registerFlow
from ..utils.error_handling import BadRequest

auth_r = APIRouter(prefix='/eshier/auth', tags=['Authentications'])


@auth_r.post('/login')
async def login(request: Request, cred: s_login):
    try:
        _in, _out = Users().tortoise_to_pydantic()
        user = Users.get(email=cred.email)
        user_parse = await _in.from_queryset_single(user)
        handeler = authHandler()
        is_valid = await handeler.verify_password(cred.password, user_parse)
    except DoesNotExist as e:
        raise BadRequest(
            developer_message=str(e),
        )

    if not user_parse.is_active:
        raise HTTPException(status_code=404, detail='user not found')

    if not is_valid:
        raise HTTPException(status_code=401, detail='username or pw wrong')
    else:
        base_response = await _out.from_queryset_single(user)
        response = base_response.dict()
        response['id'] = user_parse.id
        response['access_token'] = await handeler.jwt_encode_login(user_parse)
        response['refresh_token'] = await handeler.jwt_encode_login_refresh(user_parse)
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
            try:
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
                new_user.has_organization = False
                new_user.error_message = e
                await new_user.save()
                raise BadRequest(
                    developer_message=f'{e} ,see the database for error'
                )
        except Exception as e:
            raise BadRequest(
                developer_message=e,
                user_message='User with this email already exists'
            )
    return new_user

@auth_r.post('/refresh-token')
async def refresh_token(request: Request):
    previous_token = await request.json()
    refresh = await authHandler().jwt_refresh(previous_token.get('token', None))

    return refresh