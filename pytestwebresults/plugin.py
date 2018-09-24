from urllib.parse import urljoin

import pytest
import requests

SERVER_HOST_FLAG = '--server-host'
SERVER_PORT_FLAG = '--server-port'


def pytest_addoption(parser):
    """
    :type parser: _pytest.config.argparsing.Parser
    """
    option_group = parser.getgroup('Pytest Web Results')
    option_group.addoption(SERVER_HOST_FLAG, help='Result server host')
    option_group.addoption(SERVER_PORT_FLAG, help='Result server port (default is 80)')


def pytest_configure(config):
    """
    :type config: _pytest.config.Config
    """
    server_host = config.getoption(SERVER_HOST_FLAG)
    config.is_using_web_results = bool(server_host)
    if config.is_using_web_results:
        server_port = config.getoption(SERVER_PORT_FLAG)
        port_string = ':{port}'.format(port=server_port) if server_port else ''
        config.api_base_url = urljoin('http://{host}{port}'.format(host=server_host,
                                                                   port=port_string), 'api/')


def pytest_sessionstart(session):
    """
    :type session: _pytest.main.Session
    """
    if session.config.is_using_web_results:
        response = requests.post(urljoin(session.config.api_base_url, 'add_session'))
        session.config.session_id = response.text.strip()


def pytest_itemcollected(item):
    """
    :type item: _pytest.nodes.Item
    """
    if item.config.is_using_web_results:
        add_item_url = urljoin(item.config.api_base_url,
                               '/'.join(('add_test_item', item.config.session_id, item.nodeid)))
        response = requests.post(add_item_url)
        item.db_id = response.text.strip()


# noinspection PyUnresolvedReferences
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """
    :type item: _pytest.nodes.Item
    """
    if item.config.is_using_web_results:
        change_state_url = urljoin(item.config.api_base_url,
                                   '/'.join(('change_test_state', item.db_id, 'RUNNING_SETUP')))
        requests.put(change_state_url)


# noinspection PyUnresolvedReferences
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_call(item):
    """
    :type item: _pytest.nodes.Item
    """
    if item.config.is_using_web_results:
        change_state_url = urljoin(item.config.api_base_url,
                                   '/'.join(('change_test_state', item.db_id, 'RUNNING_TEST')))
        requests.put(change_state_url)


# noinspection PyIncorrectDocstring,PyUnusedLocal,PyUnresolvedReferences
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    :type item: _pytest.nodes.Item
    """
    hook_outcome = yield
    if item.config.is_using_web_results:
        report = hook_outcome.get_result()
        if report.when == 'call':
            item.test_outcome = report.outcome
        elif report.when == 'teardown':
            if report.outcome == 'passed':
                change_state_url = urljoin(item.config.api_base_url, '/'.join(
                    ('change_test_state', item.db_id, item.test_outcome)))
            else:
                change_state_url = urljoin(item.config.api_base_url, '/'.join(
                    ('change_test_state', item.db_id, report.outcome)))
            requests.put(change_state_url)


# noinspection PyUnusedLocal,PyIncorrectDocstring,PyUnresolvedReferences
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_teardown(item, nextitem):
    """
    :type item: _pytest.nodes.Item
    """
    if item.config.is_using_web_results:
        change_state_url = urljoin(item.config.api_base_url,
                                   '/'.join(('change_test_state', item.db_id, 'RUNNING_TEARDOWN')))
        requests.put(change_state_url)
