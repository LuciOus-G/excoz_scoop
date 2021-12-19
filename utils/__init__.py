from string import Template
from urllib.parse import quote_plus
from helpers import *

from pydantic import BaseSettings


class config(BaseSettings):
    DATABASE_URI = Template(
        "postgresql://$user:$password@$host:$port/$db_name").substitute(
        user=_str("DB_USER", "postgres"),
        password=quote_plus(_str("DB_PASS", "admin")),
        host=_str("DB_HOST", "localhost"),
        port=_str("DB_PORT", "5432"),
        db_name=_str("DB_NAME", "workascoop_db")
    )
    DEFAULT_PIC = 'https://firebasestorage.googleapis.com/v0/b/worka-eshier.appspot.com/o/default_profil_pic.jpg?alt=media&token=80eca9c8-4a81-4fd1-a6c2-8d23ea87670e'

settings = config()
