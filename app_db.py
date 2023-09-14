import sqlite3
import queryBuilder
import logging
import sys
import zlib
import logging
import util


DEFAULT_NAME = 'app.db'

CREATE_TABLE_TAG = '''
CREATE TABLE IF NOT EXISTS Tag(tagName text unique not null primary key)
'''

CREATE_TABLE_FOLDER = '''
CREATE TABLE IF NOT EXISTS Folder(
    id text unique not null primary key,
    folderName text not null,
    path text unique not null,
    added_date timestamp DEFAULT CURRENT_TIMESTAMP)
'''

CREATE_TABLE_TAG_FOLDER = '''
CREATE TABLE IF NOT EXISTS tag_folder(
    tagName text not null,
    folderName text not null,
    foreign key(tagName) references Tag(tagName)
    foreign key(folderName) references Folder(folderName)
    unique (tagName, folderName))
'''

SELECT_FOLDERS_BY_TAG = '''
SELECT folderName
FROM tag_folder
WHERE folderName NOT IN
 (SELECT folderName FROM tag_folder WHERE tagName IN ({}))
INTERSECT
SELECT folderName
FROM tag_folder
WHERE tagName IN ({})
GROUP BY folderName
HAVING COUNT(*) = {}
'''

SELECT_FOLDERS_TAGS = "SELECT * FROM tag_folder ORDER BY folderName"

SELECT_FOLDER_TAGS = """SELECT tagName FROM tag_folder
WHERE folderName = '{}'
"""

SELECT_LATEST_FOLDERS = '''
SELECT * FROM Folder
ORDER BY added_date DESC
LIMIT 0,{}
'''

SELECT_FOLDER_BY_ID = """
SELECT * FROM Folder
WHERE id = {}
"""

SELECT_COUNT_FOLDERS = "SELECT COUNT(*) FROM Folder"


def create_connection(app_db=DEFAULT_NAME):
    connection = None
    try:
        connection = sqlite3.connect(app_db)
    except:
        logging.error(sys.exc_info()[0])

    finally:
        return connection


def create_tables(app_db=DEFAULT_NAME):
    connection = create_connection(app_db)
    c = connection.cursor()
    c.execute(CREATE_TABLE_TAG)
    c.execute(CREATE_TABLE_FOLDER)
    c.execute(CREATE_TABLE_TAG_FOLDER)

    connection.commit()
    connection.close()


def get_folders_by_tags(*tags, app_db=DEFAULT_NAME):
    connection = create_connection(app_db)
    c = connection.cursor()

    tagArray = list(
        map(lambda x: str("'"+str(util.stringToB64Safe(x))+"'"), tags[0][0]))
    negTagArray = list(
        map(lambda x: str("'"+str(util.stringToB64Safe(x))+"'"), tags[0][1]))

    tagString = ", ".join(tagArray) if len(tagArray) > 0 else ""
    negTagString = ", ".join(negTagArray) if len(negTagArray) > 0 else ""

    sqlQuerry = str(SELECT_FOLDERS_BY_TAG).format(
        negTagString, tagString, len(tagArray))

    result = c.execute(sqlQuerry).fetchall()
    connection.close()

    return result


def get_latest_folders(n=30, app_db=DEFAULT_NAME):
    connection = create_connection(app_db)
    c = connection.cursor()

    sqlQuerry = str(SELECT_LATEST_FOLDERS).format(n)

    result = c.execute(sqlQuerry).fetchall()
    connection.close()

    return result


def get_folder_by_id(id, app_db=DEFAULT_NAME):
    result = {}
    with sqlite3.connect(app_db) as connection:

        cur = connection.cursor()
        sqlQuerry = str(SELECT_FOLDER_BY_ID).format(id)
        result = cur.execute(sqlQuerry).fetchone()

    return result


def get_folders_tags(app_db=DEFAULT_NAME):
    connection = create_connection(app_db)
    c = connection.cursor()

    result = c.execute(SELECT_FOLDERS_TAGS).fetchall()
    connection.close()

    return result


def get_folder_tags(folderName, app_db=DEFAULT_NAME):
    logging.debug(f"Getting tags for {folderName}")
    connection = create_connection(app_db)
    c = connection.cursor()

    result = c.execute(SELECT_FOLDER_TAGS.format(folderName)).fetchall()
    connection.close()

    return result


def get_folder_count(app_db=DEFAULT_NAME):
    connection = create_connection(app_db)
    c = connection.cursor()

    result = c.execute(SELECT_COUNT_FOLDERS).fetchall()
    connection.close()

    return result


def insertTag(tag, app_db=DEFAULT_NAME):
    try:
        connection = create_connection(app_db)
        c = connection.cursor()
        c.execute("INSERT INTO Tag(tagName) VALUES('{}')".format(tag))
        connection.commit()
        connection.close()
    except:
        logging.error(f"Failed to insert to data base: {sys.exc_info()[0]}")


def insertFolder(folder, path, app_db=DEFAULT_NAME):
    try:
        id = zlib.adler32(folder.encode())
        connection = create_connection(app_db)
        c = connection.cursor()
        c.execute(
            "INSERT INTO Folder(id, folderName, path) VALUES('{}', '{}', '{}')".format(id, folder, path))
        connection.commit()
        connection.close()

    except sqlite3.OperationalError as e:
        logging.error(e)

    except sqlite3.IntegrityError as e:
        logging.error(e)

    except:
        logging.error(f"Failed to insert to data base: {sys.exc_info()[0]}")


def insertTagFolder(tag, folder, app_db=DEFAULT_NAME):
    try:
        connection = create_connection(app_db)
        c = connection.cursor()

        c.execute("INSERT INTO tag_folder(tagName, folderName) VALUES('{}', '{}')".format(
            tag, folder))

        connection.commit()
        connection.close()
    except:
        logging.error(f"Failed to insert to data base: {sys.exc_info()[0]}")


def test_insert_some_values():
    app_db = "test.db"
    create_tables(app_db=app_db)
    insertTag('tag1', app_db=app_db)
    insertTag('tag2', app_db=app_db)
    insertTag('tag3', app_db=app_db)
    insertTag('tag4', app_db=app_db)

    insertFolder('folder1', '/path1', app_db=app_db)
    insertFolder('folder2', '/path2', app_db=app_db)
    insertFolder('folder3', '/path3', app_db=app_db)
    insertFolder('folder4', '/path4', app_db=app_db)
    insertFolder('folder5', '/path5', app_db=app_db)

    insertTagFolder('tag1', 'folder1', app_db=app_db)
    insertTagFolder('tag2', 'folder1', app_db=app_db)
    insertTagFolder('tag3', 'folder1', app_db=app_db)
    insertTagFolder('tag1', 'folder2', app_db=app_db)
    insertTagFolder('tag4', 'folder2', app_db=app_db)

    insertTagFolder('tag1', 'folder3', app_db=app_db)
    insertTagFolder('tag4', 'folder3', app_db=app_db)
    insertTagFolder('tag3', 'folder3', app_db=app_db)
    insertTagFolder('tag1', 'folder5', app_db=app_db)
    insertTagFolder('tag4', 'folder4', app_db=app_db)
    insertTagFolder('tag2', 'folder4', app_db=app_db)

    # tag1(1, 2, 3, 5)  tag4(2, 3, 4)
    query = 'tag1 -tag4'

    print(get_folders_by_tags(queryBuilder.filterResultsDb(query), app_db=app_db))


# test_insert_some_values()
