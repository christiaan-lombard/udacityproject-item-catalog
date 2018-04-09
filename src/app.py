from flask import Flask, jsonify, request, url_for, abort, g, render_template, make_response
from models import Base, User, Item, Category, init_db
from security import Auth, CSRFProtect
from oauth2client.client import FlowExchangeError
import json

app = Flask(__name__)
csfr = CSRFProtect()
auth = Auth()

@app.route('/')
def showHome():
    return render_template('home.html')


@app.route('/login')
def showLogin():
    return_to = request.args.get('return_to', url_for('showHome'))

    return render_template('login.html',
        token=csfr.generate_token(),
        google_client_id = auth.google_client_secrets['web']['client_id'],
        return_to=return_to
    )

@app.route('/oauth/google/callback', methods=['POST'])
@csfr.requires_token
def oauthGoogleCallback():
    code = request.form['code']
    # try:
    auth.loginGoogle(code)
    # except FlowExchangeError:
        # return json_response('Failed to exchange code for access token', 401)

    return json_response('Success!', 200)




@app.context_processor
def inject_latest():
    return dict(
        latest_items=Item.latest(10)
    )


def json_response(data, status):
    response = make_response(json.dumps(data),status)
    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == '__main__':
    init_db()
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)