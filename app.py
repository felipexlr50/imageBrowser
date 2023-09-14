from constant import CONTENT, LIMIT, MAIN_FILE_PATH
import db_util
import image_processing
import logging
import json
import os
import util
from bottle import static_file, Bottle, template, TEMPLATE_PATH,  run, response, request
from urllib.parse import unquote

# logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.DEBUG)
# TODO:
# - debug api tag put

logging.basicConfig(handlers=[logging.FileHandler(filename="app.log",
                                                  encoding='utf-8', mode='a+')],
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s",
                    datefmt="%F %A %T",
                    level=logging.DEBUG)

logging.getLogger().addHandler(logging.StreamHandler())


TEMPLATE_PATH.insert(0, 'content/views')

app = Bottle()


def enable_cors(fn):
    def _enable_cors(*args, **kwargs):
        # set CORS headers
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

        if request.method != 'OPTIONS':
            # actual request; reply with the actual response
            return fn(*args, **kwargs)

    return _enable_cors


@enable_cors
@app.get('/api/images/latest')
def get_latest_images():

    image_list = list(db_util.get_latest_folders(LIMIT))

    return json.dumps(image_processing.get_latest_from_file(image_list))


@enable_cors
@app.route('/load-image/<filename:path>')
def serve_image(filename):
    img_path_encoded = unquote(filename)

    actual_filename = util.B64SafeToString(img_path_encoded)

    # Construct the absolute file path
    file_path = os.path.join(MAIN_FILE_PATH, actual_filename)

    # Check if the file exists and is within the MAIN_FILE_PATH directory
    if os.path.exists(file_path) and os.path.commonprefix([file_path, MAIN_FILE_PATH]) == MAIN_FILE_PATH:
        return static_file(actual_filename, root=MAIN_FILE_PATH, mimetype='image/jpeg')
    else:
        # Return an error response if the filename is not valid
        return json.dumps({"status_code": 400, "message": f"Invalid filename: {filename}"}), 400


@enable_cors
@app.get('/api/images/<bookname>')
def get_folder_images(bookname):
    foldername_encoded = unquote(bookname)

    actual_foldername = os.path.dirname(
        util.B64SafeToString(foldername_encoded))

    return json.dumps(image_processing.get_image_list_from_path(actual_foldername))


def get_image_by_name(image_name, folder):
    return image_processing.get_image(image_name, folder)


@enable_cors
@app.put('/api/tags')
def set_tag():
    data = request.json
    foldername_encoded = unquote(data["book"])

    actual_bookname = os.path.dirname(util.B64SafeToString(foldername_encoded))

    db_util.set_tag(unquote(data["tag"]), actual_bookname)


@enable_cors
@app.get('/api/tags/<bookname>')
def get_tags(bookname):
    foldername_encoded = unquote(bookname)

    actual_bookname = os.path.dirname(
        util.B64SafeToString(foldername_encoded))
    return json.dumps(db_util.get_tags(actual_bookname))


def get_search_results(query):
    return db_util.filter_results(query)


@enable_cors
@app.get('/script/:filename#.*#')
def get_js(filename):
    return static_file(filename, root="content/script")


@enable_cors
@app.get('/css/:filename#.*#')
def get_css(filename):
    return static_file(filename, root="content/css")


@enable_cors
@app.get('/favicon.ico')
def icon():
    return static_file('favicon.ico', root=CONTENT)


@enable_cors
@app.route('/home')
def index():
    return static_file('views/index.html', root=CONTENT)


@enable_cors
@app.route('/book/<id>')
def book(id):
    print(id)
    return static_file('views/book.html', root=CONTENT)


@enable_cors
@app.get('/api/book/<id>')
def get_book(id):
    print(id)
    book_obj = db_util.get_folder_by_id(id)
    return json.dumps(image_processing.get_book(book_obj))


@enable_cors
@app.route('/search/<query>', root=CONTENT)
def search(query):
    return template('search', pQuery=query)


@app.error(500)
@app.error(404)
def error(error):
    logging.error(f"An error occurred: {error}")
    return static_file('views/error.html', root=CONTENT)


db_util.init_database()

run(app=app, port=8000, server='paste', debug=True, reloader=True)
