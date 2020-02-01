from rest_framework import routers
from django.conf.urls import include, url

from . import views

router = routers.DefaultRouter()

router.register(r"document", views.DocumentViewSet, basename="document")

urlpatterns = [
	url(r'', include(router.urls))
]
