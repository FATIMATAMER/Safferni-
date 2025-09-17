from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import api, views

router= DefaultRouter()
router.register(r'cancel',views.TripViewSet,basename='trips')

urlpatterns = [

    path('', api.api_overview),
    path('create/', api.TripListView.as_view(), name='trip_list'),
    path('detail/<int:pk>/', api.TripDetailView.as_view(), name='trip_detail'),
    path('', include(router.urls)),
]