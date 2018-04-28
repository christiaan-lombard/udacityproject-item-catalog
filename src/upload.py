import os
from security import random_string
from flask import url_for, send_from_directory


"""Application file upload helpers"""
__author__ = "Christiaan Lombard <base1.christiaan@gmail.com>"


# defines the application's allowed upload extensions
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


class Uploader:
    """ A service for dealing with uploaded files"""

    def __init__(self, upload_path):
        """Create a new instance preconfigured with upload folder
        Arguments:
            upload_path (string) -- Path where uploaded files are stored
        """

        self.upload_path = upload_path

    def delete(self, filename):
        """Delete an uploaded file

        Arguments:
            filename (string) -- filename relative to upload folder
        """

        path = os.path.join(self.upload_path, filename)
        if os.path.exists(path):
            os.remove(path)

    def upload(self, file):
        """Save filestream to upload folder

        Arguments:
            file (werkzeug.datastructures.FileStorage)
                -- The filestream to save

        Returns:
            string -- Filename relative to upload folder,
                        for retrieving the file
        """

        ext = get_ext(file.filename)
        filename = random_string(16) + '.' + ext
        dest = os.path.join(self.upload_path, filename)
        file.save(dest)
        return filename

    def serve(self, filename):
        """Serve an uploaded file

        Arguments:
            filename (string) -- Filename as provided by upload(file)

        Returns:
            string -- Http file response
        """

        return send_from_directory(self.upload_path, filename)


def upload_exists(request, key):
    """Convenience function for checking the existence
    of a file in a flask request

    Arguments:
        request (flask.Request) -- The request object
        key (striung) -- Dictionary key of the file to check

    Returns:
        boolean -- Whether the file exists and is not empty
    """

    return key in request.files and request.files[key].filename != ''


def validate_file(file):
    """ Validate a filestream against the defined allowed extensions

    Arguments:
        file (werkzeug.datastructures.FileStorage) -- The filestream to check

    Returns:
        boolean -- Whether the file is valid
    """

    if allowed_file(file.filename):
        return True
    return False


def get_ext(filename):
    """Get the extension part of a filename

    Arguments:
        filename (string) -- The filename to check

    Returns:
        string -- The extension (without the '.')
    """

    return filename.rsplit('.', 1)[1].lower()


def allowed_file(filename):
    return '.' in filename and \
           get_ext(filename) in ALLOWED_EXTENSIONS
