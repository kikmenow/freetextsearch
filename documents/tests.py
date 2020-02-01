import pytest
from .conftest import DOCUMENT_ENDPOINT, SEARCH_ENDPOINT




@pytest.mark.django_db
def test_document_creation(create_document):
    result = create_document(
        title="test_document.txt",
        content="Test body"
    )
    assert result.status_code == 201
    assert result.data['title'] == "test_document.txt"
    assert result.data['content'] == "Test body"


@pytest.mark.django_db
def test_document_saving_returns_sentences(create_document, create_sentences):
    number_of_sentences = 3
    sentences = create_sentences(sentence_count=number_of_sentences)
    result = create_document(sentences=sentences)

    # TODO: I will be removing sentences from the response. This was partly a spike and
    # TODO: was here to drive out test suite capability, and also explore the simplest way to add
    # TODO: the concept of sentences into my application
    for i, sentence in enumerate(sentences):
        assert result.data['sentences'][i] == sentence
    assert len(result.data['sentences']) == number_of_sentences
