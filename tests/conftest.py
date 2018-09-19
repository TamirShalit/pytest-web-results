import json
import os

import pytest
from webresultserver import app_factory

CONFIG_LOCATION = os.path.join(os.path.dirname(__file__), 'test_config.json')


@pytest.fixture(scope='session')
def flask_client():
    try:
        os.environ[app_factory.CONFIG_LOCATION_ENVIRONMENT_VARIABLE] = CONFIG_LOCATION
        flask_app = app_factory.create_app(__name__)

        test_client = flask_app.test_client()
        with flask_app.app_context():
            app_factory.create_db(flask_app)
            app_factory.create_rest_api(flask_app)
            yield test_client
    finally:
        if app_factory.CONFIG_LOCATION_ENVIRONMENT_VARIABLE in os.environ:
            del os.environ[app_factory.CONFIG_LOCATION_ENVIRONMENT_VARIABLE]


def assert_test_outcome(flask_client, nodeid, expected_outcome):
    filters = [dict(name='nodeid', op='==', val=nodeid)]
    url_arguments = dict(q=json.dumps(dict(filters=filters)), single=True)

    response = flask_client.get('/api/test_item', query_string=url_arguments)
    assert response.status_code == 200
    response_dict = response.get_json()
    assert response_dict['num_results'], "Couldn't find test item with nodeid {nodeid}".format(
        nodeid=nodeid)
    test_item_dict = response_dict['objects'][0]
    assert test_item_dict['state'] == expected_outcome.value
