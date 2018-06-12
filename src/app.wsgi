from app import app as application

init_db('postgresql://grader:supersecret@localhost/catalog', False)
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
app.secret_key = 'super_secret_key'
app.debug = False