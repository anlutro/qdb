from qdb import app
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(app.config.get('DB'), convert_unicode=True)
session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(session_maker)
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that they will be
    # registered properly on the metadata.  Otherwise you will have to import
    # them first before calling init_db()
    import qdb.models

    # if app.debug is true, try to create the database schema. this makes it
    # easy to do local testing, especially with sqlite - any time there's a
    # change in the schema, simply delete the database and it will be
    # recreated.
    if app.debug:
        Base.metadata.create_all(bind=engine)
