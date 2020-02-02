from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Document
from .serializers import DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


def get_documents_by_search_term(term: str):
    return list(
        Document.objects.filter(content__search=term).values_list('title', flat=True)
    )


@api_view(['GET'])
def search(request):
    search_terms = request.GET.getlist('search')
    if not search_terms:
        return Response(status=400)

    search_results = [{"documents": get_documents_by_search_term(search_term)} for search_term in search_terms]
    return Response(
        dict(zip(search_terms, search_results))
    )


