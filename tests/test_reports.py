import pytest

from webresultserver.models.item import ItemState


@pytest.fixture
def assert_test_report(request):
    yield
    # TODO assert answer using REST


@pytest.mark.parametrize('test_function, assert_test_report', [
    (lambda: None, ItemState.PASSED),
    (pytest.fail, ItemState.FAILED),
    (pytest.xfail, ItemState.XFAILED),
    (pytest.skip, ItemState.SKIPPED),
], indirect=['assert_test_report'])
def test_simple_outcome(test_function, assert_test_report):
    test_function()
