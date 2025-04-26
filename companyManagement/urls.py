from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import api
from .api import delete_company

router = DefaultRouter()
router.register( r'companies',api.CompanyViewSet ,basename='commpanies')
urlpatterns = [
 path('',include(router.urls)),   
 path('<int:company_id>/delete/', delete_company, name='delete_company'),
 ] 