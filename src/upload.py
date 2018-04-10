import os

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
DIRNAME = os.path.dirname(__file__)
UPLOAD_PATH = os.path.join(DIRNAME, '/static/pictures')

def upload_exists(request, key):
    return key in request and request.files[key].filename != ''

def validate_file(file):
    if allowed_file(file.filename):
        return True
    return False

def upload_file(file):
    pass


def get_ext(filename):
    return filename.rsplit('.', 1)[1].lower()

def allowed_file(filename):
    return '.' in filename and \
           get_ext(filename) in ALLOWED_EXTENSIONS
