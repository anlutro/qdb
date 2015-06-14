# find the project root directory
import os.path
root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# initiate the flask app
from flask import Flask
app = Flask(__name__, static_folder=os.path.join(root, 'public'))

# runtime/local configuration via config.py
cfg_file_path = os.path.join(root, 'config.py')
app.config.from_pyfile(cfg_file_path)

if not app.debug:
	# enable bytecode caching for templates
	from jinja2 import FileSystemBytecodeCache
	from werkzeug.datastructures import ImmutableDict
	j2cachedir = os.path.join(root, 'tmp', 'j2cache')
	app.jinja_options = ImmutableDict(
		extensions = ['jinja2.ext.with_'],
		bytecode_cache = FileSystemBytecodeCache(j2cachedir, '%s.cache'),
	)

	# set up logging to stderr
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

# inject global jinja variables
from qdb.models import Quote
from flask import session
@app.context_processor
def jinja_globals():
	context = dict()

	if session.get('logged_in'):
		context['pending_count'] = db_session.query(Quote) \
			.filter(Quote.approved == False) \
			.count()

	return context
