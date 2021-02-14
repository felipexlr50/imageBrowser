from constant import CONTENT, LIMIT
import eel
import db_util
import image_processing
import logging
from bottle import static_file, Bottle

#logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.DEBUG)

eel.init('content')

app = Bottle()


@eel.expose
def get_images():
    return image_processing.get_latest(LIMIT)


@eel.expose
def get_folder_images(image_name):
    return image_processing.get_all_image(image_name, 500)


@eel.expose
def get_image_by_name(image_name, folder):
    return image_processing.get_image(image_name, folder)


@app.route('/script/:filename#.*#')
def get_js(filename):
    return static_file(filename, root="content/script")


@app.route('/css/:filename#.*#')
def get_js(filename):
    return static_file(filename, root="content/css")


@app.route('/home')
def index():
    return static_file('index.html', root=CONTENT)


@app.route('/book/<id>')
def book(id):
    print(id)
    return static_file('book.html', root=CONTENT)


db_util.init_database()


eel.start('index', app=app, mode=False)
