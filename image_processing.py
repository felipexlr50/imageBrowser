import base64
import util
import os
import random
import db_util

from constant import LIMIT
from constant import MAIN_FILE_PATH
from PIL import Image
from io import BytesIO


def process_image(image_src, compressionPerCent=150):
    buffered = BytesIO()
    basewidth = compressionPerCent
    img = Image.open(image_src)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save(buffered, format="PNG")

    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def get_all_image(folder_name, compressionPerCent=150):
    folder_images = []

    entries = list(get_all_files(folder_name))
    for entry in entries:
        print(entry.name)
        imageSource = os.path.join(entry)
        folder_images.append(get_folder_img(imageSource, compressionPerCent))

    return folder_images


def get_folder_img(path, compressionPerCent=150):

    if(os.path.isfile(path)):
        img_64 = process_image(path, compressionPerCent)
        return img_64

    else:
        with os.scandir(path) as entries:
            img_file = entries.__next__()
            img_64 = process_image(os.path.join(path, img_file))
            return img_64


def get_image(image_name, folder):
    path = os.path.join(MAIN_FILE_PATH, folder, image_name)
    return process_image(path, 500)


def get_all_files(dir_name):
    entries_list = []
    with os.scandir(os.path.join(MAIN_FILE_PATH, dir_name)) as entries:

        for entry in entries:
            if not entry.is_dir():
                entries_list.append(entry)
    return entries_list


def get_latest(n=30):
    folder_images = []
    entries = list(db_util.get_latest_folders(n))

    for entry in entries:

        print(entry['name'])
        folder_images.append({
            "name": entry["name"],
            "path": entry["path"],
            "id": entry["id"],
            "date": entry["date"],
            "img": get_folder_img(entry['path'])})

    return folder_images


def get_random_entries(n):

    folder_images = []

    entries = list(util.get_all_files_dir())
    sorted_list = random.sample(entries, n)

    i = 0
    for entry in sorted_list:

        if i > LIMIT:
            break

        if entry.is_dir():
            print(entry.name)
            entryFolder = os.path.join(MAIN_FILE_PATH, entry)
            folder_images.append(get_folder_img(entryFolder))

        i += 1

    return folder_images
