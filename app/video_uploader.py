import os
import discord
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv

load_dotenv()

CHANNEL_ID = os.getenv('CHANNEL_ID')
MEDAL_CLIPS_DIR = os.getenv('MEDAL_CLIPS_DIR')

# Set up logging
logging.basicConfig(level=logging.INFO)

class ClipHandler(FileSystemEventHandler):
    def __init__(self, client):
        self.client = client

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.mp4'):
            logging.info(f"Detected new clip: {event.src_path}")
            latest_clip = self.get_latest_clip()
            if latest_clip:
                self.upload_clip(latest_clip)

    def get_latest_clip(self):
        latest_time = 0
        latest_file = None
        for root, _, files in os.walk(MEDAL_CLIPS_DIR):
            for file in files:
                if file.endswith('.mp4'):
                    file_path = os.path.join(root, file)
                    file_time = os.path.getmtime(file_path)
                    if file_time > latest_time:
                        latest_time = file_time
                        latest_file = file_path
        return latest_file

    def upload_clip(self, clip_path):
        logging.info(f"Uploading clip: {clip_path}")
        channel = self.client.get_channel(int(CHANNEL_ID))
        if channel is not None:
            with open(clip_path, 'rb') as file:
                logging.info(f"Sending clip to Discord channel {CHANNEL_ID}")
                self.client.loop.create_task(channel.send(file=discord.File(file)))
        else:
            logging.error(f"Failed to get channel: {CHANNEL_ID}")

def run_uploader(client):
    event_handler = ClipHandler(client)
    observer = Observer()
    observer.schedule(event_handler, MEDAL_CLIPS_DIR, recursive=True)
    observer.start()
    logging.info(f"Started monitoring {MEDAL_CLIPS_DIR}")
