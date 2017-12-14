import os
from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/uploading', methods=['POST'])
def upload():
    img_folder = os.path.join(APP_ROOT, 'images')
    if not os.path.isdir(img_folder):
        os.mkdir(img_folder)

    for up in request.files.getlist("file"):
        filename = up.filename
        target = "/".join([img_folder, filename])
        up.save(target)

    return render_template('index.html', img = filename)


@app.route('/upload/<filename>')
def send_img(filename):
    return send_from_directory("images", filename)


if __name__ == '__main__':
    app.run(debug=True, port=4004)
