from flask import Flask, jsonify, request, url_for, abort, g, render_template, make_response, redirect, flash
from models import Base, User, Item, Category, init_db
from security import Auth, CSRFProtect, UnauthorizedError, random_string
from upload import validate_file, upload_file, upload_exists
from oauth2client.client import FlowExchangeError
import json, os

app = Flask(__name__)
csfr = CSRFProtect()
auth = Auth()

@app.route('/')
def show_home():
    latest_items = Item.latest(10)

    return render_template('home.html',latest_items=latest_items)

@app.route('/my-items')
@auth.requires_login
def show_my_items():
    user = auth.user()
    user_items = Item.for_user(user.id)

    return render_template('item_list.html',
            items=user_items,
            list_title="My Items"
        )


@app.route('/login')
def show_login():
    return_to = request.args.get('return_to', url_for('show_home'))

    return render_template('login.html',
        token=csfr.generate_token(),
        google_client_id = auth.google_client_secrets['web']['client_id'],
        return_to=return_to
    )

@app.route('/logout', methods=['POST'])
def logout():
    auth.logout()
    return redirect(url_for('show_home'))


@app.route('/oauth/google/callback', methods=['POST'])
@csfr.requires_token
def oauth_google_callback():
    code = request.form['code']
    # try:
    auth.loginGoogle(code)
    # except FlowExchangeError:
        # return json_response('Failed to exchange code for access token', 401)

    return json_response('Success!', 200)

@app.route('/items/<int:item_id>', methods=['GET'])
def show_item(item_id):
    item = Item.find_or_fail(item_id)
    return render_template('item_detail.html', item=item)




@app.route('/items/add', methods=['GET', 'POST'])
@auth.requires_login
# @csfr.requires_token
def create_item():
    item = Item.make()
    user = auth.user()

    if user and request.method == 'POST':

        # if upload_exists(request, 'picture_file'):
        #     file = request.files['picture_file']
        #     if not validate_file(file):
        #         flash('Invalid file upload')
        #         return redirect(request.url)
        #     else
        #         upload_file(file)

        picture = ''

        item.fill(
            name=request.form['name'],
            picture=picture,
            description=request.form['description'],
            user_id=user.id,
            category_slug=request.form['category_slug']
        )
        item.save()
        flash("Item '%s' added!" % item.name)
        return redirect(url_for('show_item', item_id=item.id))

    token = csfr.generate_token()
    g.show_sidebar = False
    return render_template('item_form.html', item=item, action='create', token=token)


@app.route('/items/edit/<int:id>', methods=['GET', 'POST'])
def edit_item(id):
    item = Item.find_or_fail(id)
    user = auth.user()

    if user and user.id != item.user_id:
        raise UnauthorizedError('User not authorized to edit item.')

    if user and request.method == 'POST':
        item.fill(
            name=request.form['name'],
            picture=request.form['picture'],
            description=request.form['description'],
            category_slug=request.form['category_slug']
        )
        item.save()
        flash("Item '%s' added!" % item.name)
        return redirect(url_for('showItem', item_id=item.id))

    g.show_sidebar = False
    return render_template('item_form.html', item=item, action='update')


@app.context_processor
def inject_globals():
    return dict(
        user=auth.user(),
        categories=Category.all()
    )

@app.before_request
def reset_globals():
    g.show_sidebar = True

@app.errorhandler(Exception)
def all_exception_handler(error):
   return render_template('error.html', error_title='Oops!', error_message=error)

def json_response(data, status):
    response = make_response(json.dumps(data),status)
    response.headers['Content-Type'] = 'application/json'
    return response




if __name__ == '__main__':
    init_db()
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)