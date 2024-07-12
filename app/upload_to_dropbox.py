import dropbox
import os
from dotenv import load_dotenv

load_dotenv()

DROPBOX_ACCESS_TOKEN = os.getenv('DROPBOX_ACCESS_TOKEN')

def authenticate_dropbox():
    return dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

def upload_to_dropbox(file_path, dropbox_path):
    dbx = authenticate_dropbox()
    with open(file_path, 'rb') as f:
        dbx.files_upload(f.read(), dropbox_path)
    print(f"Uploaded {file_path} to Dropbox as {dropbox_path}")
    return dropbox_path

def delete_from_dropbox(file_path):
    dbx = authenticate_dropbox()
    dbx.files_delete_v2(file_path)
    print(f"Deleted file {file_path} from Dropbox")
