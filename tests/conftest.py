import pytest


@pytest.fixture
def app():
    import qdb

    qdb.app.testing = True
    return qdb.app


@pytest.fixture
def db(request, tmpdir):
    import qdb.database

    qdb.app.config["DB"] = tmpdir.mkdir("db").join("test.sqlite").realpath
    qdb.database.init_db()
    return qdb.database.db_session
