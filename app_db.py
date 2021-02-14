import sqlite3
import queryBuilder
import logging
import sys
import zlib


DEFAULT_NAME = 'app.db'
app_db = DEFAULT_NAME

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

SELECT_LATEST_FOLDERS = '''
SELECT * FROM Folder
ORDER BY added_date DESC
LIMIT 0,{}
'''

SELECT_COUNT_FOLDERS = "SELECT COUNT(*) FROM Folder"


def set_db_name(db_name=DEFAULT_NAME):
    app_db = db_name


def create_connection():
    connection = None
    try:
        connection = sqlite3.connect(app_db)
    except:
        print(sys.exc_info()[0])

    finally:
        return connection


def create_tables():
    connection = create_connection()
    c = connection.cursor()
    c.execute(CREATE_TABLE_TAG)
    c.execute(CREATE_TABLE_FOLDER)
    c.execute(CREATE_TABLE_TAG_FOLDER)

    connection.commit()
    connection.close()


def get_folders_by_tags(*tags):
    connection = create_connection()
    c = connection.cursor()

    tagArray = list(map(lambda x: str("'"+str(x)+"'"), tags[0][0]))
    negTagArray = list(map(lambda x: str("'"+str(x)+"'"), tags[0][1]))

    tagString = ", ".join(tagArray) if len(tagArray) > 0 else ""
    negTagString = ", ".join(negTagArray) if len(negTagArray) > 0 else ""

    sqlQuerry = str(SELECT_FOLDERS_BY_TAG).format(
        negTagString, tagString, len(tagArray))

    result = c.execute(sqlQuerry).fetchall()
    connection.close()

    return result


def get_latest_folders(n=30):
    connection = create_connection()
    c = connection.cursor()

    sqlQuerry = str(SELECT_LATEST_FOLDERS).format(n)

    result = c.execute(sqlQuerry).fetchall()
    connection.close()

    return result


def get_folders_tags():
    connection = create_connection()
    c = connection.cursor()

    result = c.execute(SELECT_FOLDERS_TAGS).fetchall()
    connection.close()

    return result


def get_folder_count():
    connection = create_connection()
    c = connection.cursor()

    result = c.execute(SELECT_COUNT_FOLDERS).fetchall()
    connection.close()

    return result


def insertTag(tag):
    try:
        connection = create_connection()
        c = connection.cursor()
        c.execute("INSERT INTO Tag(tagName) VALUES('{}')".format(tag))
        connection.commit()
        connection.close()
    except:
        logging.error(f"Failed to insert to data base: {sys.exc_info()[0]}")


def insertFolder(folder, path):
    try:
        id = zlib.adler32(folder.encode())
        connection = create_connection()
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


def insertTagFolder(tag, folder):
    try:
        connection = create_connection()
        c = connection.cursor()

        c.execute("INSERT INTO tag_folder(tagName, folderName) VALUES('{}', '{}')".format(
            tag, folder))

        connection.commit()
        connection.close()
    except:
        logging.error(f"Failed to insert to data base: {sys.exc_info()[0]}")


def test_insert_some_values():

    set_db_name('test.db')
    create_tables()
    insertTag('tag1')
    insertTag('tag2')
    insertTag('tag3')
    insertTag('tag4')

    insertFolder('folder1', '/path1')
    insertFolder('folder2', '/path2')
    insertFolder('folder3', '/path3')
    insertFolder('folder4', '/path4')
    insertFolder('folder5', '/path5')

    insertTagFolder('tag1', 'folder1')
    insertTagFolder('tag2', 'folder1')
    insertTagFolder('tag3', 'folder1')
    insertTagFolder('tag1', 'folder2')
    insertTagFolder('tag4', 'folder2')

    insertTagFolder('tag1', 'folder3')
    insertTagFolder('tag4', 'folder3')
    insertTagFolder('tag3', 'folder3')
    insertTagFolder('tag1', 'folder5')
    insertTagFolder('tag4', 'folder4')
    insertTagFolder('tag2', 'folder4')

    toPrint = queryBuilder.filterResults('tag2 tag4', get_folders_tags())

    toPrint2 = get_folders_by_tags(queryBuilder.filterResultsDb('tag2 tag4'))
