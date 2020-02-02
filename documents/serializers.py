from rest_framework import serializers
from .models import Document, SearchResult, Sentence
from typing import List
from django.db.models import Subquery
from nltk import word_tokenize, Text
import itertools


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
    count = serializers.SerializerMethodField()

    def get_documents(self, obj: SearchResult) -> List[str]:
        documents = Document.objects.filter(
            pk__in=Subquery(
                obj.sentences.values('document_id')
            )
        )
        return list(
            documents.values_list('title', flat=True)
        )

    def get_sentences(self, obj: SearchResult) -> List[str]:
        return list(
            obj.sentences.values_list('content', flat=True)
        )

    def get_count(self, obj: SearchResult) -> int:
        sentences = self.get_sentences(obj)
        tokens = [word_tokenize(sentence) for sentence in sentences]
        flat_tokens = list(itertools.chain(*tokens))
        text = Text(flat_tokens)
        return text.count(obj.search_term)

