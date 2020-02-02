import pytest
from rest_framework.test import APIClient
from string import ascii_uppercase as letters, digits
from typing import List
import itertools
import os
from .models import Document
dir_path = os.path.dirname(os.path.realpath(__file__))
DOCUMENT_ENDPOINT = "/api/document/"
SEARCH_ENDPOINT = "/api/search/"


def generate_word(words=itertools.product(letters, letters, digits, digits, digits)):
	for word in words:
		yield "".join(word)


@pytest.fixture
def title():
	def __title():
		"""Generate a new random title"""
		return "TITLE"+next(generate_word())
	return __title


@pytest.fixture
def random_words():
	def __random_words():
		return ["WORD"+next(generate_word()) for _ in range(10)]

	return __random_words


@pytest.fixture
def api_client():
	"""API Client for testing"""
	return APIClient()


@pytest.fixture
def post_document(api_client: APIClient, create_content_from_sentences):
	"""Returns a helper function that creates documents with specified content"""

	def __create_document(content: str = None, sentences: List[str] = None, title: str = "test_doc.txt"):
		"""Use DRF test client to create a document via the API"""
		if sentences:
			content = create_content_from_sentences(sentences)
		return api_client.post(DOCUMENT_ENDPOINT, {"title": title, "content": content}, format="json")

	return __create_document


@pytest.fixture
def create_sentences(random_words):
	"""Returns a helper function that returns a list of sentences with specific length"""

	def __create_sentences(sentence_count: int):
		"""Generate and return random sentences"""
		return [" ".join(random_words()) for i in range(sentence_count - 1)]

	return __create_sentences


@pytest.fixture
def obama_speech(post_document):
	file_name = 'obama.txt'
	with open(dir_path+'/' + file_name, 'r') as fp:
		content = fp.read()
	document = Document(content=content, title=file_name)
	document.save()
	return document


@pytest.fixture
def create_content(create_sentences):
	"""Returns a helper function that creates document content with specified number of sentences"""

	def __create_content(sentence_count: int):
		"""Generate and return random content"""
		return ". ".join(create_sentences(sentence_count)) + "."

	return __create_content


@pytest.fixture
def create_content_from_sentences():
	"""Returns a helper function that creates document content with specified sentences"""

	def __create_content(sentences: List[str] = None):
		"""Join sentences into content"""
		return ". ".join(sentences) + "."

	return __create_content
