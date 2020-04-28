import pytest
import openevsewifi


@pytest.fixture
def test_charger():
    return openevsewifi.Charger('openevse.example.tld')
