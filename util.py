import os
import base64
from constant import MAIN_FILE_PATH
import os
from pathlib import Path


def read_file(src):
    content = None
    with open(src, 'r') as f:
        content = f.read()
    f.closed
    return content


def stringToB64(text):
    return base64.b64encode(bytes(text, 'utf-8')).decode("utf-8")


def stringToB64Safe(text):
    return base64.urlsafe_b64encode(bytes(text, 'utf-8')).decode()


def B64SafeToString(text):
    return base64.urlsafe_b64decode(text).decode('utf-8')


def get_all_files_dir():
    entries_list = []
    with os.scandir(MAIN_FILE_PATH) as entries:

        for entry in entries:
            if entry.is_dir():
                entries_list.append(entry)
    return entries_list


def get_folders_by_date():
    paths = sorted(
        Path(os.path.join(MAIN_FILE_PATH))
        .iterdir(), key=os.path.getmtime)

    return paths
