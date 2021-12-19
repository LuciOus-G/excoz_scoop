"""
SCOOP PLATFORM ID = W_ESHIER 21
"""
import sqlalchemy
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi import FastAPI
from fastapi_sqlalchemy.middleware import DBSessionMeta, DBSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from starlette.responses import JSONResponse
import os
from utils import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(
    debug=True
)


app.add_middleware(DBSessionMiddleware, db_url=settings.DATABASE_URI)
init_db_session: DBSessionMeta = DBSession
with init_db_session():
    db = init_db_session.session

engine = sqlalchemy.create_engine(settings.DATABASE_URI)
sessions = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = scoped_session(sessions)
Base = declarative_base()
Base.query = session.query_property()

from organizations._helpers import aps
from auth.apis import auth_r
app.include_router(aps)
app.include_router(auth_r)