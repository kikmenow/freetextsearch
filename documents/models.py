from django.db import models
from dataclasses import dataclass
from django.db.models.query import QuerySet


class Document(models.Model):
	title = models.CharField(max_length=30, null=False)
	content = models.TextField(default="", null=False)

	def save(self, *args, **kwargs):
		super(Document, self).save(*args, **kwargs)
		sentences = list(filter(None, [sentence.lstrip() for sentence in self.content.split('.')]))
		for sentence_content in sentences:
			Sentence(content=sentence_content, document=self).save()


class Sentence(models.Model):
	document = models.ForeignKey(Document, related_name='sentences', on_delete=models.CASCADE)
	content = models.TextField(default="", null=False)


@dataclass
class SearchResult:
	documents: QuerySet
