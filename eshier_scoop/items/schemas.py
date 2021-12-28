from pydantic import BaseModel
from fastapi import File, UploadFile, Form

class NewStocksitem(BaseModel):
    data: list


    @classmethod
    def as_form(
            cls,
            name: str = Form(...),
    ):
        return cls(name=name)