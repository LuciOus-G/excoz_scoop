import os
import string
import random
import time

import scrypt
from binascii import hexlify, unhexlify
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from fastapi import Request
import jwt

from eshier_scoop.organizations.models import Organizations
from eshier_scoop.users.models import Users, User_organization
from datetime import datetime, timedelta

from eshier_scoop.utils import settings
from eshier_scoop.utils.error_handling import Unauthorized, BadRequest
from eshier_scoop.helpers.google_drive import google


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

    def jwt_encode(self, payload):
        return jwt.encode(
            payload,
            self.secret,
            algorithm='HS256'
        )

    async def jwt_encode_login(self, user):
        org_user_id = await self.get_user_organization(user)
        payload = {
            "exp": datetime.utcnow() + timedelta(minutes=15),
            "iat": datetime.utcnow(),
            "user_id": user.id,
            'eshier_organization': org_user_id.organization_id
        }
        return self.jwt_encode(payload)

    async def jwt_decode_user(self, request: Request):
        try:
            token = request.headers.get('Authorization', None).split(' ')[1]
            payload = jwt.decode(token, self.secret, algorithms='HS256')
            await self.get_user_for_context(
                payload.get('user_id', None),
                payload.get('eshier_organization', None)
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise Unauthorized(
                developer_message='the token is expired.',
                user_message='your session has been expired'
            )
        except jwt.InvalidTokenError as e:
            raise BadRequest(
                developer_message="Token signature invalid",
            )
        # except AttributeError as e:
        #     raise BadRequest(
        #         developer_message=f'{str(e)}, No Authorization been provided',
        #         user_message='No credential been provided'
        #     )

    async def get_user_organization(self, user):
        user_org = User_organization.get(user_id=user.id)
        _in, _out = User_organization().tortoise_to_pydantic()
        ret_org = await _out.from_queryset_single(user_org)
        return ret_org

    async def get_user_for_context(self, user_id, org_id):
        from core import g
        user_queries = await Users.get(id=user_id)
        organization_queries = await Organizations.get(id=org_id)
        g.cur_user = user_queries
        g.cur_org = organization_queries

    async def jwt_refresh(self, encoded):
        # try:
        new_expired_date = datetime.now() + timedelta(minutes=15)
        date_now = datetime.now()
        payload = jwt.decode(encoded, self.secret, algorithms='HS256')
        payload['iat'] = time.mktime(date_now.timetuple())
        payload['exp'] = time.mktime(new_expired_date.timetuple())
        encoded = self.jwt_encode(payload)
        return encoded
        # except jwt.InvalidTokenError as e:
        #     raise BadRequest(
        #         developer_message="Token signature invalid",
        #     )


class registerFlow(google):
    def __init__(self, photo_file):
        self.ORG_INSTANCE = None
        self.PREFIX_LEN = 3
        self.PREFIX = None
        self.FOLDER_ID = None
        self.FILES_PHOTO = photo_file
        self.NEW_FILE = None
        super().__init__()

    async def create_organization(self, org_name, org_type):
        for retry in range(5):
            if retry not in (4, 5):
                try:
                    #make organization ready
                    new_organization = await Organizations(
                        name=org_name,
                        org_type=org_type,
                        prefix=self.generate_prefix()
                    )
                    await new_organization.save()  # must save first to get id
                    self.ORG_INSTANCE = new_organization
                    await self.set_folder_id()
                    await self.upload_photo()
                    break
                except Exception as e:
                    print(e)
                    self.PREFIX_LEN += 1
                    continue
            else:
                print('x')

    async def set_folder_id(self):
        folder_id = await self.create_folder_second(self.ORG_INSTANCE.id)
        self.ORG_INSTANCE.folder_id = folder_id
        self.FOLDER_ID = folder_id
        await self.ORG_INSTANCE.save()

    async def upload_photo(self):
        # upload organization logo if any
        if self.FILES_PHOTO:
            await self.set_organization(self.ORG_INSTANCE)
            temp_image = await self.save_file(self.FILES_PHOTO)
            upload_file = await self.upload_file(temp_image)
            self.NEW_FILE = settings.EMBED_GOOGLE_DRIVE_IMAGE_LINK(upload_file)
            self.ORG_INSTANCE.org_logo = self.NEW_FILE
            await self.ORG_INSTANCE.save()  # save again to input folder id

    def generate_prefix(self):
        prefix = ''.join(random.choice(string.ascii_uppercase) for i in range(self.PREFIX_LEN))
        return prefix
