import os
import io
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate_google_drive():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('drive', 'v3', credentials=creds)
    return service

def get_latest_video():
    service = authenticate_google_drive()
    
    folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
    query = f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.folder'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    clips_folder = next((item for item in results.get('files', []) if item['name'] == 'Clips'), None)

    if not clips_folder:
        print('Clips folder not found.')
        return None

    query = f"'{clips_folder['id']}' in parents and mimeType='application/vnd.google-apps.folder'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    game_folders = results.get('files', [])

    video_files = []
    for game_folder in game_folders:
        game_folder_id = game_folder['id']
        game_query = f"'{game_folder_id}' in parents and mimeType='video/mp4'"
        game_results = service.files().list(q=game_query, fields="files(id, name, createdTime)").execute()
        video_files.extend(game_results.get('files', []))

    if not video_files:
        print('No video files found.')
        return None

    latest_file = max(video_files, key=lambda x: x['createdTime'])
    print(f"Latest file found: {latest_file['name']} (Created: {latest_file['createdTime']})")
    return latest_file

def get_file_content_from_google_drive(file_id):
    service = authenticate_google_drive()
    request = service.files().get_media(fileId=file_id)
    file_content = io.BytesIO()
    downloader = MediaIoBaseDownload(file_content, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")
    file_content.seek(0)
    print(f"Downloaded file with ID {file_id}")
    return file_content

def delete_file_from_google_drive(file_id):
    service = authenticate_google_drive()
    try:
        print(f"Attempting to delete file with ID {file_id}")
        service.files().delete(fileId=file_id).execute()
        print(f"Deleted file with ID {file_id}")
    except Exception as e:
        print(f"Error deleting file from Google Drive: {e}")
