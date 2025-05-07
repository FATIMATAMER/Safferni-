from . import api
from rest_framework.routers import DefaultRouter

from django.urls import path, include


router = DefaultRouter()
router.register(r'book', api.BookingViewSet, basename='book')

urlpatterns = [

    path('', api.api_overview, name='make_reservation_overview'),
    path('me/', api.UserBookingsView.as_view(), name='user_bookings'),
    path('', include(router.urls)),
]
