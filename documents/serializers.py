from rest_framework import serializers
from .models import Document, SearchResult
from typing import List


class DocumentSerializer(serializers.ModelSerializer):
    sentences = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = "__all__"

    # TODO: Don't respond with sentences. Not required.
    def get_sentences(self, obj):
        return [sentence.lstrip() for sentence in obj.content.split('.')]


class SearchResultSerializer(serializers.Serializer):
    documents = serializers.SerializerMethodField()
    # count = serializers.SerializerMethodField()

    def get_documents(self, obj: SearchResult) -> List[str]:
        return list(
            obj.documents.values_list('title', flat=True)
        )

    # def get_count(self, obj: SearchResult) -> int:
    #     return 1

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass