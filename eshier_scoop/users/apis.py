from fastapi import APIRouter, Request, Depends
from fastapi.encoders import jsonable_encoder as jsonify
from .models import Users
from eshier_scoop.auth._helpers import authHandler
from core import g
from eshier_scoop.helpers.google_drive import google
from ..organizations.models import Organizations

user_r = APIRouter(
    prefix='/eshier/user',
    tags=['Users'],
    # dependencies=[Depends(authHandler().jwt_decode_user)]
)

@user_r.get('/details')
async def get_user(request: Request):
    print(g.cur_user.id)
    data_user = Users.all()
    _in, _out = Users().tortoise_to_pydantic()
    response = await _in.from_queryset(data_user)
    return jsonify(response)


@user_r.get('/test')
async def test():
    import time
    time.sleep(5)
    return 'OK'