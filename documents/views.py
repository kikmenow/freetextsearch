from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Document, SearchResult, Sentence
from .serializers import DocumentSerializer, SearchResultSerializer
from django.db.models.query import QuerySet
from typing import List, Dict


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


@api_view(['GET'])
def search(request):
    search_terms = request.GET.getlist('term')
    search_terms = list(filter(None, search_terms))
    if not search_terms:
        return Response(status=400, data="Missing search terms")
    search_results = generate_search_response(search_terms)
    return Response(
        search_results
    )


def generate_search_response(search_terms):
    search_results = [
        SearchResultSerializer(
            SearchResult(
                sentences=get_sentences_by_search_term(search_term),
                search_term=search_term
            )
        ).data for search_term in search_terms
    ]
    return sort_by_count(search_results)


def sort_by_count(search_results: List[Dict]):
    return sorted(search_results, key=lambda k: k['count'], reverse=True)


def get_sentences_by_search_term(term: str) -> QuerySet:
    return Sentence.objects.filter(content__search=term)
