# QDB

[![Build Status](https://travis-ci.org/anlutro/qdb.png?branch=master)](https://travis-ci.org/anlutro/qdb)

## Installation

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

Run the application:

	$ ./run

Check the URL given on the command line to make sure it works.
