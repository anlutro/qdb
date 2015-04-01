# QDB

## Installation

Create a virtualenv for python 3:

	$ virtualenv -p python3 ./virtualenv

Activate the virtualenv:

	$ source ./virtualenv/bin/activate

Install dependencies with pip:

	$ pip install -r ./requirements.txt

Copy the config example file to `config.py`:

	$ cp config.example.py config.py

Replace the data in config.py as needed.

Run the schema script onto your SQLite database:

	$ sqlite3 ./tmp/test.db < ./database/schema.sqlite.sql

Run the application:

	$ ./run.py

Check the URL given on the command line to make sure it works.
