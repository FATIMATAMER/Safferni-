from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import api


router = DefaultRouter()
router.register( r'companies',api.CompanyViewSet ,basename='commpanies')

urlpatterns = [
    
    path('', api.api_overview),
    path('create/', api.CompanyListView.as_view(), name='company_list'),
    path('details<int:pk>', api.CompanyDetailView.as_view(), name='company_details'),
    path('',include(router.urls)),   
 ] 