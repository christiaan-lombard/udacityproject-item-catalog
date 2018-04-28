from flask import session, request
from models import User
from functools import wraps
import random, string, json, requests, httplib2

from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
from werkzeug.exceptions import abort
from werkzeug.exceptions import HTTPException


class UnauthenticatedError(HTTPException):
    """Error signifying an attempt to access a resource that requires authentication"""
    code = 401
    description = "Resource requires user authentication"

class UnauthorizedError(HTTPException):
    """Error signifying an attempt to access a restricted resource"""
    code = 403
    description = "Access to restricted resource denied"

class OAuthFlowError(HTTPException):
    """Generic error for error occuring during OAuth flow"""
    code = 400
    description = "Something went wrong during OAuth flow"

class CSFRTokenError(HTTPException):
    """Error signifying the lack of / or invalid CSFR token"""
    code = 400
    description = "CSFR token missing or invalid"


class Auth:

    def __init__(self):
        """Make an Auth instance"""

        self.google_client_secrets = \
            json.loads(open('google_client_secrets.json', 'r').read())


    def loginGoogle(self, code):
        """Login/register the relevant user with google oauth code

        Arguments:
            code (string) -- The code as supplied by Google Oauth2 callback
        """

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

        # keep login details in session
        session['auth_type'] = 'google'
        session['user_id'] = user.id
        session['access_token'] = credentials.access_token
        return user


    def logoutGoogle(self):
        """Logout the currently authenticated user"""

        access_token = session['access_token']

        # clear the session first in case something goes wrong
        del session['user_id']
        del session['auth_type']
        del session['access_token']

        # revoke access token if present
        if access_token:
            url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
            response = httplib2.Http().request(url, 'GET')[0]
            if response['status'] != '200':
                raise OAuthFlowError()



    def requires_login(self, func):
        """Decorate a flask route to require a logged in user

        Arguments:
            func (function) -- The function to decorate

        Raises:
            UnauthenticatedError -- If there is no user authenticated

        Returns:
            function -- The decorator
        """

        @wraps(func)
        def check_login(*args, **kwargs):
            user = self.user()
            if user is None:
                raise UnauthenticatedError()
            return func(*args, **kwargs)
        return check_login

    def user(self):
        """Get the currently authenticated user

        Returns:
            models.User -- The currently authenticated user or None
        """

        user_id = session.get('user_id')
        if user_id is None:
            return None
        return User.find(user_id)





class CSRFProtect:

    def generate_token(self):
        """Generate a token or get the current token from the flask session

        Returns:
            string -- The token to add to form request
        """

        if '_csfr_token_' not in session:
            session['_csfr_token_'] = random_string(64)
        return session['_csfr_token_']

    def requires_token(self, func):
        """Decorate a flask route tocheck for a CSFR token
        on POST requests

        Arguments:
            func (function) -- The function to decorate

        Raises:
            CSFRTokenError -- If the token is not present or invalid

        Returns:
            function -- The decorator
        """

        @wraps(func)
        def check_token(*args, **kwargs):
            if request.method == 'POST':
                session_token = session.pop('_csfr_token_', None)
                request_token = request.form.get('_csfr_token_')
                if not session_token or session_token != request_token:
                    raise CSFRTokenError()
            return func(*args, **kwargs)
        return check_token


def random_string(lenght = 32):
    """Generate a random string of
    uppercase and number characters

    Keyword Arguments:
        lenght (integer) -- The length of string to generate (default: {32})

    Returns:
        string -- The random string
    """

    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(lenght))