from django.urls import path
from .api import BookingCreateView, BookingListView
from .api import UserBookingsView

urlpatterns = [

    path('bookings/', BookingListView.as_view(), name='booking_list'),
    path('bookings/create/', BookingCreateView.as_view(), name='booking_create'),
    path('user/bookings/', UserBookingsView.as_view(), name='user-bookings'),
]