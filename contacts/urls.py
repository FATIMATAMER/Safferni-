from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.decorators.csrf import csrf_exempt
from .api import ContactViewSet

contact_post = csrf_exempt(ContactViewSet.as_view({'post': 'create'}))

router = DefaultRouter()
router.register(r'contact', ContactViewSet, basename='contact')


urlpatterns = [
    path('contact/contact/', contact_post, name='contact_us'),
    
    path('', include(router.urls)),
]