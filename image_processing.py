import util
import os
import random
import db_util
from constant import MAIN_FILE_PATH, LIMIT
from PIL import Image
from io import BytesIO


def get_latest_from_file(entries):
    folder_images = []

    for entry in entries:

        imgpath = get_relative_path(get_image_from_path(entry["path"]))
        imgpath64 = util.stringToB64Safe(imgpath)

        print(entry['name'])
        folder_images.append({
            "name": str(entry["name"]),
            "path": imgpath64,
            "id": str(entry["id"]),
            "date": str(entry["date"])
        })

    return folder_images


def get_book(book_obj):
    book = {}
    imgpath = get_relative_path(get_image_from_path(book_obj["path"]))
    imgpath64 = util.stringToB64Safe(imgpath)

    print(book_obj['name'])
    book = {
        "name": str(book_obj["name"]),
        "path": imgpath64,
        "id": str(book_obj["id"]),
        "date": str(book_obj["date"])
    }
    return book


def get_image_from_path(path):
    if (os.path.isfile(path)):

        return path

    else:
        filelist = sorted(os.listdir(
            path), key=lambda f: int(os.path.splitext(f)[0]))
        filepath = os.path.join(path, filelist[0])
        return filepath


def get_image_list_from_path(path):
    filelist = []
    dirpath = os.path.join(MAIN_FILE_PATH, path)
    for file in os.listdir(dirpath):
        filepath = os.path.join(path, file)
        filelist.append(filepath)

    filelist.sort()
    return list(map(util.stringToB64Safe, filelist))


def get_relative_path(absolute_path):
    container_folder, filename = absolute_path.split('\\')[2:]
    # Extract the container folder

    return os.path.join(container_folder, filename)


def process_image(image_src, compressionPerCent=150):
    buffered = BytesIO()
    basewidth = compressionPerCent
    img = Image.open(image_src)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    img.save(buffered, format="JPEG")

    return util.stringToB64Safe(buffered.getvalue())


def get_all_image(folder_name):
    folder_images = []

    entries = list(get_all_files(folder_name))
    for entry in entries:
        print(entry.name)
        imageSource = os.path.join(entry)
        folder_images.append(imageSource)

    return folder_images


def get_folder_img(path, compressionPerCent=150):

    imgfile = get_image_from_path(path)
    return process_image(imgfile, compressionPerCent)


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


def get_filtered_results(query, n=30):
    folder_images = []
    entries = list(db_util.filter_results(query))

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
