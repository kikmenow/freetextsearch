import pytest


@pytest.mark.django_db
def test_contract(api_client):
    result = api_client.get("/search/").data
    assert result.status_code is 200
    assert result.data is {}
