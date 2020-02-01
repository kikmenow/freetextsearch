from rest_framework import serializers
from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
	sentences = serializers.SerializerMethodField()

	class Meta:
		model = Document
		fields = "__all__"

	# TODO: Don't respond with sentences. Not required.
	def get_sentences(self, obj):
		return [sentence.lstrip() for sentence in obj.content.split('.')]

