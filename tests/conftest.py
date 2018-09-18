import os

import pytest
from webresultserver import app_factory

CONFIG_LOCATION = os.path.join(os.path.dirname(__file__), 'test_config.json')


@pytest.fixture(scope='session')
def app():
    try:
        os.environ[app_factory.CONFIG_LOCATION_ENVIRONMENT_VARIABLE] = CONFIG_LOCATION
        flask_app = app_factory.create_app(__name__)
        with flask_app.app_context():
            yield flask_app
    finally:
        if app_factory.CONFIG_LOCATION_ENVIRONMENT_VARIABLE in os.environ:
            del os.environ[app_factory.CONFIG_LOCATION_ENVIRONMENT_VARIABLE]
