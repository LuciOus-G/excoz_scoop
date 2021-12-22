from functools import wraps
from string import Template
from urllib.parse import quote_plus

from eshier_scoop.auth._helpers import authHandler
from eshier_scoop.helpers import *
from fastapi import Request

from pydantic import BaseSettings


class config(BaseSettings):
    DATABASE_URI = Template(
        "postgres://$user:$password@$host:$port/$db_name").substitute(
        user=_str("DB_USER", "postgres"),
        password=quote_plus(_str("DB_PASS", "admin")),
        host=_str("DB_HOST", "localhost"),
        port=_str("DB_PORT", "5432"),
        db_name=_str("DB_NAME", "workascoop_db")
    )
    DEFAULT_PIC = 'https://firebasestorage.googleapis.com/v0/b/worka-eshier.appspot.com/o/default_profil_pic.jpg?alt=media&token=80eca9c8-4a81-4fd1-a6c2-8d23ea87670e'
    PARENT_FOLDER = '1PeXecAsXj5glqn3BOfDeMaxdRrLrS-xy'

settings = config()

# def check_token_before_request(func):
#     @wraps(func)
#     async def inner(request: Request, *args, **kwargs):
#         jwt_decode = authHandler().jwt_decode_user(
#             request.headers.get('Authorization', None)
#         )
#         print(jwt_decode)
#         print('masuk ke decorator')
#         print(request.headers.get('Authorization', None))
#         returns = await func(request)
#         print('sesudah')
#         return returns
#
#     return inner
#
# def user_is_authenticated(func):
#     """ Raises 401 if the user is not authenticated.
#
#     Decorates a method view function.
#
#     :param `callable` func: The function that's being wrapped.
#     :return: The wrapped function.
#     """
#     @wraps(func)
#     async def inner(request: Request, *args, **kwargs):
#         print('masuk ke decorator')
#         print(request.headers.get('Authorization', None))
#         returns = await func(request)
#         print('sesudah')
#         return returns
#
#     return inner