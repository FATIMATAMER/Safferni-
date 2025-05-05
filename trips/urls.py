from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import api

# router= DefaultRouter()
# router.register(r'trips',api.TripViewSet,basename='trips')

# urlpatterns = [
#    path('',include(router.urls)),    
# ]

urlpatterns = [

    path('', api.api_overview),
    path('create/', api.TripListView.as_view(), name='trip_list'),
    path('detail/<int:pk>/', api.TripDetailView.as_view(), name='trip_detail'),
]