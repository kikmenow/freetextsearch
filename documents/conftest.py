import pytest
from rest_framework.test import APIClient

DOCUMENT_ENDPOINT = "/document/"
SEARCH_ENDPOINT = "/search/"


@pytest.fixture
def api_client():
	"""API Client for testing"""
	return APIClient()


@pytest.fixture()
def create_document(api_client: APIClient):
	"""Return a helper function for creating document fixtures with particular keywords"""
	def __create_document(document_body: str):
		"""Use API DRF test client to create a document via the API"""
		return api_client.post(DOCUMENT_ENDPOINT, {"body": document_body}, format="json")
	return __create_document

