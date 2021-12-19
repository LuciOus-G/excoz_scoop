from fastapi import Form
from pydantic import BaseModel


class s_users(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone_number: str
    profil_pic: str = None

    @classmethod
    def as_form(
            cls,
            first_name: str = Form(...),
            last_name: str = Form(...),
            email: str = Form(...),
            password: str = Form(...),
            phone_number: str = Form(...),
            profil_pic: str = Form(default=None),
    ):
        return cls(first_name=first_name, password=password, last_name=last_name,
                   email=email, phone_number=phone_number, profil_pic=profil_pic)
