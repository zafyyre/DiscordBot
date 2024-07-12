import os
import discord
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv
from upload_to_dropbox import upload_to_dropbox, delete_from_dropbox

load_dotenv()

CHANNEL_ID = os.getenv('CHANNEL_ID')
MEDAL_CLIPS_DIR = os.getenv('MEDAL_CLIPS_DIR')
DROPBOX_FOLDER_PATH = os.getenv('DROPBOX_FOLDER_PATH')

class ClipHandler(FileSystemEventHandler):
    def __init__(self, client):
        self.client = client

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.mp4'):
            self.upload_and_delete_clip(event.src_path)

    def upload_and_delete_clip(self, clip_path):
        dropbox_path = DROPBOX_FOLDER_PATH + os.path.basename(clip_path)
        # Upload to Dropbox
        uploaded_path = upload_to_dropbox(clip_path, dropbox_path)
        # Upload to Discord
        self.upload_to_discord(clip_path)
        # Delete local file
        os.remove(clip_path)
        # Delete from Dropbox
        delete_from_dropbox(uploaded_path)

    def upload_to_discord(self, clip_path):
        channel = self.client.get_channel(int(CHANNEL_ID))
        if channel is not None:
            with open(clip_path, 'rb') as file:
                self.client.loop.create_task(channel.send(file=discord.File(file)))

def run_uploader(client):
    event_handler = ClipHandler(client)
    observer = Observer()
    observer.schedule(event_handler, MEDAL_CLIPS_DIR, recursive=True)
    observer.start()
