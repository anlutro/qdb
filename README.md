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

Run the application:

	$ ./run.py

Check the URL given on the command line to make sure it works.

### PostgreSQL

If you want to run the application on top of PostgreSQL, you need to install psycopg2.

To install psycopg2 with pip, you need the `python-dev` package installed.

	$ pip install psycopg2
