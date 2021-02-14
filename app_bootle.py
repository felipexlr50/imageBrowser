from bottle import static_file,  Bottle, run, template

app = Bottle()


@app.route('/content/script/:filename#.*#')
def get_js(filename):
    return static_file(filename, root="content/script")


@app.route('/content/css/:filename#.*#')
def get_js(filename):
    return static_file(filename, root="content/css")


@app.route('/')
def index():
    return template('index.tpl')


run(app=app, port=8000, server='paste', debug=True)
