from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Document, SearchResult, Sentence
from .serializers import DocumentSerializer, SearchResultSerializer
from django.db.models.query import QuerySet


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


def get_documents_by_search_term(term: str) -> QuerySet:
    return Document.objects.filter(content__search=term)


def get_sentences_by_search_term(term: str) -> QuerySet:
    return Sentence.objects.filter(content__search=term)


@api_view(['GET'])
def search(request):
    search_terms = request.GET.getlist('term')
    search_terms = list(filter(None, search_terms))
    if not search_terms:
        return Response(status=400, data="Missing search terms")
    search_results = [
        SearchResultSerializer(
            SearchResult(
                sentences=get_sentences_by_search_term(search_term),
                search_term=search_term
            )
        ).data for search_term in search_terms
    ]
    return Response(
        dict(zip(search_terms, search_results))
    )


