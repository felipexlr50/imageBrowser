import logging
import pathlib
import util
import app_db
from constant import MAIN_FILE_PATH


def init_database():

    app_db.set_db_name(app_db.DEFAULT_NAME)
    app_db.create_tables()
    logging.info("Tables Created or Already Exists")
    verify_folders()


def add_all_folders(entries_list=util.get_all_files_dir()):
    logging.info("Adding all folders!")
    for entry in entries_list:

        if(isinstance(entry, pathlib.WindowsPath)):
            app_db.insertFolder(
                util.stringToB64Safe(entry.name),
                util.stringToB64Safe(str(entry.absolute())))
        else:
            app_db.insertFolder(
                util.stringToB64Safe(entry.name),
                util.stringToB64Safe(entry.path))


def verify_folders():
    dbFolders = app_db.get_folder_count()[0][0]
    sysFolders = util.get_folders_by_date()

    if(dbFolders == 0):
        add_all_folders()

    elif dbFolders < len(sysFolders):
        diff = len(sysFolders) - dbFolders
        to_add = sysFolders[-diff:]
        add_all_folders(to_add)
        logging.info("Folders added!")

    elif dbFolders == len(sysFolders):
        logging.info("No new folder to add!")
        return


def get_latest_folders(n=30):
    latestDb = app_db.get_latest_folders(n)
    resultList = []

    for entry in latestDb:
        resultList.append({
            'id': entry[0],
            'name': util.B64SafeToString(entry[1]),
            'path': util.B64SafeToString(entry[2]),
            'date': entry[3]})

    return resultList
