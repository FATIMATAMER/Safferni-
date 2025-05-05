from django.urls import path
from .api import UserBookingsView, BookingCreateView, BookingListView, api_overview, create_booking


urlpatterns = [

    path('', api_overview),
    path('list/', BookingListView.as_view(), name='booking_list'),
    path('c', create_booking),
    path('create/', BookingCreateView.as_view(), name='booking_create'),
    path('user/bookings/', UserBookingsView.as_view(), name='user-bookings'),
]
