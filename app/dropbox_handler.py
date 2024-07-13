import dropbox
from dotenv import load_dotenv
from io import BytesIO
import os

load_dotenv()

DROPBOX_ACCESS_TOKEN = os.getenv('DROPBOX_ACCESS_TOKEN')
DROPBOX_FOLDER_PATH = os.getenv('DROPBOX_FOLDER_PATH')

def authenticate_dropbox():
    return dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

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
