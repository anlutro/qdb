# QDB

[![Build Status](https://travis-ci.org/anlutro/qdb.png?branch=master)](https://travis-ci.org/anlutro/qdb)

## Installation

Clone the repository:

	$ git clone https://github.com/anlutro/qdb
	$ cd qdb

Create a virtualenv for python 3:

	$ virtualenv -p python3 .virtualenv

Activate the virtualenv:

	$ source ./.virtualenv/bin/activate

Install dependencies with pip:

	$ pip install -r requirements.txt

Or if you want to run with postgres:

	$ pip install -r requirements_pg.txt

Copy the config example file to `config.py`:

	$ cp config.example.py config.py

Replace the data in config.py as needed.

Run the application (for local development only):

	$ ./run

Go to `localhost:5000` in your browser of choice to make sure it works.

## UWSGI

In production I recommend running the app with UWSGI. Here's an example uwsgi.ini:

	[uwsgi]
	plugin = python3,logfile
	module = qdb:app
	chdir = /var/www/qdb
	venv = /var/www/qdb/.virtualenv
	logger = file:/var/log/www/qdb/uwsgi.log
	lazy-apps = True
	master = True
