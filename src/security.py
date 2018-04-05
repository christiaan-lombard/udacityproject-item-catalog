from flask import session, request
from models import User
from functools import wraps
import random, string

class Auth:
    def login(self, user):
        session.set('user_id', user.id)

    def requires_login(self, func):
        @wraps(func)
        def check_login(*args, **kwargs):
            user_id = session.get('user_id')
            if user_id is None:
                pass
        return check_login


class CSFRTokenError(RuntimeError):
    pass

class CSRFProtect:

    def generate_token(self):
        if '_csfr_token_' not in session:
            session['_csfr_token_'] = random_string(64)
        return session['_csfr_token_']

    def requires_token(self, func):
        @wraps(func)
        def check_token(*args, **kwargs):
            if request.method == 'POST':
                session_token = session.pop('_csfr_token_', None)
                request_token = request.form.get('_csfr_token_')
                if not session_token or session_token != request_token:
                    raise CSFRTokenError("CSFR token missing or invalid")
        return check_token


def random_string(lenght = 32):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(lenght))