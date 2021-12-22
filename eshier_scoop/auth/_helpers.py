import os
import scrypt
from binascii import hexlify, unhexlify
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, HTTPBasic
from passlib.context import CryptContext
from fastapi import Request
import jwt
from fastapi import HTTPException, Security
from eshier_scoop.users.models import Users, User_organization
from datetime import datetime, timedelta

from eshier_scoop.utils.error_handling import Unauthorized


class authHandler(object):
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=['scrypt'], deprecated="auto")
    secret = 'iniadalahkatakunci'

    def salt_generator(self):
        salt = os.urandom(32)
        hex_salt = hexlify(salt)
        return hex_salt

    def hashes_password(self, salt, plain_password):
        encrypt_password = scrypt.hash(
            plain_password,
            unhexlify(salt),
            buflen=64
        )
        return hexlify(encrypt_password)

    async def verify_password(self, password, user):
        valid = False
        if password == user.password[128:]:
            valid = True
        elif self.hashes_password(user.salt, password).decode('utf-8') == user.password:
            valid = True
        return valid

    async def jwt_encode_login(self, user):
        payload = {
            "exp": datetime.utcnow() + timedelta(minutes=15),
            "iat": datetime.utcnow(),
            "user_id": user.id,
            'user_organizations': await self.get_user_organization(user)
        }
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    async def jwt_decode_user(self, request: Request):
        token = request.headers.get('Authorization', None).split(' ')[1]
        try:
            payload = jwt.decode(token, self.secret, algorithms='HS256')
            await self.get_user_for_context(payload['user_id'])
            return payload
        except jwt.ExpiredSignatureError:
            raise Unauthorized(
                developer_message='the token is expired.',
                user_message='your session has been expired'
            )
        except jwt.InvalidTokenError as e:
            raise Unauthorized

    async def get_user_organization(self, user):
        user_org = await User_organization.filter(user_id=user.id).all()
        org_id = []
        for data in user_org:
            org_id.append(data.organization_id)
        return org_id

    async def get_user_for_context(self, user_id):
        from core import g
        user_queries = await Users.get(id=user_id)
        g.cur_user = user_queries


