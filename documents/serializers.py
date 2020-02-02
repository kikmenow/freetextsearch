from rest_framework import serializers
from .models import Document, SearchResult, Sentence
from typing import List


class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = "__all__"


class DocumentSerializer(serializers.ModelSerializer):
    sentences = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='content'
    )

    class Meta:
        model = Document
        fields = "__all__"


class SearchResultSerializer(serializers.Serializer):
    documents = serializers.SerializerMethodField()
    sentences = serializers.SerializerMethodField()

    def get_documents(self, obj: SearchResult) -> List[str]:
        return list(
            obj.documents.values_list('title', flat=True)
        )

    def get_sentences(self, obj: SearchResult):
        return list(
            obj.sentences.values_list('content', flat=True)
        )
