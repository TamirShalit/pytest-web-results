import os

import pytest
from webresultserver import app_factory

pytest_plugins = 'pytester'

CONFIG_LOCATION = os.path.join(os.path.dirname(__file__), 'test_config.json')


@pytest.fixture
def app():
    try:
        os.environ[app_factory.CONFIG_LOCATION_ENVIRONMENT_VARIABLE] = CONFIG_LOCATION
        flask_app = app_factory.create_app(__name__)

        with flask_app.app_context():
            app_factory.create_db(flask_app)
            app_factory.create_rest_api(flask_app)
            yield flask_app
    finally:
        if app_factory.CONFIG_LOCATION_ENVIRONMENT_VARIABLE in os.environ:
            del os.environ[app_factory.CONFIG_LOCATION_ENVIRONMENT_VARIABLE]
