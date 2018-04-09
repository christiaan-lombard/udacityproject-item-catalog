from flask import Flask, jsonify, request, url_for, abort, g, render_template, make_response, redirect, flash
from models import Base, User, Item, Category, init_db
from security import Auth, CSRFProtect
from oauth2client.client import FlowExchangeError
import json

app = Flask(__name__)
csfr = CSRFProtect()
auth = Auth()

@app.route('/')
def showHome():
    latest_items = Item.latest(10)

    return render_template('item_list.html',
        list_title="Latest Items",
        list_description="",
        list_items=latest_items
    )


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

@app.route('/items/<int:item_id>', methods=['GET'])
def showItem(item_id):
    item = Item.find_or_fail(item_id)
    return render_template('item_detail.html', item=item)


@app.route('/items/add', methods=['GET', 'POST'])
@csfr.requires_token
def createItem():
    item = Item.make()
    user = auth.user()

    if user and request.method == 'POST':
        item.fill(
            name=request.form['name'],
            picture=request.form['picture'],
            description=request.form['description'],
            user_id=user.id,
            category_slug=request.form['category_slug']
        )
        item.save()
        flash("Item '%s' added!" % item.name)
        return redirect(url_for('showItem', item_id=item.id))

    return render_template('item_form.html', item=item)




@app.context_processor
def inject_latest():
    return dict(
        user=auth.user(),
        categories=Category.all()
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