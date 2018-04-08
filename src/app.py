from models import Base, User, Item, Category, init_db
from flask import Flask, jsonify, request, url_for, abort, g, render_template

app = Flask(__name__)


@app.route('/')
def showHome():
    return render_template('home.html')


@app.route('/login')
def showLogin():
    return render_template('login.html')




@app.context_processor
def inject_latest():
    return dict(latest_items=Item.latest(10))


if __name__ == '__main__':
    init_db()
    app.debug = True
    app.run(host='0.0.0.0', port=5000)