import time

from fastapi import APIRouter, Request, Depends
from fastapi.encoders import jsonable_encoder as jsonify
from .schemas import NewStocksitem, EditStocksItems
from .models import Items, ItemsPieces
from core import g
from eshier_scoop.auth._helpers import authHandler
from ..organizations.models import Organizations
from ..users.models import Users

items_r = APIRouter(
    prefix='/eshier/item',
    tags=['Items'],
    dependencies=[
        Depends(authHandler().jwt_decode_user)
    ]
)

@items_r.post('/new')
async def post_new_stock(request: Request, item: NewStocksitem):
    all_data = []
    for items in item.data:
        new_item = Items(
            name=items['name'],
            stock_left=items['stock'],
            single_price=items['price'],
            organization_id=g.cur_org.id,
            created_by_id=g.cur_user.id,
            total_restock=items['stock']
        )

        if new_item:
            await new_item.save()
            pieces = ItemsPieces(
                items_id=new_item.id,
                restock=items['stock'],
                created_by_id=g.cur_user.id
            )
            await pieces.save()
        all_data.append(new_item)

    return jsonify({
        "new_item": all_data
    })

@items_r.put('{item_id}')
async def edit_items(request: Request, item_id ,edited: EditStocksItems):
    pass

@items_r.post('/news',)
async def get_items_stock(request: Request):
    items = await Items.get(id=4)
    _in, _out = Organizations().tortoise_to_pydantic()
    return {**items.created_by}

@items_r.get('/{org_id}')
async def get_item(request: Request, org_id):
    item = await Items.filter(organization_id=org_id).all()
    return item

