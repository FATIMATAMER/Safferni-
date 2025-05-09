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
    
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])  # يجب أن يكون المستخدم مسجلاً للدخول إجبارية مسجل دخول 
# def create_booking(request):

#     trip_id = request.data.get('trip_id')
#     seat_number = request.data.get('seat_number')

#  # تحقق من وجود الرحلة
#     try:
#         trip = Trip.objects.get(id=trip_id)
#     except Trip.DoesNotExist:
#         return Response({"detail": "Trip not found."}, status=status.HTTP_404_NOT_FOUND)

#   # تحقق من وجود مقاعد متاحة
#     if trip.available_seats <= 0:
#         return Response({"detail": "No available seats."}, status=status.HTTP_400_BAD_REQUEST)
#   # التحقق ان كان المقعد محوز ام لا 
#     if BookingUser.objects.filter(trip=trip, seat_number=seat_number).exists():
#         return Response({"detail": "Seat already booked."}, status=status.HTTP_400_BAD_REQUEST)

#   # إنشاء الحجز
#     booking = BookingUser.objects.create(
#         trip=trip,
#         passenger=request.user,
#         seat_number=seat_number
#     )

#     # تحديث عدد المقاعد المتاحة
#     trip.available_seats -= 1
#     trip.save()

#     # إعادة استجابة بنجاح الحجز
#     return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)


# class BookingCreateView(generics.CreateAPIView):

#     queryset = BookingUser.objects.all()
#     serializer_class = BookingSerializer
#     permission_classes = [IsAuthenticated]

    
#     def create(self, request, *args, **kwargs):
#         trip_id = request.data.get('trip')
#         seat_number = request.data.get('seat_number')
#         trip = Trip.objects.get(id=trip_id)
        
#         # تحقق من المقاعد المتاحة
#         if trip.available_seats > 0:
#             booking = super().create(request, *args, **kwargs)
#             trip.available_seats -= 1  # تقليل المقاعد المتاحة
#             trip.save()
#             return booking
#         else:
#             return Response({"detail": "No available seats"}, status=status.HTTP_400_BAD_REQUEST)
        

# class BookingListView(generics.ListAPIView):

#     queryset = BookingUser.objects.all()
#     serializer_class = BookingSerializer
#     permission_classes = [IsAuthenticated]


