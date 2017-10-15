# find the project root directory
import os.path
root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

# initiate the flask app
from flask import Flask, session, url_for
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
		extensions=['jinja2.ext.with_'],
		bytecode_cache=FileSystemBytecodeCache(j2cachedir, '%s.cache'),
	)

# set up logging to stderr
import logging
import sys
file_handler = logging.StreamHandler(sys.stderr)
file_handler.setLevel(logging.WARNING)
app.logger.addHandler(file_handler)

if app.config.get('OPBEAT'):
	from opbeat.contrib.flask import Opbeat
	opbeat = Opbeat(app)


# replace the json encoder
from qdb.utils import CustomJSONEncoder
app.json_encoder = CustomJSONEncoder

# register routes
import qdb.routes

@app.teardown_appcontext
def shutdown_session(exception=None):
	from qdb.database import db_session
	db_session.remove()

@app.context_processor
def jinja_globals():
	# inject global jinja variables
	from qdb.database import db_session
	from qdb.models import Quote

	context = dict()

	if session.get('logged_in'):
		context['pending_count'] = db_session.query(Quote) \
			.filter(Quote.approved == None) \
			.count()

	# cache busting URLs
	if not app.debug:
		url_cache = {}

		def dated_url_for(endpoint, **values):
			if endpoint == 'static':
				filename = values.get('filename')
				if filename:
					if filename not in url_cache:
						file_path = os.path.join(app.static_folder, filename)
						if os.path.isfile(file_path):
							timestamp = int(os.stat(file_path).st_mtime)
							directory, filename = os.path.split(filename)
							filename, extension = filename.split('.', 1)
							filename = '{}.{}.{}'.format(filename, timestamp, extension)
							url_cache[filename] = os.path.join(directory, filename)
						else:
							url_cache[filename] = filename
					values['filename'] = url_cache[filename]
			return url_for(endpoint, **values)

		context['url_for'] = dated_url_for

	return context
