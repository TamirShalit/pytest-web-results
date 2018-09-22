import http
import os

import pytest
from webresultserver.models.item import ItemState

from pytestwebresults import plugin

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'simple_outcome_test.template')


def assert_test_outcome(flask_client, expected_outcome):
    url_arguments = {'single': True}
    response = flask_client.get('/api/test_item', query_string=url_arguments)
    assert response.status_code == http.HTTPStatus.OK
    response_dict = response.get_json()
    print(response_dict)
    assert response_dict['num_results'], "Couldn't find test item"
    test_item_dict = response_dict['objects'][0]
    assert test_item_dict['state'] == expected_outcome.value


@pytest.mark.parametrize('test_function, expected_outcome', [
    ('lambda: None', ItemState.PASSED),
    # ('pytest.fail', ItemState.FAILED),
    # ('pytest.xfail', ItemState.XFAILED),
    # ('pytest.skip', ItemState.SKIPPED),
])
def test_simple_outcome(testdir, live_server, client, test_function, expected_outcome):
    with open(TEMPLATE_PATH) as template_file:
        test_code = template_file.read().format(test_function=test_function)
    testdir.makepyfile(test_code)
    testdir.runpytest(plugin.SERVER_HOST_FLAG, 'localhost', plugin.SERVER_PORT_FLAG,
                      str(live_server.port))
    assert_test_outcome(client, expected_outcome)
