import os
from security import random_string
from flask import url_for

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_PATH = '/vagrant/src/static/pictures'
UPLOAD_URL = 'pictures'

class Uploader:

    def __init__(self, upload_path):
        self.upload_path = upload_path

    def delete(self, filename):
        path = os.path.join(self.upload_path, filename)
        if os.path.exists(path):
            os.remove(path)

    def upload(self, file):
        ext = get_ext(file.filename)
        filename = random_string(16) + '.' + ext
        dest = os.path.join(self.upload_path, filename)
        file.save(dest)
        return filename


def upload_exists(request, key):
    return key in request.files and request.files[key].filename != ''

def validate_file(file):
    if allowed_file(file.filename):
        return True
    return False

def get_ext(filename):
    return filename.rsplit('.', 1)[1].lower()

def allowed_file(filename):
    return '.' in filename and \
           get_ext(filename) in ALLOWED_EXTENSIONS
