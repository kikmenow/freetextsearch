import pytest
from .conftest import SEARCH_ENDPOINT
from .models import Document


@pytest.mark.django_db
def test_document_creation(post_document):
    result = post_document(
        title="test_document.txt",
        content="Test body"
    )
    assert result.status_code == 201
    assert result.data['title'] == "test_document.txt"
    assert result.data['content'] == "Test body"


@pytest.mark.django_db
def test_document_saving_returns_sentences(post_document, create_sentences):
    number_of_sentences = 3
    sentences = create_sentences(sentence_count=number_of_sentences)
    result = post_document(sentences=sentences)
    # TODO: I will be removing sentences from the response. This was partly an investigation and
    # TODO: was here to drive out test suite capability, and also explore the simplest way to add
    # TODO: the concept of sentences into my application
    for i, sentence in enumerate(sentences):
        assert result.data['sentences'][i] == sentence
    assert len(result.data['sentences']) == number_of_sentences


@pytest.mark.django_db
def test_search_endpoint_returns_400_if_no_search_terms(api_client, create_content):
    document = Document(title='example.txt', content=create_content(5))
    document.save()
    result = api_client.get(f"{SEARCH_ENDPOINT}")
    # TODO: Add error message to body
    assert result.status_code == 400


@pytest.mark.django_db
def test_search_endpoint_can_return_documents_single_word_query(api_client, create_content, title):
    document = Document(title=title, content=create_content(5))
    document.save()
    word = document.content.split(' ')[0]
    result = api_client.get(f"{SEARCH_ENDPOINT}?search={word}")
    assert result.data[0]['documents'][0] == title
    assert result.data[0]['word'] == word
