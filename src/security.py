from flask import session, request
from models import User
from functools import wraps
import random, string, json, requests

from oauth2client.client import flow_from_clientsecrets, FlowExchangeError


class UnauthorizedError(RuntimeError):
    pass

class UnauthenticatedError(RuntimeError):
    pass

class Auth:

    def __init__(self):
        self.google_client_secrets = \
            json.loads(open('google_client_secrets.json', 'r').read())

    def redirectUrlGoogle(self):
        pass


    def loginGoogle(self, code):
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('google_client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)

        # Get user info
        userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {'access_token': credentials.access_token, 'alt': 'json'}
        userinfo = requests.get(userinfo_url, params=params).json()

        user = User.find_by_email(userinfo['email'])

        if user is None:
            user = User.make(
                name=userinfo['name'],
                email=userinfo['email'],
                picture=userinfo['picture']
            )
            # generate a random password
            user.set_password(random_string(32))
            user.save()

        self.login(user)


    def login(self, user):
        session['user_id'] = user.id

    def logout(self):
        del session['user_id']

    def requires_login(self, func):
        @wraps(func)
        def check_login(*args, **kwargs):
            user = self.user()
            if user is None:
                raise UnauthenticatedError("Requires a logged in user.")
            return func(*args, **kwargs)
        return check_login

    def user(self):
        user_id = session.get('user_id')
        if user_id is None:
            return None
        return User.find(user_id)



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
                    raise CSFRTokenError("CSFR token missing or invalid: %s" % request_token)
            return func(*args, **kwargs)
        return check_token


def random_string(lenght = 32):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(lenght))