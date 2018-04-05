from models import Base, User, Item, Category
from flask import Flask, jsonify, request, url_for, abort, g

app = Flask(__name__)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)