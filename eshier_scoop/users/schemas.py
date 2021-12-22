from fastapi import Form
from pydantic import BaseModel


class s_users(BaseModel):
    first_name: str = None
    last_name: str = None
    phone_number: str = None
    email: str
    password: str

    @classmethod
    def as_form(
            cls,
            first_name: str = Form(...),
            last_name: str = Form(...),
            email: str = Form(...),
            password: str = Form(...),
            phone_number: str = Form(...),
    ):
        return cls(first_name=first_name, password=password, last_name=last_name,
                   email=email, phone_number=phone_number)

    @classmethod
    def as_login(
            cls,
            email: str = Form(...),
            password: str = Form(...),
    ):
        return cls(password=password, email=email)
