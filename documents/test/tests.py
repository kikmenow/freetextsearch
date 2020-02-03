import pytest
from documents.models import Document, Sentence
from .conftest import SEARCH_ENDPOINT


@pytest.mark.django_db
def test_saving_document_creates_sentences():
    Document(title="bar", content="bar bar baz. foo foo.").save()
    sentences = list(Sentence.objects.values_list('content', flat=True))
    assert "bar bar baz" in sentences
    assert "foo foo" in sentences
    assert "" not in sentences


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
def test_search_endpoint_returns_400_if_no_search_terms(api_client, create_content):
    content = create_content(5)
    document = Document(title='example.txt', content=content)
    document.save()
    result = api_client.get(f"{SEARCH_ENDPOINT}")
    assert result.status_code == 400
    assert "Missing search terms" in result.data
    result = api_client.get(f"{SEARCH_ENDPOINT}?term=")
    assert result.status_code == 400
    assert "Missing search terms" in result.data


@pytest.mark.django_db
def test_search_endpoint_can_return_multiple_documents_single_word_query(search, title):
    word = "hello"
    first_doc = Document(title=title(), content=word)
    first_doc.save()
    second_doc = Document(title=title(), content=word)
    second_doc.save()
    result = search(word)
    assert first_doc.title in result.result_for('hello')['documents']
    assert second_doc.title in result.result_for('hello')['documents']


@pytest.mark.django_db
def test_search_endpoint_can_return_documents_multi_word_query(search):
    Document(title="foo.txt", content="foo bar baz").save()
    Document(title="bar.txt", content="bar bar baz").save()
    result = search("foo", "baz")
    assert result.result_for("foo")['documents'] == ["foo.txt"]
    assert result.result_for("baz")['documents'] == ["foo.txt", "bar.txt"]


@pytest.mark.django_db
def test_search_endpoint_can_return_sentences_single_word_query(unique_words, post_document, search):
    word = unique_words()[0]
    positive_results = [" ".join(unique_words()) + f" {word}", " ".join(unique_words()) + f" {word}"]
    negative_results = [" ".join(unique_words())]
    post_document(sentences=(positive_results + negative_results))
    result = search(word)
    assert positive_results[0] in result.result_for(word)['sentences']
    assert positive_results[1] in result.result_for(word)['sentences']
    assert len(result.result_for(word)['sentences']) == len(positive_results)


@pytest.mark.django_db
def test_search_endpoint_can_return_instance_count_single_word_query(search):
    Document(title="foo", content="foo foo foo").save()
    Document(title="bar", content="bar bar foo").save()
    result = search("foo", "bar")
    assert result.result_for('foo')['count'] == 4
    assert result.result_for('bar')['count'] == 2


@pytest.mark.django_db
def test_search_endpoint_is_case_insensitive(search, post_document):
    post_document(content="Foo. foo. Foo")
    result = search("foo", "Foo")
    assert result.result_for('foo')['count'] == 3
    assert result.result_for('Foo')['count'] == 3


@pytest.mark.django_db
def test_search_endpoint_can_return_obama_document_for_various_terms(search, obama_speech: Document):
    obama_speech.save()
    result = search("let", "begin")
    assert obama_speech.title in result.result_for('let')['documents']
    assert obama_speech.title in result.result_for('begin')['documents']


@pytest.mark.django_db
def test_search_endpoint_sorts_by_hit_count(search, obama_speech: Document):
    obama_speech.save()
    result = search("begin", "believe")
    assert result.results[0]['search_term'] == "believe"
    assert result.results[1]['search_term'] == "begin"
    result = search("believe", "begin")
    assert result.results[0]['search_term'] == "believe"
    assert result.results[1]['search_term'] == "begin"

# TODO: Choose some words
# TODO: Find a pretty way to display the report!
# TODO: Finish README.md