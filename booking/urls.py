from django.urls import path
from .api import UserBookingsView, BookingCreateView, BookingListView, api_overview


urlpatterns = [

    path('', api_overview),
    path('list/', BookingListView.as_view(), name='booking_list'),
    path('create/', BookingCreateView.as_view(), name='booking_create'),
    path('user/bookings/', UserBookingsView.as_view(), name='user-bookings'),
]
