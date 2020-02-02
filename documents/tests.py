import pytest
from .conftest import SEARCH_ENDPOINT
from .models import Document, Sentence


@pytest.mark.django_db
def test_saving_document_creates_sentences():
    # TODO: Move this test elsewhere
    Document(title="bar", content="bar bar baz. foo foo.").save()
    sentences = list(Sentence.objects.values_list('content', flat=True))
    assert "bar bar baz" in sentences
    assert "foo foo" in sentences
    assert "" not in sentences


# TODO: Refactor document endpoint tests to separate suite
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
    # TODO: Find a way to tidy up creation of django models
    document = Document(title=title(), content=create_content(5))
    document.save()
    word = document.content.split(' ')[0]
    result = api_client.get(f"{SEARCH_ENDPOINT}?term={word}")
    assert result.data[word]['documents'][0] == document.title


@pytest.mark.django_db
def test_search_endpoint_can_return_multiple_documents_single_word_query(api_client, title):
    word = "hello"
    first_doc = Document(title=title(), content=word)
    first_doc.save()
    second_doc = Document(title=title(), content=word)
    second_doc.save()
    result = api_client.get(f"{SEARCH_ENDPOINT}?term={word}")
    assert first_doc.title in result.data[word]['documents']
    assert second_doc.title in result.data[word]['documents']


@pytest.mark.django_db
def test_search_endpoint_can_return_documents_multi_word_query(api_client):
    Document(title="foo", content="foo bar baz").save()
    Document(title="bar", content="bar bar baz").save()
    result = api_client.get(f"{SEARCH_ENDPOINT}?term=foo&term=baz")
    assert result.data['foo']['documents'] == ["foo"]
    assert result.data['baz']['documents'] == ["foo", "bar"]


# TODO: perhaps try parameterising these tests with a generator fn instead of calling random_words a lot
@pytest.mark.django_db
def test_search_endpoint_can_return_sentences_single_word_query(api_client, random_words, post_document):
    # Todo: use random word
    test_word = "word"
    positive_results = [" ".join(random_words()) + f" {test_word}", " ".join(random_words()) + f" {test_word}"]
    negative_results = [" ".join(random_words())]
    post_document(sentences=(positive_results + negative_results))
    result = api_client.get(f"{SEARCH_ENDPOINT}?term={test_word}")
    assert positive_results[0] in result.data[test_word]['sentences']
    assert positive_results[1] in result.data[test_word]['sentences']
    assert len(result.data[test_word]['sentences']) == len(positive_results)


@pytest.mark.django_db
def test_search_endpoint_can_return_instance_count_single_word_query(api_client):
    Document(title="foo", content="foo foo foo").save()
    Document(title="bar", content="bar bar foo").save()
    # TODO: abstract api_client away under a search function fed in by pytest
    result = api_client.get(f"{SEARCH_ENDPOINT}?term=foo&term=bar")
    assert result.data['foo']['count'] == 4
    assert result.data['bar']['count'] == 2

# TODO: Test drive cleaning/casing/removal of odd characters inside sentences.

# TODO: The reason this is failing is due to postgres config. Will follow up later.
# @pytest.mark.django_db
# def test_search_endpoint_can_return_obama_document_for_various_terms(api_client, obama_speech: Document):
#     result = api_client.get(f"{SEARCH_ENDPOINT}?term=let&term=me&term=begin")
#     assert obama_speech.title in result.data['let']['documents']
#     assert obama_speech.title in result.data['me']['documents']
#     assert obama_speech.title in result.data['begin']['documents']