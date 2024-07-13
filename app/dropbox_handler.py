import dropbox
from dropbox.oauth import DropboxOAuth2FlowNoRedirect
from dotenv import load_dotenv
from io import BytesIO
import os
import requests
import json

load_dotenv()

DROPBOX_APP_KEY = os.getenv('DROPBOX_APP_KEY')
DROPBOX_APP_SECRET = os.getenv('DROPBOX_APP_SECRET')
DROPBOX_REFRESH_TOKEN = os.getenv('DROPBOX_REFRESH_TOKEN')
DROPBOX_FOLDER_PATH = os.getenv('DROPBOX_FOLDER_PATH')

def refresh_access_token():
    url = "https://api.dropbox.com/oauth2/token"
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': DROPBOX_REFRESH_TOKEN,
        'client_id': DROPBOX_APP_KEY,
        'client_secret': DROPBOX_APP_SECRET
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens['access_token']
        print(f"Refreshed access token: {access_token[:4]}...")  # Print the first few characters of the token
        return access_token
    else:
        raise Exception("Failed to refresh access token: " + response.text)

def authenticate_dropbox():
    access_token = refresh_access_token()
    return dropbox.Dropbox(access_token)

def get_latest_video(dropbox_folder_path):
    dbx = authenticate_dropbox()
    print(f"Checking Dropbox folder: {dropbox_folder_path}")
    try:
        response = dbx.files_list_folder(dropbox_folder_path, recursive=True)
    except dropbox.exceptions.ApiError as err:
        print(f"API error: {err}")
        return None

    files = [entry for entry in response.entries if isinstance(entry, dropbox.files.FileMetadata) and entry.name.endswith('.mp4')]
    if not files:
        print("No video files found.")
        return None

    latest_file = max(files, key=lambda f: f.client_modified)
    print(f"Latest file found: {latest_file.name}")
    return latest_file

def get_file_content_from_dropbox(file_metadata):
    dbx = authenticate_dropbox()
    _, res = dbx.files_download(file_metadata.path_lower)
    file_content = BytesIO(res.content)
    print(f"Read content of {file_metadata.name} from Dropbox")
    return file_content

def delete_from_dropbox(file_metadata):
    dbx = authenticate_dropbox()
    dbx.files_delete_v2(file_metadata.path_lower)
    print(f"Deleted file {file_metadata.name} from Dropbox")
