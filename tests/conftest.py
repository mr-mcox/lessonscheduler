from app import create_app
import pytest
from app import db as _db
from alembic.command import upgrade
from alembic.config import Config
from flask.ext.migrate import upgrade
from flask.ext.migrate import Migrate


@pytest.fixture(scope='session')
def app():
    app = create_app('testing')
    return app


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""

    migrate = Migrate(app, _db)
    _db.app = app
    upgrade()

    return _db


@pytest.fixture(scope='function', autouse=True)
def reset_db(request, db):
    def clear_data():
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            print('Clear table %s' % table)
            db.session.execute(table.delete())
        db.session.commit()
    request.addfinalizer(clear_data)
