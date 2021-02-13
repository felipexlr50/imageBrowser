import os
import random
import base64
import eel
import logging
import app_db
import util

from PIL import Image
from io import BytesIO
from pathlib import Path

MAIN_FILE_PATH = "S:\\NH"

SCRIP_FILE_PATH = os.getcwd()

LIMIT = 20

ENTRIES_FILE = "temp_entries"


eel.init('content')


def get_all_files_dir():
    entries_list = []
    with os.scandir(MAIN_FILE_PATH) as entries:

        for entry in entries:
            if entry.is_dir():
                entries_list.append(entry)
    return entries_list

def get_all_files(dir_name):
    entries_list = []
    with os.scandir(os.path.join(MAIN_FILE_PATH, dir_name)) as entries:

        for entry in entries:
            if not entry.is_dir():
                entries_list.append(entry)
    return entries_list


def stringToB64(text):
    return base64.b64encode(bytes(text, 'utf-8')).decode("utf-8")


def add_all_folders(main_file_path, scriptpath):
    entries_list = get_all_files_dir()
    logging.debug("Adding all folders!")
    for entry in entries_list:
        app_db.insertFolder(stringToB64(entry.name), stringToB64(entry.path))


def init_database():

    app_db.create_tables()
    logging.info("Tables Created or Already Exists")
    #add_all_folders(MAIN_FILE_PATH, SCRIP_FILE_PATH)
    logging.info("Folders added!")


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
            entryFolder = os.path.join(MAIN_FILE_PATH, entry)
            folder_images.append(get_folder_img(entryFolder))

        i += 1

    return folder_images

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
        img_file = path
        img_64 = process_image(img_file, compressionPerCent)
        img_name = img_file.split('\\')[-1]
        return [img_64, img_name]

    else:
        with os.scandir(path) as entries:
            img_file = entries.__next__()
            img_64 = process_image(os.path.join(path, img_file))
            img_name = path.replace("S:\\NH\\", "")
            return [img_64, img_name]


def get_image(image_name, folder):
    path = os.path.join(MAIN_FILE_PATH, folder, image_name)
    return process_image(path, 500)


def process_image(image_src, compressionPerCent=150):
    buffered = BytesIO()
    basewidth = compressionPerCent
    img = Image.open(image_src)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save(buffered, format="PNG")

    return base64.b64encode(buffered.getvalue()).decode("utf-8")


@eel.expose
def get_images():
    return get_random_entries(18)

@eel.expose
def get_folder_images(image_name):
    return get_all_image(image_name, 500)

@eel.expose
def get_image_by_name(image_name, folder):
    return get_image(image_name, folder)       


init_database()


eel.start('index.html')
