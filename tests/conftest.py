import os

import pytest
from webresultserver import app_factory

pytest_plugins = 'pytester'

CONFIG_TEMPLATE_LOCATION = os.path.join(os.path.dirname(__file__), 'test_config.template')


@pytest.fixture
def app(tmpdir):
    """
    :type tmpdir: py._path.local.LocalPath
    """
    db_location = tmpdir.join('test.db')
    with open(CONFIG_TEMPLATE_LOCATION) as config_template_file:
        config_content = config_template_file.read().format(db_location=db_location.strpath)
    config_location = tmpdir.join('test_config.json')
    config_location.write(config_content)
    try:
        os.environ[app_factory.CONFIG_LOCATION_ENVIRONMENT_VARIABLE] = config_location.strpath
        flask_app = app_factory.create_app(__name__)

        with flask_app.app_context():
            app_factory.create_db(flask_app)
            app_factory.create_rest_api(flask_app)
            yield flask_app
    finally:
        if app_factory.CONFIG_LOCATION_ENVIRONMENT_VARIABLE in os.environ:
            del os.environ[app_factory.CONFIG_LOCATION_ENVIRONMENT_VARIABLE]
