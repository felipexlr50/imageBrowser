import os
import random
import base64
import eel

from pathlib import Path

path = "S:\\NH"

LIMIT = 20


def get_all_files_dir():
    entries_list = []
    with os.scandir(path) as entries:

        for entry in entries:
            if entry.is_dir():
                entries_list.append(entry)
    return entries_list


def get_random_entries(n):

    folder_images = []

    entries = list(get_all_files_dir())
    sorted_list = random.sample(entries, n)

    i = 0
    for entry in sorted_list:

        if i > LIMIT:
            break

        if entry.is_dir():
            print(entry.name)
            entryFolder = os.path.join(path, entry)
            folder_images.append(get_folder_img(entryFolder))

        i += 1

    return folder_images


def get_folder_img(folder_path):
    with os.scandir(folder_path) as entries:
        img_file = entries.__next__()
        return os.path.join(folder_path, img_file)


def open_file(file_path):
    encoded_byte = None
    with open(file_path, "rb") as f:
        encoded_byte = f.read()
    f.close()

    return base64.b64encode(encoded_byte)


print(get_random_entries(10))
