import pytest
import openevsewifi


@pytest.fixture
def test_charger():
    return openevsewifi.Charger('openevse.example.tld')

@pytest.fixture
def test_charger_json():
    return openevsewifi.Charger('openevse.example.tld', json=True)
