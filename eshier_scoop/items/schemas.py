from pydantic import BaseModel
from fastapi import File, UploadFile, Form

class NewStocksitem(BaseModel):
    name: str
    stocks: int
    single_price: float


    @classmethod
    def as_form(
            cls,
            name: str = Form(...),
            stocks: str = Form(...),
            single_price: int = Form(...),
    ):
        return cls(name=name, stocks=stocks, single_price=single_price)