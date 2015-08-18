# enable or disable debug mode
DEBUG = True

# secret key used for session stuff
SECRET_KEY = 'IAMTOTALLYNOTSECRET!'

# the moderator password
PASSWORD = 'whathefuck'

# the sqlite database string
# http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls
import os.path
DB = 'sqlite:////{}/tmp/test.db'.format(os.path.dirname(__file__))
# DB = 'postgresql://user:pass@localhost/dbname'