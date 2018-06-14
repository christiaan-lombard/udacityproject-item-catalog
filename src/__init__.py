import os
from catalog import app, init_db

init_db(os.environ['APP_DATABASE'], False)
app.config['MAX_CONTENT_LENGTH'] = int(os.environ['APP_MAX_UPLOAD'])
app.secret_key = os.environ['APP_SECRET']
app.debug = (os.environ['APP_DEBUG'] == 'true')
