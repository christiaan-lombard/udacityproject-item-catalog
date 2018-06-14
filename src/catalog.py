#!/usr/bin/env python
from flask import (Flask, jsonify, request,
                   url_for, abort, g, render_template,
                   make_response, redirect, flash,
                   send_from_directory)
from models import (Base, User, Item, Category,
                    init_db, ModelNotFoundError)
from security import (Auth, CSRFProtect, UnauthorizedError,
                      random_string, CSFRTokenError)
from upload import validate_file, upload_exists, Uploader
from utils import slugify, form_has
from oauth2client.client import FlowExchangeError
from werkzeug.exceptions import HTTPException

import json
import os


"""Udacity Project - Item Catalog"""
__author__ = "Christiaan Lombard <base1.christiaan@gmail.com>"


# get the upload path relative to the application folder
dirname = os.path.dirname(os.path.abspath(__file__))
upload_path = os.path.join(dirname, 'static/pictures')

# setup app and services
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = upload_path
csfr = CSRFProtect()
auth = Auth()
uploader = Uploader(upload_path)

#
# WEB ROUTES
#


@app.route('/')
def show_home():
    """Show the application home page"""

    latest_items = Item.latest(10)

    return render_template('home.html', latest_items=latest_items)


@app.route('/items/<string:slug>')
def show_item_category(slug):
    """List the items in a category

    Arguments:
        slug (string) -- The slug of the category to lookup
    """

    category = Category.find_or_fail(slug)
    items = category.items

    return render_template('item_list.html',
                           items=items,
                           list_title=category.title)


@app.route('/login')
def show_login():
    """Show the login page"""

    return_to = request.args.get('return_to', url_for('show_home'))
    client_id = auth.google_client_secrets['web']['client_id']

    return render_template('login.html',
                           google_client_id=client_id,
                           return_to=return_to)


@app.route('/oauth/google/callback', methods=['POST'])
@csfr.requires_token
def oauth_google_callback():
    """Callback response function for a Google Oauth2 request"""
    code = request.form['code']
    auth.loginGoogle(code)

    return json_response('Success!', 200)


@app.route('/logout', methods=['POST'])
def logout():
    """Logout the current user"""
    auth.logoutGoogle()
    flash("You have been logged out.")
    return redirect(url_for('show_home'))


@app.route('/items/<int:id>', methods=['GET'])
def show_item(id):
    """Show the details of an item

    Arguments:
        id (integer) -- The id of the item
    """

    item = Item.find_or_fail(id)
    return render_template('item_detail.html', item=item)


@app.route('/user/<int:id>/items')
def show_user_items(id):
    """Show a list of a user's items

    Arguments:
        id (integer) -- The user's id
    """

    user = User.find(id)
    user_items = Item.for_user(user.id)

    return render_template('item_list.html',
                           items=user_items,
                           list_title="{}'s Items".format(user.name))


@app.route('/items/add', methods=['GET', 'POST'])
@app.route('/items/<int:id>/edit', methods=['GET', 'POST'])
@auth.requires_login
@csfr.requires_token
def edit_item(id=None):
    """Edit or create an item

    Keyword Arguments:
        id (integer) -- The id of the item to edit or
            None to create a new item (default: {None})

    Raises:
        UnauthorizedError -- If the user is not the owner of the item
    """

    user = auth.user()

    if not id:
        action = 'create'
        item = Item.make()
    else:
        action = 'update'
        item = Item.find_or_fail(id)
        if item.user_id != user.id:
            raise UnauthorizedError('Not authorized to edit item.')

    if request.method == 'POST':

        # valid until proven otherwise
        valid = True

        if form_has(request.form, 'name'):
            item.name = request.form['name']
        else:
            valid = False
            flash('Please enter a name for the item.')

        if form_has(request.form, 'description'):
            item.description = request.form['description']

        # validate category and add category if new specified
        if form_has(request.form, 'category_slug'):
            if request.form['category_slug'] == '_new_':
                title = request.form['new_category_title']
                slug = slugify(title)
                if not slug:
                    flash('Category title can not be empty.')
                    valid = False
                else:
                    category = Category.create(title=title, slug=slug)
                    item.category_slug = slug
            else:
                item.category_slug = request.form['category_slug']
        else:
            valid = False
            flash('Select a category for the item.')

        # upload picture or take form link
        if form_has(request.form, 'should_upload') \
                and upload_exists(request, 'picture_file'):
            file = request.files['picture_file']
            if not validate_file(file):
                flash('What was that file?! Select a picture file please...')
                valid = False
            else:
                # delete current file if uploaded
                t, filename = item.get_picture_info()
                if t == 'UPLOAD':
                    uploader.delete(filename)
                # upload picture and keep fileref
                item.set_picture_upload(uploader.upload(file))
        elif form_has(request.form, 'picture_link'):
            # delete current file if uploaded
            t, filename = item.get_picture_info()
            if t == 'UPLOAD':
                uploader.delete(filename)
            # set picture from link
            item.set_picture_link(request.form['picture_link'])

        item.user_id = user.id

        if valid:
            item.save()
            flash("Item '%s' added!" % item.name)
            return redirect(url_for('show_item', id=item.id))

    g.show_sidebar = False
    return render_template('item_form.html', item=item, action=action)


@app.route('/items/<int:id>/delete', methods=['POST'])
@auth.requires_login
@csfr.requires_token
def delete_item(id):
    """Delete an item

    Arguments:
        id (iteger) -- The id of the item

    Raises:
        UnauthorizedError -- If the user is not the owner of the item
    """

    item = Item.find_or_fail(id)
    user = auth.user()

    if item.user_id != user.id:
        raise UnauthorizedError('Not authorized to delete item.')

    t, filename = item.get_picture_info()
    item_name = item.name

    if t == 'UPLOAD':
        uploader.delete(filename)

    item.delete()
    flash("Item '{}' is gone!".format(item_name))
    return redirect(url_for('show_user_items', id=user.id))


#
# API ROUTES
#


@app.route('/api/items/<int:id>', methods=['GET'])
def api_get_item(id):
    """Get the item info

    Arguments:
        id (integer) -- The id of the item
    """
    item = Item.find_or_fail(id)
    return json_response(item.serialize, 200)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Get an uploaded file

    Arguments:
        filename (string) -- The filename as uploaded
    """

    return uploader.serve(filename)


#
# FLASK HANDLERS
#

@app.context_processor
def inject_globals():
    """Inject global vars required by html templates"""

    return dict(
                user=auth.user(),
                categories=Category.all(),
                token=csfr.generate_token())


@app.before_request
def reset_globals():
    """Reset global vars to default state

        Requests may alter these defaults
    """

    g.show_sidebar = True


@app.errorhandler(HTTPException)
def catch_http_errors(error):
    """Respond to errors

    Arguments:
        error (HTTPException) -- The error that occured
    """
    return render_template('error.html',
                           error_title=error.code,
                           error_message=error.description
                           ), error.code


def json_response(data, status):
    """Make an http JSON response

    Arguments:
        data (dict) -- The data to encode
        status (integer) -- The http reponse status

    Returns:
        string -- Http response with json body
    """

    response = make_response(json.dumps(data), status)
    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == '__main__':
    init_db('sqlite:///catalog.db', True)
    app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
