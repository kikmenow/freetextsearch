from django.db import models
from dataclasses import dataclass
from django.db.models.query import QuerySet


class Document(models.Model):
	title = models.CharField(max_length=30, null=False)
	content = models.TextField(default="", null=False)


@dataclass
class SearchResult:
	documents: QuerySet
