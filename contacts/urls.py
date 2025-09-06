from rest_framework.routers import DefaultRouter
from .api import ContactViewSet

from django.urls import path, include


router = DefaultRouter()
router.register(r'contact', ContactViewSet, basename='contact')

urlpatterns = [

    path('', include(router.urls)),
]
