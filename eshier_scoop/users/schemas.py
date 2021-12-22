from typing import Optional

from fastapi import Form, File
from pydantic import BaseModel

from eshier_scoop.utils import settings


class s_register(BaseModel):
    first_name: str = None
    last_name: str = None
    phone_number: str = None
    email: str
    password: str
    organization_name: str
    organization_type: str
    organization_logo: str = None

    @classmethod
    def as_form(
            cls,
            first_name: str = Form(...),
            last_name: str = Form(...),
            email: str = Form(...),
            password: str = Form(...),
            phone_number: str = Form(...),
            organization_name: str = Form(...),
            organization_type: str = Form(...),
            organization_logo: str = File(default=settings.DEFAULT_PIC)
    ):
        return cls(first_name=first_name, password=password, last_name=last_name,
                   email=email, phone_number=phone_number, organization_name=organization_name,
                   organization_type=organization_type, organization_logo=organization_logo)

class s_login(BaseModel):
    email: str
    password: str
