from rest_framework import generics, serializers, viewsets, permissions
from .models import Trip, BookingUser
from .serializers import BookingSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timezone

from rest_framework.decorators import api_view, permission_classes, action


@api_view(['GET'])
def api_overview(request):
     
	api_urls = {

        'auth api overview' : '/',
        'List authenticated user bookings' : 'me/',
        'create bookings' : 'book/',
        'Update, retreive and delete a bookings' : 'book/<int:id>',
		}

	return Response(api_urls)


class BookingViewSet(viewsets.ModelViewSet):
    
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return BookingUser.objects.filter(user=self.request.user).order_by('-booking_date')
    
    def perform_create(self, serializer):
        
        trip = serializer.validated_data['trip']
        number_of_seats = serializer.validated_data['number_of_seats']

        # Calculate assigned seats
        seat_start = trip.total_seats - trip.available_seats + 1
        seat_end = seat_start + number_of_seats - 1
        assigned_seats = list(range(seat_start, seat_end + 1))

        # Save the booking with user info
        booking = serializer.save(user=self.request.user)

        # Attach assigned_seats for serializer use (not saved in DB)
        booking.assigned_seats = assigned_seats
        booking.seat_start = seat_start
        booking.seat_end = seat_end

        # Update available seats
        trip.available_seats -= number_of_seats
        trip.save()

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        
        if booking.is_cancelled:
            return Response(
                {"detail": "Booking is already cancelled."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if booking.trip.booking_date < timezone.now().date():
            return Response(
                {"detail": "Cannot cancel booking for past trips."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if booking.trip.departure_date == timezone.now().date():
            if booking.trip.departure_date and booking.trip.departure_date < timezone.now().time():
                return Response(
                    {"detail": "Cannot cancel booking as the bus has already departed."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        booking.cancel()
        return Response(
            {"detail": "Booking cancelled successfully."},
            status=status.HTTP_200_OK
        )
    

class UserBookingsView(generics.ListAPIView):

    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BookingUser.objects.filter(user=self.request.user)
    

