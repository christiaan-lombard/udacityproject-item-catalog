from flask import Flask, jsonify, request, url_for, abort, g, render_template, make_response, redirect, flash, send_from_directory
from models import Base, User, Item, Category, init_db, ModelNotFoundError
from security import Auth, CSRFProtect, UnauthorizedError, random_string, CSFRTokenError
from upload import validate_file, upload_exists, Uploader
from utils import slugify, form_has
from oauth2client.client import FlowExchangeError
import json, os

dirname = os.path.dirname(os.path.abspath(__file__))
upload_path = os.path.join(dirname, 'static/pictures')

app = Flask(__name__)
csfr = CSRFProtect()
auth = Auth()
uploader = Uploader(upload_path)

@app.route('/')
def show_home():
    latest_items = Item.latest(10)

    return render_template('home.html',latest_items=latest_items)



@app.route('/items/<string:slug>')
def show_item_category(slug):
    category = Category.find_or_fail(slug)
    items = category.items

    return render_template('item_list.html',
            items=items,
            list_title=category.title
        )


@app.route('/login')
def show_login():
    return_to = request.args.get('return_to', url_for('show_home'))

    return render_template('login.html',
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

@app.route('/items/<int:id>', methods=['GET'])
def show_item(id):
    item = Item.find_or_fail(id)
    return render_template('item_detail.html', item=item)

@app.route('/user/<int:id>/items')
@auth.requires_login
def show_user_items(id):
    user = User.find(id)
    user_items = Item.for_user(user.id)

    return render_template('item_list.html',
            items=user_items,
            list_title="{}'s Items".format(user.name)
        )


@app.route('/items/add', methods=['GET', 'POST'])
@app.route('/items/<int:id>/edit', methods=['GET', 'POST'])
@auth.requires_login
@csfr.requires_token
def edit_item(id = None):

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
        if form_has(request.form, 'should_upload') and upload_exists(request, 'picture_file'):
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
    item = Item.find_or_fail(id)
    user = auth.user()

    if item.user_id != user.id:
        raise UnauthorizedError('Not authorized to delete item.')

    t, filename = item.get_picture_info()

    if t == 'UPLOAD':
        uploader.delete(filename)

    item.delete()
    flash("Item '{}' is gone!")
    return redirect(url_for('show_user_items', id=user.id))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.context_processor
def inject_globals():
    return dict(
        user=auth.user(),
        categories=Category.all(),
        token=csfr.generate_token()
    )

@app.before_request
def reset_globals():
    g.show_sidebar = True


@app.errorhandler(404)
@app.errorhandler(ModelNotFoundError)
def handle_error_not_found(error):
    return render_template('error.html',
        error_title='404 Not Found',
        error_message="The resource you are looking for does not exist."
    ), 404

@app.errorhandler(CSFRTokenError)
def handle_error_bad_token(error):
    return render_template('error.html',
        error_title='400 Token Error',
        error_message="Something was missing in that request. Please try again."
    ), 404

def json_response(data, status):
    response = make_response(json.dumps(data),status)
    response.headers['Content-Type'] = 'application/json'
    return response




if __name__ == '__main__':
    init_db()
    app.config['UPLOAD_FOLDER'] = upload_path
    app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)