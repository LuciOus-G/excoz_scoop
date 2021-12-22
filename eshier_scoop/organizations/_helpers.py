import os

from fastapi_cloud_drives import GoogleDrive
from fastapi_cloud_drives import GoogleDriveConfig
from starlette.responses import JSONResponse
from fastapi import APIRouter

from core import BASE_DIR

aps = APIRouter(prefix='/v1')

google_conf = {
    "CLIENT_ID_JSON" : os.path.join(BASE_DIR, 'core/client_id.json'),
    "SCOPES": [
        "https://www.googleapis.com/auth/drive"
        ]
}

config = GoogleDriveConfig(**google_conf)
gdrive = GoogleDrive(config)

async def list_files():
    f = await gdrive.list_files()
    return JSONResponse(status_code=200, content=f)

async def upload_file(fname, fpath):
    resp = await gdrive.upload_file(
        filename=fname,
        filepath=fpath,
    )
    return JSONResponse(status_code=200, content=resp)

async def create_folder(folder_name: str):
    resp = await gdrive.create_folder(folder_name=folder_name)
    return JSONResponse(status_code=200, content=resp)