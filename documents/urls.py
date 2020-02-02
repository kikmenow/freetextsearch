from rest_framework import routers
from django.conf.urls import include
from django.urls import path
from . import views


router = routers.DefaultRouter()

router.register(r"document", views.DocumentViewSet, basename="document")

urlpatterns = [
	path(r"", include(router.urls)),
	path(r"search/", views.search, name='search')
]
