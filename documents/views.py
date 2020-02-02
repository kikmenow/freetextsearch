from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Document
from .serializers import DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


@api_view(['GET'])
def search(request):
    """
    Initially we will use request.GET['search']
    but afterwards we will use request.GET.getlist('search') to take in multiple words/phrases simultaneously.
    """
    if 'search' not in request.GET:
        return Response(status=400)
    documents = list(
        Document.objects.filter(content__search=request.GET['search']).values_list('title', flat=True)
    )
    return Response(
            {
                request.GET['search']: {
                    "documents": documents
                }
            }
    )


