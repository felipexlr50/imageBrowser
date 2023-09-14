import logging
import pathlib
import util
import app_db
import queryBuilder
import threading


def init_database():

    app_db.create_tables()
    logging.debug("Tables Created or Already Exists")
    # verify_folders()
    thread = threading.Thread(target=verify_folders)
    thread.start()


def add_all_folders(entries_list=util.get_all_files_dir()):
    logging.debug("Adding all folders!")
    for entry in entries_list:

        if (isinstance(entry, pathlib.WindowsPath)):
            app_db.insertFolder(
                util.stringToB64Safe(entry.name),
                util.stringToB64Safe(str(entry.absolute())))


def verify_folders():
    dbFolders = app_db.get_folder_count()[0][0]
    sysFolders = util.get_folders_by_date()

    if dbFolders < len(sysFolders):
        diff = len(sysFolders) - dbFolders
        to_add = sysFolders[-diff:]
        add_all_folders(to_add)
        logging.debug("Folders added!")

    elif dbFolders == len(sysFolders):
        logging.debug("No new folder to add!")
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


def get_folder_by_id(id):
    result = app_db.get_folder_by_id(id)
    result_obj = {
        'id': result[0],
        'name': util.B64SafeToString(result[1]),
        'path': util.B64SafeToString(result[2]),
        'date': result[3]}
    return result_obj


def set_tag(tag, folder):
    app_db.insertTag(util.stringToB64Safe(tag))
    app_db.insertTagFolder(util.stringToB64Safe(tag),
                           util.stringToB64Safe(folder))


def get_tags(folder):
    dbResults = app_db.get_folder_tags(util.stringToB64Safe(folder))

    resultList = []

    for entry in dbResults:
        resultList.append(util.B64SafeToString(entry[0]))

    return resultList


def filter_results(query):
    dbResults = app_db.get_folders_by_tags(
        queryBuilder.filterResultsDb(query))

    resultList = []

    for entry in dbResults:
        resultList.append(util.B64SafeToString(entry[0]))

    return resultList
