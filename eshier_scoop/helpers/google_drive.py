import inspect
import mimetypes
import random
import shutil
import string
from pathlib import Path
from tempfile import NamedTemporaryFile
import os
from core import BASE_DIR

from fastapi import UploadFile
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

from eshier_scoop.organizations.models import Organizations

class google(object):
    def __init__(self):
        self.GAUTH = None
        self.ORG = None
        self.FOLDER = None
        self.initiate()

    def initiate(self):
        gauth = GoogleAuth()
        # Try to load saved client credentials
        gauth.LoadCredentialsFile("storage.json")
        if gauth.credentials is None:
            # Authenticate if they're not there
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            # Refresh them if expired
            gauth.Refresh()
        else:
            # Initialize the saved creds
            gauth.Authorize()
        # Save the current credentials to a file
        gauth.SaveCredentialsFile("storage.json")

        drive = GoogleDrive(gauth)

        self.GAUTH = drive
        return 'OK'

    def get_files_list(self):
        file_list = self.GAUTH.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for file1 in file_list:
            print('title: %s, id: %s' % (file1['title'], file1['id']))

    async def upload_file(self, path):
        file = self.GAUTH.CreateFile({
            'title': self.generate_file_name(),
            'parents': [{'id': self.ORG.folder_id}]
        })
        file.SetContentFile(path)
        file.Upload()
        permission = file.InsertPermission({
            'type': 'anyone',
            'value': 'anyone',
            'role': 'reader'})
        return file

    def create_folder(self, org_id):
        from eshier_scoop.utils import settings
        newFolder = self.GAUTH.CreateFile({
            'title': f'_{str(org_id)}',
            "parents": [{
                "kind": "drive#fileLink",
                "id": settings.PARENT_FOLDER
            }],
            "mimeType": "application/vnd.google-apps.folder"
        })
        newFolder.Upload()
        return newFolder

    async def create_folder_second(self, org_id):
        from core import BASE_DIR
        import os
        from fastapi_cloud_drives import GoogleDrive
        from fastapi_cloud_drives import GoogleDriveConfig

        google_conf = {
            "CLIENT_ID_JSON": os.path.join(BASE_DIR, 'client_secrets.json'),
            "SCOPES": [
                "https://www.googleapis.com/auth/drive"
            ],
        }

        config = GoogleDriveConfig(**google_conf)
        gdrive = GoogleDrive(config)

        resp = await gdrive.create_folder(folder_name=f"_{str(org_id)}")
        return resp

    async def set_organization(self, organization):
        """
        :param organization: accept organization instance or organization id
        :return: no return anything, set ORG object to organization instance

        check if :param organization: is alredy organization instance else get by id
        """
        if isinstance(organization, Organizations):
            self.ORG = organization
        else:
            organization = await Organizations.get(id=organization)
            self.ORG = organization

    async def save_file(self, upload_file: UploadFile):
        self.FOLDER = os.path.join(BASE_DIR, f'temp_image/test/{upload_file.filename}')
        with open(self.FOLDER, 'wb') as out_file:
            uploaded_file = upload_file.file.read()
            out_file.write(uploaded_file)
        return self.FOLDER

    def generate_file_name(self):
        prefix = ''.join(random.choice(string.ascii_uppercase) for i in range(5))
        name = f'21_{self.ORG.prefix}_{str(self.ORG.id)}_{prefix}'
        return name