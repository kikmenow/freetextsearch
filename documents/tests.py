import pytest
from .conftest import DOCUMENT_ENDPOINT, SEARCH_ENDPOINT


# @pytest.mark.django_db
# def test_search_endpoint(api_client, create_document):
#     create_document("this is a test document")
#     result = api_client.get("/search/").data
#     assert result.status_code is 200
#     assert result.data is {}


@pytest.mark.django_db
def test_document_creation(api_client):
    result = api_client.post(DOCUMENT_ENDPOINT, {"name": "test_document.txt", "body": "Test body"}, format="json")
    assert result.status_code == 200


# @pytest.mark.django_db
# def test_document_creation_two_sentences(api_client):
#     result = api_client.post(DOCUMENT_ENDPOINT, {"body": "First sentence. Another sentence."}, format="json")
