def pytest_addoption(parser):
    """
    :type parser: _pytest.config.argparsing.Parser
    """
    option_group = parser.getgroup('Pytest Web Results')
    option_group.addoption('--server-host', help='Result server host')
    option_group.addoption('--server-port', default=80, help='Result server port (default is 80)')
