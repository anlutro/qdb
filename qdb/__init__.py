from flask import (Flask, url_for, render_template, jsonify,
	redirect, abort, flash, request, session)
app = Flask(__name__)

# find the project root directory
import os.path
dirname = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# runtime/local configuration via config.py
cfg_file_path = os.path.join(dirname, 'config.py')
app.config.from_pyfile(cfg_file_path)

# enable bytecode caching for templates
from jinja2 import FileSystemBytecodeCache
from werkzeug.datastructures import ImmutableDict
j2cachedir = os.path.join(dirname, 'tmp', 'j2cache')
app.jinja_options = ImmutableDict(
	extensions = ['jinja2.ext.with_'],
	bytecode_cache = FileSystemBytecodeCache(j2cachedir, '%s.cache'),
)

# set up logging to stderr
if not app.debug:
    import logging, sys
    file_handler = logging.StreamHandler(sys.stderr)
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

# replace the json encoder
from qdb.utils import CustomJSONEncoder
app.json_encoder = CustomJSONEncoder

# register routes
import qdb.routes

# initialize the database session
from qdb.database import init_db, db_session
init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
	db_session.remove()

# inject the pending_count variable as a jinja global
@app.context_processor
def inject_pending_count():
	if not session.get('logged_in'):
		return dict()

	query = db_session.query(Quote) \
		.filter(Quote.approved == False)
	count = query.count()
	return {'pending_count': count}
