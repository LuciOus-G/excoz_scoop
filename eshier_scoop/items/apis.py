from fastapi import APIRouter, Request, Depends
from .schemas import NewStocksitem
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
async def post_new_stock(request: Request, items: NewStocksitem):
    new_item = Items(
        name=items.name,
        stock_left=items.stocks,
        single_price=items.single_price,
        organization_id=g.cur_org.id,
        created_by_id=g.cur_user.id,
        total_restock=items.stocks
    )

    if new_item:
        await new_item.save()
        pieces = ItemsPieces(
            items_id=new_item.id,
            restock=items.stocks,
            created_by_id=g.cur_user.id
        )
        await pieces.save()

    return new_item

@items_r.post('/news')
async def get_items_stock(request: Request):
    items = await Items.get(id=4)
    print(items.created_by)
    _in, _out = Organizations().tortoise_to_pydantic()
    print(await _in.from_queryset_single(items.organization))
    return {**items.created_by}
