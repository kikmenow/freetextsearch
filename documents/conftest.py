import pytest
from rest_framework.test import APIClient
from typing import List

from random_word import RandomWords
r = RandomWords()

DOCUMENT_ENDPOINT = "/api/document/"
SEARCH_ENDPOINT = "/search/"


@pytest.fixture
def api_client():
	"""API Client for testing"""
	return APIClient()


@pytest.fixture
def create_document(api_client: APIClient, create_content):
	"""Returns a helper function that creates documents with specified content"""
	def __create_document(content: str = None, sentences: List[str] = None, title: str = "test_doc.txt"):
		"""Use DRF test client to create a document via the API"""
		if sentences:
			content = create_content(sentences)
		return api_client.post(DOCUMENT_ENDPOINT, {"title": title, "content": content}, format="json")
	return __create_document


@pytest.fixture
def create_sentences():
	"""Returns a helper function that creates a sentence list with specified number of sentences"""
	def __create_sentences(sentence_count: int):
		"""Generate and return random sentences"""
		return [" ".join(r.get_random_words(limit=10)) for i in range(sentence_count - 1)]
	return __create_sentences


@pytest.fixture
def create_content():
	"""Returns a helper function that creates document content with specified number of sentences"""
	def __create_content(sentences: List[str] = None):
		"""Generate and return random content"""
		return ". ".join(sentences) + "."
	return __create_content
