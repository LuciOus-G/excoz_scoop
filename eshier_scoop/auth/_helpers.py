import os
import string
import random

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
from eshier_scoop.utils.error_handling import Unauthorized
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
